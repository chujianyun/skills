# Self-hosted LangSmith changelog

**Subscribe**: Our changelog includes an [RSS feed](https://docs.langchain.com/langsmith/self-hosted-changelog/rss.xml) that can integrate with [Slack](https://slack.com/help/articles/218688467-Add-RSS-feeds-to-Slack), [email](https://zapier.com/apps/email/integrations/rss/1441/send-new-rss-feed-entries-via-email), Discord bots like [Readybot](https://readybot.io/) or [RSS Feeds to Discord Bot](https://rss.app/en/bots/rssfeeds-discord-bot), and other subscription tools.

[Self-hosted LangSmith](../Self-hosted%20LangSmith.md) is an add-on to the Enterprise plan designed for our largest, most security-conscious customers. For more details, refer to [Pricing](https://www.langchain.com/pricing). [Contact our sales team](https://www.langchain.com/contact-sales) if you want a license key to trial LangSmith in your environment.

**2026-11-12**

## langsmith-0.17.52

**LangSmith version:** `0.17.75`

* Run detail pages no longer get stuck loading when the trace runs request fails or does not return the selected run.

* The sandbox-host image builds Firecracker with the upstream fix for CVE-2026-122192 (GHSA-48ww-rqpp-2mgm). This prevents root inside a sandbox from reading or modifying Firecracker process memory after a failed memory discard.

* Fixed security vulnerabilities. See CVE-2026-122192 for details.

**Download the Helm chart:** [`langsmith-0.17.52.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.52/langsmith-0.17.52.tgz)

**2026-11-12**

## langsmith-0.18.0-rc.73

**LangSmith version:** `0.18.26rc1`

* This release packages the same LangSmith application version as langsmith-0.18.0-rc.72. Refer to the [langsmith-0.18.0-rc.72](#langsmith-0-18-0-rc-72) release notes below for application changes.
* Requests to `/api/v1/workspaces/current/deprecated-api-usage` route to the platform backend, with or without `config.basePath`. All other `/api/v1/workspaces/` routes remain on the backend.

**Download the Helm chart:** [`langsmith-0.18.0-rc.73.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.18.0-rc.73/langsmith-0.18.0-rc.73.tgz)

**Sandbox runtime chart, for Sandboxes in a separate cluster:** [`langsmith-sandbox-0.18.0-rc.7.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-sandbox-0.18.0-rc.7/langsmith-sandbox-0.18.0-rc.7.tgz)

**2026-11-12**

## langsmith-0.18.0-rc.72

**LangSmith version:** `0.18.26rc1`

* JavaScript graph factories deployed on the Python Agent Server receive a second runtime argument with access and execution context, matching the JavaScript Agent Server. This prevents deployment failures for factories that rely on runtime data and leaves factories that accept only `config` unaffected.
* The Coding Agent overview's work-type cost breakdown matches the LLM cost card for the selected time range, eliminating inflated cost figures.
* Grouped metrics on the Coding Agent overview appear as one horizontal bar per group for the selected date range, rather than as time series. Grouped merge rate and cost per merged PR use the full range instead of averaging daily values, while ungrouped charts remain unchanged.
* Agent Server images bundle Datadog init 1.11.4 to address vulnerable dependencies.
* The JavaScript SDK compresses queued trace uploads with Zstandard when both the server and Node.js runtime support it, retaining existing compression behavior otherwise. Set `LANGSMITH_RUN_COMPRESSION_LEVEL` and `LANGSMITH_RUN_COMPRESSION_WINDOW_LOG` to tune compression, noting that larger windows increase server memory usage per upload.
* Gateway traces omit provider error text when content capture is disabled or an export retries in metadata-only mode after a monthly quota rejection. Traces still record the error status without retaining sensitive provider response text.
* Thread streams in `lifecycle` mode emit `interrupts` events so clients can see which interrupts another client answered. Streams resumed with `Last-Event-ID` also replay these events for runs created with `stream_resumable`.
* Forking from a checkpoint with `run.start` starts a new run even when the thread has pending interrupts. This prevents message edits from being dropped or forks from being rejected as ambiguous interrupt responses.
* The server automatically sets the Go soft memory limit to 90% of the container's memory limit. This triggers garbage collection earlier and reduces the risk of out-of-memory failures during slow model responses.
* You can retrieve agent runtime details through `GET /v1/platform/agent-runtimes/{id}`, with a consistent response across runtime sources. Agent lookups support `include=runtime_bindings` to discover runtime IDs.
* Feedback category lists scroll within the editor so **Add category** and **Save** remain reachable, including on short screens. Newly added category labels receive focus and scroll into view automatically.
* Slack users receive a private **Confirm** or **Cancel** prompt before changes that require approval, including creating datasets and adding examples. Mentioning the bot again while approval is pending cancels the pending change before processing the new request.
* Go API requests can look up project deployments without authorization failures. Self-hosted installations must upgrade to a release containing this fix before adopting v2 session `PATCH`.
* Thread search and count endpoints accept `state_updated_after` (inclusive) and `state_updated_before` (exclusive) filters to find threads by when their state last changed. These filters ignore metadata-only and status-only changes and fall back to the thread's last update time for older threads without a state-update timestamp.
* Servers wait for pending database migrations before starting, and concurrent index builds no longer fail because of a one-second lock timeout. If you use a startup probe timeout shorter than the new `STARTUP_TIMEOUT_SECONDS` default of 270 seconds, set `STARTUP_TIMEOUT_SECONDS` below that timeout.
* Resuming a run's event stream replays stored events in batches, preventing long replays from stalling Redis for other clients. Replay includes events regardless of how their fields are ordered in storage.
* Tools loaded mid-session, such as those added by Claude Code, are available to models whose providers do not support ordered tool additions instead of being silently ignored. These tools are declared up front, so their availability no longer follows the order of activation within the conversation.
* A labeled **Chat** button in the page header replaces the floating launcher, keeping page content unobstructed. Clicking it opens the conversation and focuses the composer without submitting a suggested prompt.
* The Coding Agent overview shows cost alongside thread counts and cost per thread alongside turns per thread, using a separate dollar axis. Cost per thread is omitted when filtering by model, and cost lines are omitted when splitting charts by a grouping.
* CLI profiles can store API keys in the OS keychain using `profile create --keychain` or `LANGSMITH_SECRET_STORE=keychain`, falling back to file storage with a warning if the keychain is unavailable. The Go SDK supports keychain-backed profiles, while other SDKs report a clear error when reading them.
* Sandbox browsers load only the highest version of each extension name, and loading extensions restarts Chrome when an existing extension is removed or superseded. These restarts preserve logins but close open tabs and drop connections, while adding extensions without replacing existing ones remains non-disruptive.
* Custom code evaluator rules fail immediately and record an error when a batch contains run data that cannot be JSON-encoded, rather than retrying for about 25 minutes. The affected batch is still dropped.
* The **Get started** checklist's **Add alert** action reopens the create-alert pane after you close it, rather than doing nothing on subsequent clicks.
* Thread updates retry brief lock timeouts and reduce lock contention for threads with large state, making concurrent updates less likely to fail with HTTP 500 errors.
* Thread listings with custom authentication are faster when metadata equality filters match indexed fields. Updating thread TTL settings also works correctly when an authentication filter is applied.
* Organization and workspace **Members** tables provide an explicit **Edit** action beside **Delete**. Workspace **Members** also explains why Organization Admin access cannot be changed there, and organization member actions remain visible at laptop screen widths.
* User-authenticated requests can send `X-LangSmith-Team-Tags: true` to tag runs with `ls_team:<team id>` for each of the sender's teams with workspace access, enabling usage grouping by team. Team attribution reflects membership when the run is sent, and client-supplied `ls_team:` tags are removed to prevent spoofing.
* Pages account for global banners when sizing their content, preventing unnecessary scrolling and keeping the pinned **Next** button in annotation queues visible.
* The project stats sidebar no longer shows **% Streaming**, which measures the share of completed traces that stream tokens rather than project health. The metric remains available through the API and dashboards.
* Offline usage backfills for air-gapped installations emit Standard Units events alongside legacy events. Backfills also accept multiple CSV export parts in one run without overwriting per-customer output.
* Run statistics requests that time out return HTTP 504 instead of HTTP 500, distinguishing timeouts from internal errors.
* Annotation queues prompt before you leave, reload, or close the tab with unsaved custom view changes, helping prevent accidental loss of drafts. Moving between items in the same queue does not trigger a prompt.
* The coding work-type breakdown groups investigative threads under **Investigation** instead of **Question Answering**. Automations that check something and report back are classified as investigations rather than off topic, even when no follow-up action is needed.
* Code evaluators can read and create feedback using their credentials, while feedback permission checks remain enforced. Feedback API responses return the public schema with nullable defaults, omit create-only fields and caller-supplied source identities, and preserve large integers in source metadata.
* The Python and TypeScript SDKs support managing Prompt Hub repositories, directories, and commits, including synchronous and asynchronous access in Python.
* Prompt repository updates return the same response type as repository fetches in the Go and Java SDKs. The API's JSON response remains unchanged.
* Issue detection splits trace retrieval requests into smaller batches after an HTTP 504 timeout instead of falling back to data the detectors cannot read. This prevents missing issue-detection results.
* Repeated project writes with inherited dataset tags no longer fail because of duplicate tag assignments.
* Self-hosted model credential resolution requires a nonempty per-run license JWT and no longer falls back to deployment gateway or tracing keys when the JWT is missing or empty. Customer-provided model routing remains unchanged.
* You can create or upsert projects through `POST /api/v2/sessions`, which returns the stored project with HTTP 201 for creation or HTTP 200 for updates. Upserting an existing project requires both read and update access, including attribute-based permissions, while creating a new project requires only creation permission.
* Press Escape while focused inside floating Chat to close it, while embedded Chat stays open. Nested pickers, message editing, and image previews handle Escape first, and Escape during IME composition preserves Chat and its draft.
* The `/mcp` endpoint accepts web login bearer tokens with `X-Tenant-Id`, allowing tool calls to run with the signed-in user's workspace permissions. Logins that rely on session cookies remain unsupported.
* Custom chart definitions migrate only when ClickHouse queries are disabled or `CUSTOM_CHART_SERIES_DEFINITIONS_BACKFILL_ENABLED=true`, preventing empty dashboards when switching back to ClickHouse. To opt in while ClickHouse queries remain enabled, set `CUSTOM_CHART_SERIES_DEFINITIONS_BACKFILL_ENABLED=true`.
* A2A requests with `A2A-Version: 1.0` receive v1.0 JSON-RPC and SSE response formats, including wrapped stream events and `toolResults` envelopes. Requests without the header or using version 0.3 retain their existing format, while unsupported versions return error `-32009`.
* You can play Trace Flight, a hidden arcade game on the chat page, with a seasonal leaderboard shared across your installation and a ghost of your best run to race against.
* Dataset examples load automatically in batches of 50 as you scroll, replacing page controls. Wide example tables support horizontal scrolling, and column headers remain visible during vertical scrolling.
* Project updates through `PATCH /api/v2/sessions/{session_id}` are transactional and enforce project-level access controls, dataset ownership, and trace-tier permissions. Updates preserve omitted fields and metadata numeric precision, support metadata merging, nullable-field clearing, and project-specific retention overrides, and prevent renaming projects linked to a deployment.
* Sandbox proxies support opt-in static or callback-provided attribution headers on proxy-handled HTTP(S) requests, and callback host lists are optional in API responses and the Java SDK. Before configuring attribution, deploy compatible sandbox hosts throughout the deployment and ensure consumers handle missing callback host lists.
* Run updates and completions preserve their computed status when error details or metadata are offloaded, preventing incorrect run status classification.
* The Python SDK requires Python 3.11 or later. If you use Python 3.10, upgrade your interpreter before updating the SDK.
* Deprecated API notices show the LangSmith release that removes each endpoint and the version your instance runs, rather than a Cloud removal date. Notices cover all detected deprecated endpoints, including those with distant removal dates, and link to migration guidance.
* Size `redis.deployment.resources.limits.memory` for Redis's new 75% memory cap (3Gi with the default 4Gi limit) and `noeviction` policy, which rejects writes when Redis is full instead of evicting keys. Omitting the memory limit leaves Redis uncapped, and custom container arguments remain unchanged.

**Download the Helm chart:** [`langsmith-0.18.0-rc.72.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.18.0-rc.72/langsmith-0.18.0-rc.72.tgz)

**Sandbox runtime chart, for Sandboxes in a separate cluster:** [`langsmith-sandbox-0.18.0-rc.7.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-sandbox-0.18.0-rc.7/langsmith-sandbox-0.18.0-rc.7.tgz)

**2026-11-11**

## langsmith-0.18.0-rc.71

**LangSmith version:** `0.18.25rc1`

* This release packages the same LangSmith application version as langsmith-0.18.0-rc.67. Refer to the [langsmith-0.18.0-rc.67](#langsmith-0-18-0-rc-67) release notes below for application changes.
* `config.superAdmins` sets instance admins via `INSTANCE_ADMIN_EMAILS` as well as usage-export admins. With the organization's installation operations permission, these users can view instance health, restart backfills, and create organizations even when organization creation is disabled.

**Download the Helm chart:** [`langsmith-0.18.0-rc.71.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.18.0-rc.71/langsmith-0.18.0-rc.71.tgz)

**Sandbox runtime chart, for Sandboxes in a separate cluster:** [`langsmith-sandbox-0.18.0-rc.6.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-sandbox-0.18.0-rc.6/langsmith-sandbox-0.18.0-rc.6.tgz)

**2026-11-11**

## langsmith-0.18.0-rc.70

**LangSmith version:** `0.18.25rc1`

* This release packages the same LangSmith application version as langsmith-0.18.0-rc.67. Refer to the [langsmith-0.18.0-rc.67](#langsmith-0-18-0-rc-67) release notes below for application changes.
* Requests to `/api/v1/workspaces/current/legacy-api-usage` route to the platform backend with or without a configured base path, avoiding backend 404 responses.

**Download the Helm chart:** [`langsmith-0.18.0-rc.70.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.18.0-rc.70/langsmith-0.18.0-rc.70.tgz)

**Sandbox runtime chart, for Sandboxes in a separate cluster:** [`langsmith-sandbox-0.18.0-rc.6.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-sandbox-0.18.0-rc.6/langsmith-sandbox-0.18.0-rc.6.tgz)

**2026-11-11**

## langsmith-0.17.51

**LangSmith version:** `0.17.74`

* Self-hosted agent images use Agent Server 0.15.13 with patched npm tooling and Datadog initialization binaries.

**Download the Helm chart:** [`langsmith-0.17.51.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.51/langsmith-0.17.51.tgz)

**2026-11-10**

## langsmith-0.18.0-rc.69

**LangSmith version:** `0.18.25rc1`

* This release packages the same LangSmith application version as langsmith-0.18.0-rc.67. Refer to the [langsmith-0.18.0-rc.67](#langsmith-0-18-0-rc-67) release notes below for application changes.
* Scale-to-zero LGPs support `autoscaling.httpScaling`, `multiTenancy`, and `serverSpec` fields for the `core-api` sidecar and inline queue. The bundled CRD accepts and preserves these fields, and existing LGPs remain valid.

**Download the Helm chart:** [`langsmith-0.18.0-rc.69.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.18.0-rc.69/langsmith-0.18.0-rc.69.tgz)

**Sandbox runtime chart, for Sandboxes in a separate cluster:** [`langsmith-sandbox-0.18.0-rc.6.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-sandbox-0.18.0-rc.6/langsmith-sandbox-0.18.0-rc.6.tgz)

**2026-11-10**

## langsmith-0.18.0-rc.68

**LangSmith version:** `0.18.25rc1`

* This release packages the same LangSmith application version as langsmith-0.18.0-rc.67. Refer to the [langsmith-0.18.0-rc.67](#langsmith-0-18-0-rc-67) release notes below for application changes.
* Workspace usage-limit `GET` requests route directly to Go by default. Writes and organization routes remain on Python.

**Download the Helm chart:** [`langsmith-0.18.0-rc.68.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.18.0-rc.68/langsmith-0.18.0-rc.68.tgz)

**Sandbox runtime chart, for Sandboxes in a separate cluster:** [`langsmith-sandbox-0.18.0-rc.6.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-sandbox-0.18.0-rc.6/langsmith-sandbox-0.18.0-rc.6.tgz)

**2026-11-10**

## langsmith-0.18.0-rc.67

**LangSmith version:** `0.18.25rc1`

* The project statistics pane displays loading placeholders while run and feedback statistics load.

* Model selectors exclude managed gateway models on data planes without access to them, preventing calls that fail with HTTP 403 errors. Gateway routing with your own provider keys remains available.

* Generating a pull request from a draft goal allows the requested tracking changes instead of rejecting them as out of scope. When no change is produced, the goal page shows the reason when available and offers a retry.

* Deployment metrics charts and summaries default to a full rolling hour when no start time is specified, rather than the time since the start of the current UTC hour. Explicit time bounds remain unchanged.

* Usage exports exclude skipped rows and rows with no node or run usage from the nodes CSV, reducing export size and improving export speed for self-hosted deployments.

* Scans continue when pull-request monitoring or issue APIs encounter transport failures, reporting tool errors instead of aborting. Safe retries help recover from transient failures without automatically replaying issue creation when the outcome is uncertain.

* Workspace admins can lock and unlock agents and list other members' private agents with their lock states on self-hosted installations without configuring `FLEET_ADMIN_SERVICE_KEY`.

* Insights retains run threads for two hours to prevent them from being deleted while a run is still in progress.

* The Stats sidebar in a single trace's trajectory view displays previously missing feedback.

* Engine boards offer a setup checklist for repository connections, Slack notifications, automatic pull requests, coding-agent handoffs, preview verification, and Linear sync. The checklist includes only features available in your deployment and hides when all steps are complete.

* Automated trace scans recover latency and baseline samples when trace queries exceed memory limits, reducing failed or undersized scans on high-volume projects. Recovered samples omit unavailable trace-level token and cost totals rather than reporting incorrect values.

* You can filter threads by creation time in `POST /threads/search` and `POST /threads/count` using the optional `created_after` (inclusive) and `created_before` (exclusive) parameters. Both accept ISO 8601 timestamps, treat timestamps without a timezone as UTC, and return HTTP 422 for invalid values.

* Users in BYOC workspaces can access the Tools page when their data plane supports Tool Gateway. On data planes that do not report support, the page remains hidden and direct links redirect.

* Taskset runs wait for available workspace sandbox quota instead of failing after repeated attempts to create a runner sandbox. If quota remains full for the 30-minute preparation limit, the run fails with `runner_sandbox_quota_exceeded`.

* Taskset trials wait for sandbox capacity instead of failing when the workspace's sandbox quota is full. The wait lasts up to 10 minutes and counts toward the environment startup timeout.

* Filter suggestions in run details use the time range around the trace instead of a 400-day window. Thread and experiment views use the time range across their root runs, with thread views accounting for turns beyond the loaded pages.

* Self-hosted installations that report both Playground and workload AWS role principals offer IAM role authentication for Amazon Bedrock in provider secrets, evaluator secrets, and the Playground. The setup instructions provide a trust policy for both roles, including session tagging and the required `LangSmithBedrock=true` tag.

* The onboarding checklist's Add alert task opens the create-alert pane with the project preselected, including when you are already on the alerts page.

* Reconnecting a Slack workspace through a different Slack app notifies the installer and posts a handoff notice in private channels that need the new bot. Members must invite the new bot to those private channels before it can deliver alerts there.

* The `GET /v1/platform/slack/installations/app-status` endpoint reports which linked Slack workspaces need the app reinstalled, and organization Slack settings show an "Update available" badge and a Reinstall button for workspaces connected to an older Slack app. Reinstall opens Slack authorization with the workspace preselected, and Slack authorization accepts an optional `team_id` to preselect a workspace during installation.

* Prometheus scrapes exclude auxiliary `*_created` timestamp series from Python metrics. Counter values and histogram and summary measurements remain unchanged.

* The API specification and Go/Java SDKs represent commit `manifest_sha` values as base64 strings to prevent response decoding failures, and commit creation marks `manifest` as required to match existing server validation. SDK users must update code that expects an integer array.

* Registered MCP server routes reject JSON-RPC batches with HTTP 400 and `jsonrpc_batch_unsupported`, preventing batches from bypassing per-tool deny and approval policies. Clients must send one message per request.

* For agents with multiple environments, the evaluator editor preselects Production, or the most production-like environment available, as its source. Sample traces and evaluator testing are available without manually selecting a source.

* Agent deployment settings state that workload identity requires `langgraph-api` version `0.19.0dev6` or later.

* Fixed security vulnerabilities. See CVE-2026-111497 for details.

**Download the Helm chart:** [`langsmith-0.18.0-rc.67.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.18.0-rc.67/langsmith-0.18.0-rc.67.tgz)

**Sandbox runtime chart, for Sandboxes in a separate cluster:** [`langsmith-sandbox-0.18.0-rc.6.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-sandbox-0.18.0-rc.6/langsmith-sandbox-0.18.0-rc.6.tgz)

**2026-11-10**

## langsmith-0.17.50

**LangSmith version:** `0.17.73`

* Opening a tracing project checks for a single recent run to decide whether to show the tracing quickstart, instead of counting all runs in the project over the last 30 days.
* Filter queries hide errors for a trailing `AND` or `OR` while you type after the operator. The error returns when you leave the filter bar or move the cursor before the operator.

**Download the Helm chart:** [`langsmith-0.17.50.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.50/langsmith-0.17.50.tgz)

**2026-11-09**

## langsmith-0.18.0-rc.66

**LangSmith version:** `0.18.22rc1`

* This release packages the same LangSmith application version as langsmith-0.18.0-rc.63. Refer to the [langsmith-0.18.0-rc.63](#langsmith-0-18-0-rc-63) release notes below for application changes.
* The Fleet runtime, tool server, and trigger server can route HTTPS egress through a proxy without affecting the backend. Set `fleet.egressProxy.url` to enable this routing.
* `fleet.egressProxy.url` is stored in a plaintext ConfigMap, and URLs containing credentials fail chart rendering even when validation is skipped. Use a credential-free URL.
* In-cluster services and `config.hostname` bypass the proxy, but CIDR ranges are unsupported. Set `fleet.egressProxy.noProxy` to add hosts or domain suffixes that also bypass the proxy.
* Combine `fleet.egressProxy.url` with `config.customCa` to use the custom CA bundle for Fleet proxy requests through `requests` and `httplib2`.

**Download the Helm chart:** [`langsmith-0.18.0-rc.66.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.18.0-rc.66/langsmith-0.18.0-rc.66.tgz)

**Sandbox runtime chart, for Sandboxes in a separate cluster:** [`langsmith-sandbox-0.18.0-rc.5.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-sandbox-0.18.0-rc.5/langsmith-sandbox-0.18.0-rc.5.tgz)

**2026-11-09**

## langsmith-0.18.0-rc.65

**LangSmith version:** `0.18.22rc1`

* This release packages the same LangSmith application version as langsmith-0.18.0-rc.63. Refer to the [langsmith-0.18.0-rc.63](#langsmith-0-18-0-rc-63) release notes below for application changes.
* When `fleet.agentAccessToken.enabled` is enabled, `platformBackend.rbac.create` also grants `platform-backend` permission to read pods, ReplicaSets, and Deployments in the release namespace. Grant these permissions yourself if RBAC creation is disabled.
* Assign distinct service accounts to the two Fleet pods. Chart validation rejects installs and upgrades that share one service account between them.

**Download the Helm chart:** [`langsmith-0.18.0-rc.65.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.18.0-rc.65/langsmith-0.18.0-rc.65.tgz)

**Sandbox runtime chart, for Sandboxes in a separate cluster:** [`langsmith-sandbox-0.18.0-rc.5.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-sandbox-0.18.0-rc.5/langsmith-sandbox-0.18.0-rc.5.tgz)

**2026-11-09**

## langsmith-0.18.0-rc.64

**LangSmith version:** `0.18.22rc1`

* This release packages the same LangSmith application version as langsmith-0.18.0-rc.63. Refer to the [langsmith-0.18.0-rc.63](#langsmith-0-18-0-rc-63) release notes below for application changes.
* Fleet pods support signed, short-lived agent access tokens through `fleet.agentAccessToken.enabled` (default: `false`), with an optional `fleet.agentAccessToken.egressAudience` that defaults to empty. To enable tokens, set `fleet.agentAccessToken.enabled` to `true`, set `config.hostname`, supply an RSA private signing JWKS through `fleet.agentAccessToken.signingJwks`, add `agent_access_token_signing_jwks` to your Secret if using `config.existingSecretName` or `config.disableSecretCreation`, and set `fleet.agentAccessToken.egressAudience` to the audience your egress gateway checks if needed.
* `platformBackend.rbac.create` (default: `true`) creates the ClusterRole and ClusterRoleBinding required when `fleet.agentAccessToken.enabled` is enabled. Set it to `false` if you grant TokenReview creation and service account key read access yourself, and use `platformBackend.rbac.labels` and `platformBackend.rbac.annotations` to customize the platform-backend RBAC resources.

**Download the Helm chart:** [`langsmith-0.18.0-rc.64.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.18.0-rc.64/langsmith-0.18.0-rc.64.tgz)

**Sandbox runtime chart, for Sandboxes in a separate cluster:** [`langsmith-sandbox-0.18.0-rc.5.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-sandbox-0.18.0-rc.5/langsmith-sandbox-0.18.0-rc.5.tgz)

**2026-11-09**

## langsmith-0.18.0-rc.63

**LangSmith version:** `0.18.22rc1`

* Cache hit rates, token breakdowns, dashboards, and filters correctly account for cached and reasoning tokens in new OpenAI priority and flex runs. Costs remain unchanged, and historical runs retain their existing token data.
* Run reads include stored provider-specific token and cost breakdowns, such as `priority` and `priority_cache_read`, when requested, so returned data includes these categories.
* Run ingestion enforces a separate hourly persisted-data limit, including large fields and attachments, defaulting to 100 GB per workspace alongside the existing queued-data limit. Set `ENFORCE_PERSISTED_BYTES_LIMIT=false` to disable the persisted-data limit.
* Workspace-scoped MCP tool calls require an explicit `workspace_id` on every request, including pagination, while organization-scoped calls remain usable without workspace context. Update workspace-scoped calls to provide `workspace_id` instead of relying on the credential's default workspace.
* Graph state, streams, and stored threads preserve literal `\u0000` text instead of replacing it with `\ufffd`. Previously altered data remains unchanged, and actual NUL characters continue to be replaced with the Unicode replacement character (`U+FFFD`).
* Tracing onboarding stays visible until a project's first trace arrives, then refreshes the trace table. Filtered-empty views of populated projects show the normal empty table, and failed trace checks leave the normal project page available.
* JavaScript graph factories receive `configurable.__is_for_execution__` to distinguish runs from state and history reads. Factories can check this value to skip run-only setup during reads.
* Project Online Evaluators lists hide system-generated evaluators whose details cannot be opened. Their usage remains included in spend charts and project and workspace totals.
* New API endpoints let authorized users bind workspace-compatible service keys to Agent environments, list bindings, and remove bindings without revoking the keys. Bindings determine which Agent policies apply to the keys' gateway traffic.
* Self-hosted installations without the LLM Gateway can create decision model evaluators using providers that accept their own API keys, such as OpenAI. Gateway-only options remain hidden on these installations.
* Redirects from an Allowed URLs host to a host that does not qualify for authentication do not forward the injected LLM authentication token, preventing potential exposure of the user's identity provider token.
* New OpenAI LLM-as-a-judge evaluators default to `gpt-6-luna` instead of `gpt-6.1-sol` when no workspace evaluator default is configured. Workspace defaults and the Playground default remain unchanged.
* Writes to `PUT /store/items` that omit `ttl` use the selected store's configured default expiration, including updates to existing items. Explicit `null` still disables expiration, and custom authorization handlers can override the effective default before the write.
* With `LLM_AUTH_PROXY_FORWARD_IDP_TOKEN=true`, authentication JWTs include users' IdP tokens only when the organization has an explicit Allowed URLs list, not "Allow all" or "Block all". To retain IdP token forwarding, replace "Allow all" with an admin-approved Allowed URLs list.
* Polly can identify tools in a tool kit that requires connections to all linked servers, even when some servers are not connected. It also explains that all servers must be connected on the **Tools** page before it can read the tools' input schemas.
* Agent Servers configured with both a license and a LangSmith Cloud API key authenticate with the API key first, falling back to the license if key validation fails. License-first authentication remains unchanged for self-hosted authentication endpoints and when `LANGSMITH_LICENSE_REQUIRED_CLAIMS` is set.
* The API key creation dialog fits mobile screens and stacks service-key role selectors so all fields and actions remain accessible.
* Self-hosted workspaces display the unified Agent Platform interface once migration marks them ready. The existing workspace-level opt-out lets users retain the classic experience.
* Runs configured with `on_disconnect: "cancel"` or `cancel_on_disconnect=true` cancel reliably when clients disconnect before streaming begins, including during custom authentication checks. Failures to open a join stream return an HTTP error status instead of a successful response containing an error event.
* Creating feedback using only a run ID encounters fewer timeouts. Feedback lookups also exclude deleted or expired runs.
* With badge signing keys and issuer settings configured, deployments can exchange deployment API keys for five-minute signed identity tokens at `POST /v1/agent-auth/token`, while personal API keys are rejected. Public discovery and signing-key endpoints let downstream services verify these tokens without contacting the issuer.
* Deleting a thread with no run in progress clears its cached stream events, preventing a new thread with the same ID from replaying them. This also applies to thread deletion through assistant deletion, pruning, or expiration.
* OIDC authorization-code exchange, token refresh, and authenticated UserInfo requests reject redirects to prevent credential forwarding, while discovery redirects remain supported. Ensure self-hosted OIDC token and UserInfo endpoints respond directly without redirecting.
* Self-hosted instance administrators can configure or remove a customer-owned GitHub App for deployments through `/v1/platform/deployments/github-app`. Its configuration is stored separately from other GitHub App integrations.
* Scans retry failed trace queries over a smaller time window and continue with partial results when other queries return traces. Scans still fail when query failures prevent any traces from being retrieved.
* Dynatrace and PagerDuty alert actions require `workspaces:manage-secrets` permission to select workspace secrets, restrict delivery to the secret's configured URL, and block cross-host redirects to prevent secret exposure. Existing alert actions with mismatched secrets and URLs are suspended.
* Redis connections recover automatically after Azure Managed Redis changes shard ports, preventing prolonged request hangs and HTTP 500 errors without requiring a pod restart.
* You can add or remove categorical feedback categories using `add_categories` and `remove_categories` in `PATCH /feedback-configs`, without resending the full category list. Retried edits are idempotent, and changes preserve existing feedback scores while enforcing validation, permissions, and annotation queue compatibility.
* Tool kits that allow partial connections expose tool definitions for unconnected sources in the missing-credential metadata returned by `tools/list`. Agents can discover these tools before users connect their accounts, but calling them still requires authorization.
* `POST /v1/trajectories/query` supports selecting additional per-message metadata and tool definitions, reducing the need to fetch each trajectory separately. Responses replace `has_more_messages` with an optional `messages_cursor`, but resuming from this cursor is not yet supported.
* You can cancel simulation runs with `POST /v1/platform/simulation/threads/{thread_id}/runs/{run_id}/cancel` or LangGraph SDK `client.runs.cancel`. The endpoint supports interrupting or rolling back a run and optionally waiting for its result.
* You can download complete traces containing up to 2,000 runs, up from 1,000, without downloading runs individually.
* Background workers allow running tasks up to 20 seconds, instead of 8 seconds, to finish during shutdown before requeuing unfinished tasks. To adjust this timeout independently of HTTP draining, set `ASYNQ_SHUTDOWN_TIMEOUT_SEC` and ensure the pod termination grace period accommodates it.
* Access policy editing preserves UI and JSON drafts, blocks invalid saves, and stages role changes until **Save changes**, with retries for remaining assignments after partial failures. Policy details remain read-only, and access-control managers can find **Access policies** under **Settings** > **Organization** > **Permissions**.
* Custom apps and annotation queue custom views can use `window.langsmith.openUrl(url)` to open external HTTPS links in a new tab after the viewer confirms a dialog showing the destination site and full URL. External HTTP links, unsupported URL schemes, and malformed URLs are rejected.
* `POST /v2/traces/messages` supports organization-specific rate and burst limits, applied separately to each workspace. Organizations without an override retain the environment-configured defaults.
* Model fallback chains offer grouped status-code triggers with per-code controls. New chains exclude HTTP 409, 501, 505, and 506 as fallback triggers by default, while existing chains retain their saved settings.
* Deleted or revoked tracing keys, service keys, and personal access tokens are rejected even when their authentication details are cached. Credential expiration is checked on every request, preventing cached credentials from remaining valid after they expire.
* Annotation queue CSV exports include all selected categories for multi-select feedback in a single cell, separated by semicolons, instead of showing only one selection. Duplicate selections appear only once.
* The list evaluators API returns HTTP 400 Bad Request instead of HTTP 500 Internal Server Error when the `name_contains` query parameter contains a NUL character.
* Resumable streams do not deliver duplicate events or tokens when a stream publish is retried after a Redis timeout, connection reset, or failover. Resuming a stream also avoids replaying duplicates caused by these retries.
* Deployments with a custom HTTP app use the configured store instead of ignoring it and connecting to the default store.
* LLM-as-a-judge evaluators using Claude Fable 5.1, Claude Opus 5.5, or Claude Sonnet 5.5 through the Anthropic provider support structured output without an unsupported tool-choice error.
* Organization and workspace member settings show active members, pending invitations, and deactivated members together by default, with status and role filters, configurable columns, and CSV exports that respect current filters and sorting. Member rows open an edit dialog, and workspace counts open a searchable workspace list.
* Member invitation and editing dialogs show role documentation, searchable permission previews, and Organization Admins' automatic admin access to all workspaces. Organizations with custom roles can invite members without assigning a workspace, and workspace roles default to Workspace Admin or an unrestricted alternative when that role cannot be assigned.
* New browsers created through `POST /v2/sandboxes/browsers` are automatically deleted after stopping, using the sandbox retention default of 14 days, while existing browsers remain unchanged. Set `delete_after_stop_seconds` to override the delay or to `0` to retain stopped browsers indefinitely.
* The trajectory stats endpoint, `GET /v1/trajectory/{scope_id}/stats`, returns a `tools` list ordered by call count with per-tool call counts and median, 99th-percentile, and maximum latencies in seconds, excluding unfinished runs from latency statistics and returning an empty list when no tool runs exist. It also returns a `turns` list ordered oldest first with per-trace timing, token usage, costs, error previews, and tool and LLM run counts, or an empty list when the database does not yet provide turn data.
* Agent Overview recommends the PII Leakage evaluator template instead of Correctness. When the Decision Model Evaluator is unavailable, PII Leakage appears only once in the recommendations.
* Simulations parse the updated Garden verification format, including verification parts and reply checks, so verifier details and expected answers display correctly. The verifier table shows human-readable names instead of IDs, and the legacy verification format is no longer supported.
* Runs ignore the unsupported `fairness_weight` field returned by a priority callback instead of failing with a 500 error. The `priority` and `fairness_group` fields still apply.
* Agent-controlled browser windows support Stagehand 4.4 connections without the "Stagehand client disconnected during registration" error. Browser clients such as browser-use can also auto-attach to their window's own hidden targets without being unexpectedly detached.
* Custom apps can export files such as CSV, JSON, XLSX, and PDF through LangSmith, with viewer confirmation before each download. Downloads support files up to 50 MB, sanitize filenames, and block executable and other potentially unsafe file extensions.
* To use persistent storage without changing lifecycle cleanup, set `ENGINE_DISPOSABLE_SANDBOXES=false`, as sandboxes remain disposable by default. Set `ENGINE_SANDBOX_FS_CAPACITY_BYTES` to a positive byte count to customize sandbox filesystem capacity, or leave it unset to retain the snapshot default.
* Deployment metrics requests require a minimum interval of 60 seconds for `step` and `step_seconds`, including on the deprecated v1 endpoint. Requests with smaller values return HTTP 400 for `step` or HTTP 422 for `step_seconds` instead of being silently clamped.
* Runs can send traces to an agent environment using `langsmith_tracer.address` instead of `project_name`, or use the deployment's agent tracing settings as the default destination. The `/info` endpoint reports whether the installed SDK supports agent addressing, and project tracing remains unchanged.
* Vertex AI requests using the `us` or `eu` multi-region locations use the correct endpoints, preventing invalid-hostname errors in online evaluators and other model requests.
* Run and thread streams disconnect when Redis interrupts event delivery or a client stalls, allowing SDKs to reconnect instead of incorrectly reporting a failed run or silently losing events. Runs created with `stream_resumable=True` replay missed events, while apps using custom `BaseHTTPMiddleware` continue to receive an error event instead of reconnecting automatically.
* Thread state endpoints accept `select` to return specific fields or state keys, such as `values.messages`. On PostgreSQL-backed deployments, selective reads can also avoid loading unrequested state, reducing read overhead for large threads.
* Terraform-managed workspaces can target a specific BYOC data plane using the optional `data_plane_id` setting. Imports and refreshes preserve workspace metadata when data-plane discovery is forbidden, while mutations are blocked until routing can be resolved.
* You can retrieve session dashboard data through `sessions.dashboard` in the Python and TypeScript SDKs. This read-only operation creates no resources.
* Safari and Firefox automatically reload when a stale browser tab fails to load a page after an update. The reload safeguard expires after 30 seconds, allowing tabs to recover again after later updates.
* Automation rule scheduling retries temporary Redis connection failures, including closed connections, up to five times to reduce delayed rule execution.
* Joining a run's stream without a `Last-Event-ID` returns HTTP 404 before streaming if the run is missing, belongs to another thread, or is hidden by authorization, instead of returning HTTP 200 with an error event. Resuming with `Last-Event-ID` retains the existing replay behavior.
* Single-run reads support omitted or blank start times when trace-level permissions apply, for both JSON and streaming responses. Missing timestamps do not cause a fallback or a 501 error, while project authorization and field restrictions remain enforced.
* A2A `message/send` and `message/stream` report tasks canceled mid-run as canceled, rather than failed or completed, without cancellation error messages.
* Run and thread streams emit a `gap` event with `reason: too_large` and the dropped event's `mode` when a payload exceeds `MAX_STREAM_CHUNK_SIZE_BYTES` (28 MB by default). Clients can detect missing events instead of silently receiving incomplete streams.
* You can create, update, delete, import, and look up registered agents with the Terraform provider. Agent resources expose environment and tracing-project IDs for dependent resources, with environment references remaining stable during updates.
* The LLM Gateway supports DeepSeek chat completions at `POST /deepseek/v1/chat/completions` using the workspace `DEEPSEEK_API_KEY` secret, with usage and spend tracking. For organizations with an existing Model Access policy, add `deepseek` to allow requests.
* Single-experiment and comparison tables offer Default (340px), Tall (600px), and Fit (unlimited) row heights for inputs, outputs, metadata, and attachments. The preference is saved locally and included in shared URLs, while compact mode remains available.
* Clicking an ID badge copies the ID to the clipboard.
* Clearer Insights copy focuses on understanding how people use your agent.
* OpenTelemetry ingestion enforces per-project monthly trace limits on `/otel/v1/traces` and `/otel/v1/claude_code`, returning HTTP 429 if any span's project exceeds its limit. Enforcement takes effect immediately for projects already over their limit, while gateway metadata-only spans remain exempt.
* Metadata filters generated from run details, highlighted text, shortcuts, and autocomplete use correct quoting and escaping for keys with special characters. Autocomplete also preserves surrounding filters, negation, and existing values when inserting or replacing metadata keys.
* Database migrations use a new migration runner by default. Set `DB_MIGRATION_BY_CORE_API=false` to temporarily restore the previous migration behavior if needed.
* Agent identities can own credentials, complete authorization sessions, and refresh tokens. Deleting an agent environment automatically deletes its associated credentials.
* You can send Groq chat completions through `POST /groq/v1/chat/completions` using the workspace `GROQ_API_KEY` secret, with streaming, usage tracking, and cost tracking. For organizations with an existing Model Access policy, add `groq` to allow requests through this route.
* Admins can use the custom role editor to add missing workspace read or organization metadata read permissions to roles created through the API or Terraform. This resolves permission-related page failures, such as Annotation Queues showing "Not authorized to resolve identity information," without updating roles through the API.
* Workspace admins can use the existing server APIs to view an agent environment's tool connection status, authorize OAuth connections, and store or delete its secrets. These actions require the appropriate workspace credential permissions and permissions on the environment's tracing project.
* The LLM Gateway supports Mistral chat completions at `POST /mistral/v1/chat/completions` using the workspace `MISTRAL_API_KEY` secret, including streaming, tool calls, and token and cost tracking. For organizations with an existing Model Access policy, add `mistral` to allow access.
* Managed tool calls made with an API key bound to an agent's environment use that agent's admin-connected credentials when the key has credential-use permission. Missing credentials return HTTP 409 without a connection link, and API key binding lookup failures return HTTP 503 rather than falling back to other credentials.
* Ingestion workers process runs with multiple inputs, outputs, or attachments stored in S3 without crashing from concurrent access.
* Slack channels can opt in to receive message edit and deletion events, allowing deployments to respond when messages change or are removed. Existing channels keep their current behavior unless event forwarding is explicitly configured.
* Channel action API responses include structured Slack error details, including the error code, message, and required scope when available, making failed posts and reactions easier to diagnose.
* OpenAI traces capture the response model, allowing pricing and spend-cap accounting when the request model is unavailable. Run metadata shows the model reported by the response, which may be a dated snapshot name rather than the requested alias.
* Custom apps support shareable URL views, refresh and rebuild persistence, route updates without reloading, browser Back/Forward navigation, and local deep-link testing with `langsmith apps dev`. Polly and new browser-created custom-app templates include guidance for shareable page links, Back/Forward support, and safe route handling.
* Dashboard charts support v2 filters with the same meaning as their matching-run links. Ratio charts validate the combined series and operand filters when saving, rejecting invalid combinations and mixed legacy/v2 syntax.
* Studio displays browser handoff and async subagent notifications as automated messages when agents send the newer notification format. Browser handoff cards clear when the handoff ends, while older notification formats remain supported.
* Custom-code evaluators load prior feedback more efficiently for runs with large feedback histories while preserving the existing limit of the newest 100 feedback entries per batch.
* The Python and TypeScript SDKs support deleting projects with `client.sessions.delete(project_id)`, matching the existing Go and Java SDK support.
* The Python and TypeScript SDKs support retrieving a project by ID with `client.sessions.retrieve(project_id, ...)`, using the existing `GET /api/v1/sessions/{session_id}` endpoint.
* On self-hosted data planes that support GitHub sources, you can create deployments from GitHub repositories, rebuild automatically on push, and view build logs. Organization administrators can configure the required GitHub App connection from the deployment form.

**Download the Helm chart:** [`langsmith-0.18.0-rc.63.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.18.0-rc.63/langsmith-0.18.0-rc.63.tgz)

**Sandbox runtime chart, for Sandboxes in a separate cluster:** [`langsmith-sandbox-0.18.0-rc.5.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-sandbox-0.18.0-rc.5/langsmith-sandbox-0.18.0-rc.5.tgz)

**2026-11-09**

## langsmith-0.17.49

**LangSmith version:** `0.17.72`

* Prompt webhook payloads send `created_at` as an RFC 3339 UTC timestamp for tag and commit events, so strict parsers accept every delivery.

**Download the Helm chart:** [`langsmith-0.17.49.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.49/langsmith-0.17.49.tgz)

**2026-11-07**

## langsmith-0.18.0-rc.62

**LangSmith version:** `0.18.20rc1`

* This release packages the same LangSmith application version as langsmith-0.18.0-rc.54. Refer to the [langsmith-0.18.0-rc.54](#langsmith-0-18-0-rc-54) release notes below for application changes.
* Set `managedTools.enabled` (default: `false`) to enable Tool Gateway in the platform backend without deploying an extra service. All organizations receive Tool Gateway access, the frontend routes `managed-tools` and `agent-policies` requests to the backend, and built-in tools use the Fleet tool server when deployed.

**Download the Helm chart:** [`langsmith-0.18.0-rc.62.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.18.0-rc.62/langsmith-0.18.0-rc.62.tgz)

**Sandbox runtime chart, for Sandboxes in a separate cluster:** [`langsmith-sandbox-0.18.0-rc.4.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-sandbox-0.18.0-rc.4/langsmith-sandbox-0.18.0-rc.4.tgz)

**2026-11-06**

## langsmith-0.18.0-rc.61

**LangSmith version:** `0.18.20rc1`

* This release packages the same LangSmith application version as langsmith-0.18.0-rc.54. Refer to the [langsmith-0.18.0-rc.54](#langsmith-0-18-0-rc-54) release notes below for application changes.
* Blobs under the `ttl_<N>d/` prefixes specified by `config.ttl.longlivedAllowedDays` never expire without lifecycle rules. Create a blob-storage lifecycle rule for each prefix.

**Download the Helm chart:** [`langsmith-0.18.0-rc.61.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.18.0-rc.61/langsmith-0.18.0-rc.61.tgz)

**Sandbox runtime chart, for Sandboxes in a separate cluster:** [`langsmith-sandbox-0.18.0-rc.4.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-sandbox-0.18.0-rc.4/langsmith-sandbox-0.18.0-rc.4.tgz)

**2026-11-06**

## langsmith-0.17.48

**LangSmith version:** `0.17.70`

* Internal improvements and maintenance updates

**Download the Helm chart:** [`langsmith-0.17.48.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.48/langsmith-0.17.48.tgz)

**2026-11-06**

## langsmith-0.18.0-rc.60

**LangSmith version:** `0.18.20rc1`

* This release packages the same LangSmith application version as langsmith-0.18.0-rc.54. Refer to the [langsmith-0.18.0-rc.54](#langsmith-0-18-0-rc-54) release notes below.

**Download the Helm chart:** [`langsmith-0.18.0-rc.60.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.18.0-rc.60/langsmith-0.18.0-rc.60.tgz)

**Sandbox runtime chart, for Sandboxes in a separate cluster:** [`langsmith-sandbox-0.18.0-rc.4.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-sandbox-0.18.0-rc.4/langsmith-sandbox-0.18.0-rc.4.tgz)

**2026-11-06**

## langsmith-0.17.47

**LangSmith version:** `0.17.69`

* This release packages the same LangSmith application version as langsmith-0.17.45. Refer to the [langsmith-0.17.45](#langsmith-0-17-45) release notes below.

**Download the Helm chart:** [`langsmith-0.17.47.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.47/langsmith-0.17.47.tgz)

**2026-11-06**

## langsmith-0.17.46

**LangSmith version:** `0.17.69`

* This release packages the same LangSmith application version as langsmith-0.17.45. Refer to the [langsmith-0.17.45](#langsmith-0-17-45) release notes below.

**Download the Helm chart:** [`langsmith-0.17.46.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.46/langsmith-0.17.46.tgz)

**2026-11-06**

## langsmith-0.17.45

**LangSmith version:** `0.17.69`

* Internal improvements and maintenance updates

**Download the Helm chart:** [`langsmith-0.17.45.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.45/langsmith-0.17.45.tgz)

**2026-11-06**

## langsmith-0.18.0-rc.59

**LangSmith version:** `0.18.20rc1`

* This release packages the same LangSmith application version as langsmith-0.18.0-rc.54. Refer to the [langsmith-0.18.0-rc.54](#langsmith-0-18-0-rc-54) release notes below.

**Download the Helm chart:** [`langsmith-0.18.0-rc.59.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.18.0-rc.59/langsmith-0.18.0-rc.59.tgz)

**Sandbox runtime chart, for Sandboxes in a separate cluster:** [`langsmith-sandbox-0.18.0-rc.4.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-sandbox-0.18.0-rc.4/langsmith-sandbox-0.18.0-rc.4.tgz)

**2026-11-06**

## langsmith-0.17.44

**LangSmith version:** `0.17.68`

* This release packages the same LangSmith application version as langsmith-0.17.43. Refer to the [langsmith-0.17.43](#langsmith-0-17-43) release notes below.

**Download the Helm chart:** [`langsmith-0.17.44.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.44/langsmith-0.17.44.tgz)

**2026-11-06**

## langsmith-0.17.43

**LangSmith version:** `0.17.68`

* Internal improvements and maintenance updates

**Download the Helm chart:** [`langsmith-0.17.43.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.43/langsmith-0.17.43.tgz)

**2026-11-06**

## langsmith-0.18.0-rc.58

**LangSmith version:** `0.18.20rc1`

* This release packages the same LangSmith application version as langsmith-0.18.0-rc.54. Refer to the [langsmith-0.18.0-rc.54](#langsmith-0-18-0-rc-54) release notes below.

**Download the Helm chart:** [`langsmith-0.18.0-rc.58.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.18.0-rc.58/langsmith-0.18.0-rc.58.tgz)

**Sandbox runtime chart, for Sandboxes in a separate cluster:** [`langsmith-sandbox-0.18.0-rc.4.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-sandbox-0.18.0-rc.4/langsmith-sandbox-0.18.0-rc.4.tgz)

**2026-11-05**

## langsmith-0.17.42

**LangSmith version:** `0.17.67`

* This release packages the same LangSmith application version as langsmith-0.17.41. Refer to the [langsmith-0.17.41](#langsmith-0-17-41) release notes below.

**Download the Helm chart:** [`langsmith-0.17.42.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.42/langsmith-0.17.42.tgz)

**2026-11-05**

## langsmith-0.17.41

**LangSmith version:** `0.17.67`

* Internal improvements and maintenance updates

**Download the Helm chart:** [`langsmith-0.17.41.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.41/langsmith-0.17.41.tgz)

**2026-11-03**

## langsmith-0.16.50

**LangSmith version:** `0.16.77`

* Sub-agent editors show the root agent model when no override is set. You can clear an explicit override to restore inheritance.

**Download the Helm chart:** [`langsmith-0.16.50.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.16.50/langsmith-0.16.50.tgz)

**2026-11-03**

## langsmith-0.17.40

**LangSmith version:** `0.17.66`

* Internal improvements and maintenance updates

**Download the Helm chart:** [`langsmith-0.17.40.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.40/langsmith-0.17.40.tgz)

**2026-11-03**

## langsmith-0.16.49

**LangSmith version:** `0.16.75`

* This release packages the same LangSmith application version as langsmith-0.16.47. Refer to the [langsmith-0.16.47](#langsmith-0-16-47) release notes below for application changes.
* The operator exits at startup if the LGP CRD is missing. Install the LGP CRD before starting or upgrading the operator.

**Download the Helm chart:** [`langsmith-0.16.49.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.16.49/langsmith-0.16.49.tgz)

**2026-11-03**

## langsmith-0.17.39

**LangSmith version:** `0.17.65`

* This release packages the same LangSmith application version as langsmith-0.17.38. Refer to the [langsmith-0.17.38](#langsmith-0-17-38) release notes below for application changes.
* The chart's updated operator RBAC grants the operator its required permissions. Apply it when installing or upgrading.

**Download the Helm chart:** [`langsmith-0.17.39.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.39/langsmith-0.17.39.tgz)

**2026-11-03**

## langsmith-0.17.38

**LangSmith version:** `0.17.65`

* Setting `GO_INGESTION_PARTITIONS_SLOT_SPREAD=true` names ingestion queue partitions so they spread evenly across Redis Cluster shards when you run more than 4 partitions. Enable it while `GO_INGESTION_QUEUE_PARTITIONS` and `GO_INGESTION_WORKER_PARTITIONS` are both 4 or fewer, then raise worker partitions before queue partitions.

**Download the Helm chart:** [`langsmith-0.17.38.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.38/langsmith-0.17.38.tgz)

**2026-11-03**

## langsmith-0.18.0-rc.57

**LangSmith version:** `0.18.20rc1`

* This release packages the same LangSmith application version as langsmith-0.18.0-rc.54. Refer to the [langsmith-0.18.0-rc.54](#langsmith-0-18-0-rc-54) release notes below for application changes.
* `config.agentMigration.enabled` defaults to `true`, so existing ingest queue workers migrate existing tracing projects and experiments to Agent Platform agents after an upgrade unless `authType` is set to `none`. Do not downgrade to an app version that predates the migration once it runs.

**Download the Helm chart:** [`langsmith-0.18.0-rc.57.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.18.0-rc.57/langsmith-0.18.0-rc.57.tgz)

**Sandbox runtime chart, for Sandboxes in a separate cluster:** [`langsmith-sandbox-0.18.0-rc.4.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-sandbox-0.18.0-rc.4/langsmith-sandbox-0.18.0-rc.4.tgz)

**2026-11-03**

## langsmith-0.17.37

**LangSmith version:** `0.17.64`

* Sub-agent editors show the root agent model when no override is set. Clear an override to use the root model again.
* LangSmith Python service images install `ddtrace` 4.15.6, which fixes CVE-2026-116588 and CVE-2026-116589.

**Download the Helm chart:** [`langsmith-0.17.37.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.37/langsmith-0.17.37.tgz)

**2026-11-03**

## langsmith-0.18.0-rc.56

**LangSmith version:** `0.18.20rc1`

* This release packages the same LangSmith application version as langsmith-0.18.0-rc.54. Refer to the [langsmith-0.18.0-rc.54](#langsmith-0-18-0-rc-54) release notes below for application changes.
* Frontend requests to `/api/v1/agents`, `/api/v1/agent-environments`, and `/api/v1/sessions/resolutions` route to the platform backend instead of the Python backend, avoiding routing-related 404s.

**Download the Helm chart:** [`langsmith-0.18.0-rc.56.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.18.0-rc.56/langsmith-0.18.0-rc.56.tgz)

**Sandbox runtime chart, for Sandboxes in a separate cluster:** [`langsmith-sandbox-0.18.0-rc.4.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-sandbox-0.18.0-rc.4/langsmith-sandbox-0.18.0-rc.4.tgz)

**2026-11-02**

## langsmith-0.18.0-rc.55

**LangSmith version:** `0.18.20rc1`

* This release packages the same LangSmith application version as langsmith-0.18.0-rc.54. Refer to the [langsmith-0.18.0-rc.54](#langsmith-0-18-0-rc-54) release notes below for application changes.
* Opt in to extra ServiceAccount and SecretProviderClass manifests with `config.deployment.extraManifestsEnabled` (default: `false`). This requires a running operator, coordinated supporting images, and the LGP CRD.

**Download the Helm chart:** [`langsmith-0.18.0-rc.55.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.18.0-rc.55/langsmith-0.18.0-rc.55.tgz)

**Sandbox runtime chart, for Sandboxes in a separate cluster:** [`langsmith-sandbox-0.18.0-rc.4.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-sandbox-0.18.0-rc.4/langsmith-sandbox-0.18.0-rc.4.tgz)

**2026-11-02**

## langsmith-0.18.0-rc.54

**LangSmith version:** `0.18.20rc1`

* Joining a run stream returns all requested modes when multiple `stream_mode` query parameters are supplied, preventing missing modes with the Python SDK and JavaScript SDK 1.12+. The JSON-array format used by older JavaScript SDKs remains supported.
* Sandbox storage totals, tables, and charts retain recorded measurements across sampling gaps and flag excluded intervals, while entirely unmeasured resources remain unavailable and unmeasured days remain chart gaps. Usage requests may temporarily report that summaries are initializing while historical summaries are rebuilt.
* Thread search filters preserve your latest edits during updates, preventing the query from briefly reverting and the cursor from jumping backward. Explicit clears and resets continue to work.
* OpenTelemetry spans with exception events appear as errors even when the events lack a message or stack trace. Spans with an `ERROR` status and no exception events retain their error status and available diagnostics.
* You can remove selected workspaces from their chips when creating a service key, using the mouse or keyboard without opening the workspace picker or submitting the form. Workspace permission checks and the requirement to select at least one workspace remain unchanged.
* The workspace picker groups workspaces by dataplane name and region, lists LangSmith Cloud separately, and retains a flat list for organizations without dataplanes. Search matches workspace names, IDs, dataplane names, and regions, and identically named workspaces remain independently selectable.
* Creating or updating an LLM-as-judge evaluator returns HTTP 400 if its prompt lacks a structured output schema with feedback fields, preventing evaluators that appear to succeed but produce no feedback. Existing evaluators are unaffected.
* Repository owners in workspaces with more than 100 active members can change restricted mode and add or remove owners, even when they are outside the first 100 members.
* Requests from external agents and agents using workspace service keys include the associated agent and environment identity when their keys are linked to an agent environment. Existing deployment-key identity resolution takes precedence.
* Python, JavaScript, Go, and Java SDK users can create a decision-model evaluator in a single call. CLI users can create one with `langsmith evaluators create-decision-model`, specifying prompts, questions, a dataset, and variable mappings in a single command.
* The deprecated LangServe provider is unavailable in the provider picker for Playground, evaluators, and saved model configurations, and is no longer selected as an automatic fallback. Existing saved LangServe configurations and OpenAI- and Anthropic-compatible endpoints remain supported.
* Agents using remote MCP can create, update, and delete custom model prices and filter the price list by provider. Updating a model price outside the current workspace, including a built-in default, returns HTTP 404 instead of 500.
* Prompt Hub commit API errors use RFC 7807 problem details while retaining the legacy `error` field, and repository validation errors include per-field messages in `errors`. Deleting a missing prompt repository returns HTTP 200 instead of 404, making repeated deletes safe.
* The `langsmith api` CLI command warns on `stderr` when an endpoint is deprecated, including the removal date and migration links when available. JSON output on `stdout` remains unchanged.
* Error notifications automatically dismiss after five seconds, matching other notification types. Plain input fields, including dataset and experiment search, have visible backgrounds on white surfaces.
* The JavaScript SDK reduces memory usage during slow trace uploads by compressing runs as they enter the queue when the server supports gzip. Improved batching also reduces upload requests when runs arrive in quick succession.
* The Python and JavaScript SDKs avoid HTTP 403 errors when replicating traces to another LangSmith instance with a separate API key by no longer forwarding the primary instance's workspace ID. Each entry in `LANGSMITH_RUNS_ENDPOINTS` also supports a `workspace_id` for targeting a workspace with an organization-scoped API key.
* Scans continue when latency, token, or cost percentile queries fail, rather than aborting during setup. Scan evidence identifies the missing outliers, while failures in error or baseline queries still stop the scan.
* The Python SDK's `wrap_openai` traces OpenAI Agents API sessions, capturing model calls, tool calls, and subagents as LangSmith runs. Session turns are grouped into a thread and nest under a parent `@traceable` run when present.
* Worker heartbeats are stored in PostgreSQL, preventing Redis restarts from incorrectly marking active runs as unhealthy and requeuing them. This avoids duplicate execution and cascading failures.
* Python agent code can use `get_client()` to access its own deployment through an in-process connection.
* Column order changes made by dragging trace and run table headers persist across reloads and stay in sync with changes made through the **Columns** menu.
* Restoring a recent run filter places the cursor at the end of the query, so subsequent typing appends rather than prepends text. The run-details search bar also stays stable as thread results load or change.
* Networking and Brotli compression dependencies used by self-hosted deployments include patches for security vulnerabilities. Some Agent Server image dependencies still require upstream updates, so vulnerability scans may continue to report findings.
* Expanded output diffs in experiment tables and comparison views stay complete during automatic refreshes instead of reverting to truncated previews. Refreshes also no longer cause the diff view to jump or the expand button to flash.
* Python, JavaScript, and Java SDKs resolve API keys from the environment variable specified by a profile's `api_key_env` field. Profiles using `api_key_cmd` receive guidance to use `api_key_env` or `LANGSMITH_API_KEY` instead, with JavaScript and Java rejecting requests while Python warns and continues without a key.
* Checkpoint metadata excludes internal configuration fields and the redundant copy of the run context, reducing checkpoint storage growth for runs with large contexts. Existing checkpoint rows remain unchanged.
* With SQLite storage, deleting a thread or assistant also deletes its associated crons. Creating a cron that references a missing thread is rejected.
* Deployment metrics API requests that omit a step use an interval scaled to the requested time range, targeting roughly 60 points per series with a one-minute minimum. This reduces response sizes and prevents HTTP 502 errors on long-range queries, while explicitly supplied intervals remain unchanged.
* Issue scans use fixed-point decimals for cost thresholds, avoiding query errors and unnecessary retries when filtering for very small costs.
* Teams REST API documentation covers 17 operations, including team membership, workspace grants, and access-policy attachments. Teams pages no longer require a rollout override, while existing entitlement and permission requirements remain unchanged.
* Python graph runs in multi-process mode use the request's encryption context for checkpoints and store operations rather than empty metadata, so custom encryption works correctly.
* Run and cron searches work with SQLite when custom authorization uses `$contains` filters on thread metadata, avoiding `no such column: thread.metadata` errors.
* Deleting an assistant with `delete_threads=true` on SQLite-backed deployments removes the assistant and its associated threads without crashing.
* The thread storage endpoint, `GET /threads/{id}/storage`, reports storage usage on SQLite instead of returning an unimplemented error.
* Agent Server starts successfully with FastAPI included routers when custom-route authentication or auth-first middleware ordering is enabled. Nested route path parameters are available to authentication and middleware.
* Custom dashboards remain visible for tenants outside a query-backend allowlist. The chart migration runs only when the query backend is configured and enabled globally.
* CLI commands that accept a single project ID also accept `--project NAME`, so you can select projects by name rather than UUID. Commands that require a project fall back to `LANGSMITH_PROJECT` when no project is specified, except when reading a request from `stdin`.
* Deployments automatically set `LANGSMITH_ENDPOINT` alongside `LANGCHAIN_ENDPOINT`, preventing application code that reads only `LANGSMITH_ENDPOINT` from connecting to the wrong LangSmith instance. Explicit `LANGSMITH_ENDPOINT` or `LANGSMITH_RUNS_ENDPOINTS` settings continue to take precedence.
* The API reference at `/v1/fleet/docs` loads correctly, including behind gateways that use an `/api` prefix.
* SCIM user deletions and updates affect only the calling organization's login method, preventing changes to the same person's login methods or profile details in other organizations.
* A new read-only BigQuery query tool supports single-statement GoogleSQL queries, including CTEs, joins, and subqueries, while rejecting writes, exports, and multi-statement scripts before execution. Existing Google OAuth and IAM access controls still apply, and query result limits do not limit query cost.
* The CLI accepts `--start-time` and `--end-time` as aliases for `--since` and `--before` on run and trace filtering commands. It also accepts `langsmith rules` and `langsmith rule` as aliases for `langsmith evaluator rule`, while help output remains unchanged.
* Toggling an agent policy to its current state leaves its modification timestamp unchanged, preventing policy history from showing changes that do not occur.
* Tool policies support only deny rules, and the policy dialog no longer offers **Allow**. API requests to create or replace a policy with `PERMIT` return HTTP 400, and any matching deny rule blocks access regardless of policy order.
* Missing logos no longer prevent onboarding, invitation, and SSO verification emails from being sent.
* Terraform workspace membership resources no longer fail with permission errors after their workspace is deleted outside Terraform. Refresh removes stale membership state, and deletion succeeds when workspace deletion is confirmed.
* Updating, starting, stopping, or restarting a sandbox, sharing its service URL, and minting a service-URL token require you to be the sandbox's creator or have the `sandboxes:exec` permission, matching the requirement for running commands in it.
* New sandbox runtimes remain unready until LangSmith accepts a report that includes their elected host, preventing Helm installs and rollouts from reporting success prematurely. When migrating from an embedded runtime to a separate cluster, use a Helm `--timeout` longer than the default five minutes to allow the previous runtime registration to expire.
* The **Add feedback** picker prioritizes keys used for human feedback in the project over the past 30 days, with alphabetical groups for recently used keys and other feedback. Unapplied suggestion chips no longer appear in a trace's **Feedback** section, avoiding confusion with feedback already recorded.
* Online evaluation rules stop retrying windows whose query results exceed the receive-size limit and record the error in the rule log, while bulk exports also treat this error as permanent. The default retry limit for transient rule failures decreases from 10 attempts to 5, reducing delays from persistently failing windows but skipping affected evaluations sooner during prolonged outages.
* Sandbox AWS proxy roles support session tags set at sandbox creation that cannot be changed, allowing IAM policies to scope S3 access by user or thread without growing session policies for each mount. Roles using session tags must allow `sts:TagSession` in their trust policy.
* New Anthropic and Anthropic-compatible model configurations default to a maximum of 8,192 output tokens instead of 1,024. Existing saved configurations and explicitly set token limits remain unchanged.
* Validation replays for single-graph deployments fall back to the deployment's graph ID when no explicit graph selector is present, preventing `graph_identity_missing` errors that block replay against a preview deployment.
* Experiment comparisons no longer crash when you switch from a short diff preview to the full output. Read-only code displays fall back to plain text if the editor encounters an error.
* Newly created runs in SQLite-backed runtimes no longer wait until the next queue poll because of a timing issue.
* Evaluator tables on the evaluator page and project **Evaluators** tab show the organization's default weekly spend limit and spending percentage when that limit applies, instead of displaying "N/A" or a dash.
* The Python and TypeScript SDKs provide `sessions.create()` and `sessions.update()` methods for the existing v1 endpoints, returning the complete `TracerSession` resource, including timestamps and statistics.
* Agent API requests canceled by the caller return HTTP 499 instead of an internal server error (500). Request timeouts continue to return server errors.
* Creating a tracing project through the v1 API produces an audit event when audit logging is enabled. Update audit-log consumers to accept the new `create_tracer_session` operation value.
* Model pricing details show rates by context length and service tier, along with explanations of built-in and user-defined pricing. Editing or cloning a context-tiered pricing entry preserves its token threshold on save.
* A new internal endpoint, `POST /v1/trajectories/query`, returns paginated thread and trace trajectories for a project, with optional filtering, selected aggregate fields, and stored messages.
* Polly can search and read official documentation when answering questions without requiring a separate documentation assistant deployment. Documentation lookups support reading long pages in sections and explicitly report incomplete or failed results.
* Error-path connectors in trace trees remain red when you select a failed run, an ancestor, or a successful sibling that shares the path. Successful-only segments retain blue selection highlighting.
* Automation rules enforce server-side fetch byte limits and reliably resume processing when a time window exceeds the limit, preventing runs or threads from being skipped or processed more than once.
* Agent Server images and user graph dependencies support redis-py 8.x, removing the previous build constraint that blocked these versions. Redis connections retain their existing timeout and protocol behavior.
* Polly no longer incorrectly asks for an API key or blocks messages when you save a key just before opening the **Chat** panel.
* MCP tool calls use the caller's IP address for organization IP allowlist checks, allowing calls from approved IPs instead of incorrectly rejecting them. MCP initialization and tool listing also enforce the organization's IP allowlist.
* Prompt Hub directory endpoints return authentication and authorization errors as `application/problem+json` instead of plain text, matching their other error responses. The API specification also reflects this error format for listing directories and committing directory changes.
* Polly can discover the Tool Gateway kits available to you and read their tools' input schemas when building custom apps, enabling it to generate calls to those tools. It also identifies sources that require you to connect credentials.
* Sandbox lists and status checks enforce editing-credential scopes, preventing disclosure of out-of-scope sandboxes and their run configurations. General sandbox creation returns HTTP 403 for app- and sandbox-scoped editing credentials, while separately authorized editing-sandbox provisioning remains unchanged.
* Batch sandbox deletion respects the caller's editing scope, matching single-sandbox deletion. Sandboxes outside that scope are skipped as "sandbox not found," while permitted sandboxes are still deleted.
* Logging failures no longer cause otherwise successful actions, such as organization creation, to return server errors.
* Google Drive tools support files and permissions in Shared Drives and include Shared Drive items in search results. Existing account credentials, scopes, and permission checks remain unchanged.
* The commits list API supports cursor-based pagination with `page_size` and `cursor` parameters and a `next_cursor` response field, with stable ordering for commits that share a timestamp. Existing `limit`/`offset` pagination remains supported, but combining it with `cursor` or supplying an invalid cursor returns HTTP 400.
* Prompt deletion in the Go and JavaScript SDKs and the CLI accepts empty `204 No Content` responses without failing.
* The `GET /api/v1/repos` endpoint supports cursor pagination through optional `page_size` and `cursor` parameters, returning `next_cursor` for the next page or `null` on the last page. Existing `limit`/`offset` pagination remains supported, but cursors must match the requested sort and cannot be combined with a non-zero `offset`.

**Download the Helm chart:** [`langsmith-0.18.0-rc.54.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.18.0-rc.54/langsmith-0.18.0-rc.54.tgz)

**Sandbox runtime chart, for Sandboxes in a separate cluster:** [`langsmith-sandbox-0.18.0-rc.4.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-sandbox-0.18.0-rc.4/langsmith-sandbox-0.18.0-rc.4.tgz)

**2026-11-01**

## langsmith-0.17.36

**LangSmith version:** `0.17.63`

* AWS proxy rules with `role_arn` accept `session_tags` that LangSmith passes when assuming the role, letting one role's policy scope each sandbox with `${aws:PrincipalTag/<key>}`. Allow `sts:TagSession` in the role's trust policy.

**Download the Helm chart:** [`langsmith-0.17.36.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.36/langsmith-0.17.36.tgz)

**2026-10-31**

## langsmith-0.18.0-rc.53

**LangSmith version:** `0.18.19rc1`

* This release packages the same LangSmith application version as langsmith-0.18.0-rc.50. Refer to the [langsmith-0.18.0-rc.50](#langsmith-0-18-0-rc-50) release notes below.

**Download the Helm chart:** [`langsmith-0.18.0-rc.53.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.18.0-rc.53/langsmith-0.18.0-rc.53.tgz)

**Sandbox runtime chart, for Sandboxes in a separate cluster:** [`langsmith-sandbox-0.18.0-rc.3.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-sandbox-0.18.0-rc.3/langsmith-sandbox-0.18.0-rc.3.tgz)

**2026-10-30**

## langsmith-0.18.0-rc.52

**LangSmith version:** `0.18.19rc1`

* This release packages the same LangSmith application version as langsmith-0.18.0-rc.50. Refer to the [langsmith-0.18.0-rc.50](#langsmith-0-18-0-rc-50) release notes below.

**Download the Helm chart:** [`langsmith-0.18.0-rc.52.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.18.0-rc.52/langsmith-0.18.0-rc.52.tgz)

**Sandbox runtime chart, for Sandboxes in a separate cluster:** [`langsmith-sandbox-0.18.0-rc.3.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-sandbox-0.18.0-rc.3/langsmith-sandbox-0.18.0-rc.3.tgz)

**2026-10-30**

## langsmith-0.17.35

**LangSmith version:** `0.17.62`

* Workspace admins can create computer environments and access profiles through the Fleet API. Agents created on an environment run on its computers with those profiles applied.

**Download the Helm chart:** [`langsmith-0.17.35.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.35/langsmith-0.17.35.tgz)

**2026-10-29**

## langsmith-0.17.34

**LangSmith version:** `0.17.61`

* Agent Builder uses saved model OAuth credentials for chat, subagents, and thread titles. OAuth models retain auxiliary secret requirements and recover from transient token refresh failures.
* Run, trace, and thread pages show a request timeout message when loading takes too long instead of reporting that the service is unavailable.

**Download the Helm chart:** [`langsmith-0.17.34.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.34/langsmith-0.17.34.tgz)

**2026-10-29**

## langsmith-0.18.0-rc.51

**LangSmith version:** `0.18.19rc1`

* This release packages the same LangSmith application version as langsmith-0.18.0-rc.50. Refer to the [langsmith-0.18.0-rc.50](#langsmith-0-18-0-rc-50) release notes below for application changes.
* [Sandboxes](../Install%20an%20instance/Additional%20features/Enable%20Sandboxes/Enable%20Sandboxes%20on%20self-hosted%20LangSmith.md) can run in a separate cluster. Set `sandboxes.external.enabled` to `true` and install the runtime with the `langsmith-sandbox` chart that has the same appVersion as this release. To route control plane calls through the runtime's host ingress, set `sandboxes.external.hostIngressEndpoint` to an `https://` origin.
* Sandboxes can use a dedicated service-auth secret, set with `sandboxes.serviceAuth.secret` or `sandboxes.serviceAuth.secretKey`, and rotate it with the `previousSecret` and `previousSecretKey` values. An external runtime requires a dedicated secret that differs from `config.apiKeySalt`.
* `sandboxes.clusterName` sets the name of the sandbox runtime cluster. Choose it at install time, because renaming it hides every existing sandbox, snapshot, and host record.

**Download the Helm chart:** [`langsmith-0.18.0-rc.51.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.18.0-rc.51/langsmith-0.18.0-rc.51.tgz)

**Sandbox runtime chart, for Sandboxes in a separate cluster:** [`langsmith-sandbox-0.18.0-rc.2.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-sandbox-0.18.0-rc.2/langsmith-sandbox-0.18.0-rc.2.tgz)

**2026-10-29**

## langsmith-0.18.0-rc.50

**LangSmith version:** `0.18.19rc1`

* Gateway usage reports show input and output token counts alongside costs, making it easier to reconcile usage with tracing projects.

* The workspace selector offers a labeled, keyboard-selectable creation action below search results, with the search text prefilled as the workspace name. Sidebar searches with no matching workspaces display "No workspaces found."

* GPT-6.1 Terra is available in OpenAI model dropdowns in the Playground, model configurations, and Model Access suggestions. The default model remains unchanged.

* MCP clients using protocol revision `2026-07-28` receive typed forms for graph interrupts that declare a response schema, and graphs relay MCP tools' form and secure URL prompts to compatible clients. Clients without the required form or URL capabilities receive a clear error.

* The `POST /api/v1/runs/group` endpoint is deprecated with a sunset date of January 31, 2027, and returns deprecation and migration headers without changing its behavior. Migrate callers to `POST /api/v2/threads/query`.

* Concurrent LangSmith CLI commands on Windows refresh OAuth tokens reliably, avoiding timeouts and unnecessary login prompts. Saving refreshed tokens also retries when another command has the configuration file open.

* Run and thread event streams release resources after 120 seconds when a client stops reading, including when encryption or custom HTTP middleware is enabled. With encryption or custom HTTP middleware, the connection can remain open until the client disconnects.

* Issue evidence identifies the feedback keys supporting each linked trace, reads their current feedback from any span in the trace, and replaces cited keys when a trace is relinked. Engine issue details show each issue's cited feedback keys and trace counts, with links to the newest citing traces.

* Automated trace analysis reports structural tracing problems as individual tracing-quality issues rather than combining them in a metadata summary. It checks for split traces, orphaned or unfinished runs, and runs sent to the wrong project, even when messages or child runs are unavailable.

* Studio graphs show the names of tools currently running for Python and JavaScript agents. With a LangGraph version that provides tool metadata, tool nodes also show a tool count and a hover card listing their tools.

* Annotation queues offer "Show reviewer notes to other reviewers" under **Collaborator Settings**, allowing reviewers to read each other's notes in single, align, and pairwise review panes. The option is off by default and includes previously written notes when enabled, while reviewers can still edit only their own notes.

* GitLab connections rotate tokens to a supported lifetime within the instance's limit, even when the original token expires tomorrow or the limit is lowered after connecting. Instances that allow token lifetimes of only one day remain unsupported.

* You can freeze ranked bar chart tooltips with pointer or keyboard controls to select and copy values. Keyboard activation anchors the tooltip to the focused bar.

* Rolling upgrades preserve compatibility with older application processes that read agent archival timestamps. The migration preserves existing timestamps and restores the column if previously removed, but cannot recover deleted timestamps.

* Runs on threads that previously used event streaming endpoints honor their requested stream modes instead of inheriting the event streaming format. Studio Graph mode and streaming clients receive debug events and the expected message format.

* CLI commands such as `bulk-delete` and `delete-all` ask for confirmation before deleting, and `online-evaluators bulk-delete` supports deleting multiple online evaluators with repeated `--evaluator-id` options. Pass `--yes` to skip confirmation for `online-evaluators bulk-delete`.

* Insights analysis retries trace retrieval with smaller batches when a response exceeds the size limit, preventing failures from oversized responses.

* JavaScript evaluations support selective run uploads with an `uploadRuns` predicate while retaining all results locally and including them in summary evaluations. Setting `uploadRuns` to `false` runs evaluations locally without creating a project or uploading traces or feedback.

* You can search evaluator templates by name, description, evaluator type, or category in the **Configure Evaluator** picker and the "Get started with Evaluators" gallery. Searches with multiple terms show templates that match every term.

* The `langsmith-backend` image upgrades the transitive dependency `dnspython` from 2.8.0 to 2.9.0 to resolve [CVE-2026-114605](https://nvd.nist.gov/vuln/detail/CVE-2026-114605) (CVSS 7.5 High, CWE-674), whose [upstream fix](https://github.com/rthalley/dnspython/releases/tag/v2.9.0) prevents attacker-controlled DNS compression pointer chains in `dns.name.from_wire_parser` from causing CPU exhaustion or denial of service through malicious DNS wire-format messages. The dependency arrives through `langchainplus` > `pydantic[email]` > `email-validator` > `dnspython`, is absent from `langsmith-insights-engine` and all direct workspace dependencies, and is constrained with `dnspython>=2.9.0` in the root `[tool.uv]` `constraint-dependencies` because `email-validator` 2.3.0 already permits `>=2.0.0`, with `uv lock --upgrade-package dnspython` using uv 0.13.4 changing only `dnspython` in `uv.lock` and leaving the lock `revision` unchanged.

* No matching Linear tickets are identified because the Linear CLI is unavailable in this session.

* Managed Tools enforces separate permissions for integration management, profile administration, and runtime credential use while preserving legacy workspace-manager and deployment-runtime access. Complete the backend upgrade before exposing the updated UI to roles that rely only on granular permissions.

* Issue validation replay preserves additional checkpoint state, such as todos and summaries, when the checkpoint has no writes, avoiding malformed-history errors.

* JavaScript OpenAI Agents and Vercel AI SDK tracing integrations accept an agent address for root and child runs, Python OpenAI, Anthropic, and Gemini tracing wrappers recognize it in `tracing_extra` without type-checking errors, and Python Claude Agent SDK, Google ADK (including live), OpenAI Agents SDK, OpenAI Realtime, and Gemini Live integrations accept it for root traces to an agent environment instead of a project. The JavaScript integrations and listed Python SDK integrations reject an address combined with a project name, and an explicit destination supplied when creating a traced Python session overrides the configured destination.

* MCP clients using protocol revision `2026-07-28` can approve, reject, answer, or edit tool calls paused by LangChain's human-in-the-loop middleware instead of receiving a generic error. Python and JavaScript agents support batched reviews and per-call approvals, with invalid per-call edits returning correctable errors.

* Dashboard feedback and metadata search fields fit narrow containers without clipping.

* The JavaScript execution sandbox rejects HTTPS connections that rely on compromised eMudhra certificate authorities.

* Overlay-based sandboxes start faster when pre-provisioned disks are unavailable, reducing delays during bursts of sandbox creation.

* Redis Cluster connections through `redis.external.connectionUrl` derive TLS from the `rediss://` URL scheme, matching standalone Redis behavior. `redis.external.cluster.tlsEnabled` applies only to `redis.external.cluster.nodeUris`.

* You can target multiple Azure resources within a workspace using `azure/<resource>/<deployment>` as the model and a resource-specific API key in `AZURE_FOUNDRY_API_KEY_<RESOURCE>`, with the resource name uppercased and hyphens replaced by underscores. Existing `azure/<deployment>` requests continue to use the default resource and credentials.

* The v1 project create, upsert, and `PATCH` endpoints return the full project representation, matching the default `GET` response and including `last_run_start_time` for projects with existing activity. Response fields are additive, but clients independently regenerated from the updated OpenAPI schema may require source updates.

* Playwright browser drivers and other subprocesses launch from background worker threads in LangSmith Deployments without crashing.

* Bulk exports spanning more than 360 days consolidate empty hourly partitions, avoiding thousands of unnecessary export tasks for sparse data.

* Repository clones retry once after a transient failure, reducing cases where connected repositories appear disconnected during scans. Persistent failures appear in scan context and run metadata so unavailable checkouts are not mistaken for disconnected repositories.

* You can retrieve, update, and delete workspaces from the CLI using `--id` to specify the workspace. Deletion retains its confirmation prompt.

* Workspace-scoped service keys support Organization Viewer (the default) or Restricted organization roles when created or edited, without gaining access to other workspaces. Newly created workspace-scoped keys cannot create replacement service keys, while existing keys remain unchanged.

* Run lists, including paginated results, show subtree token and cost totals and the earliest first-token timestamp when supported by the backend. API clients can opt in with `include_subtree_usage` on `POST /api/v2/runs/query`, while omitting it preserves existing behavior.

* Coding agent outcomes receive pull request and installation events through the shared GitHub App on self-hosted installations. Events forward in the background without delaying or failing the original webhook response.

* Self-hosted installations can authenticate to model gateways with short-lived LLM auth proxy tokens instead of a static API key by setting `ENGINE_GATEWAY_AUTH=llm_auth_proxy`. This mode requires an explicit `GO_ENDPOINT` and cannot be combined with `ENGINE_GATEWAY_API_KEY_FILE`.

* Model requests use saved maximum-token and reasoning-effort defaults when no explicit request value is provided, including for fallback models. Explicit request values take precedence over saved settings, which take precedence over built-in defaults.

* The Go, Java, JavaScript, and Python SDKs support Server-Sent Events for v2 run, trace, and thread queries without changing existing non-streaming methods. The `langsmith` CLI supports these queries through `runs streaming query-v2`, `threads streaming query`, and `traces streaming query`, including AI-powered search with `--ai-search`.

* Playground experiment batches do not automatically retry after dispatch errors, reducing duplicate runs and repeated model calls when a response is lost or an upstream error occurs. Failures before dispatch still retry, but partial results after an ambiguous failure may require a manual rerun.

* Hugging Face PyTorch checkpoint loading protects against unsafe deserialization.

* Specially crafted Zstandard-compressed data no longer triggers a decoder panic.

* Taskset runs make a final attempt to capture completed trials and their rewards before cleanup after a timeout or repeated polling failures, preventing those trials from being incorrectly marked as not run.

* You can request asynchronous cancellation of queued, preparing, or running taskset runs with `POST /v1/platform/tasksets/{taskset_id}/runs/{run_id}/cancellation`, using the same `tasksets:run` permission required to start a run. Repeated requests are safe, and runs already finalizing or finished return `409` unless cancellation is already requested.

* New online evaluators default to the "top-level traces only" filter, so **Sample data** previews and **Test** use the full trace rather than an inner step. Existing saved evaluators remain unchanged.

* Prompt webhook payloads use RFC 3339 timestamps with a UTC timezone indicator for `created_at`, preventing parsing failures in receivers that require timezone-aware timestamps. All prompt webhook events use second-level precision without fractional seconds.

* Slack agent sessions avoid extra "Thinking" replies when there is no progress to display. Reply text arriving before a tool call streams correctly without skipped or duplicated text.

* Reopening a deployed custom app in the editor restores the deployed version and discards undeployed edits in the shared workspace, including other users' edits. This applies to newly created editing sandboxes, while existing sandboxes retain the previous behavior until replaced and never-deployed drafts remain intact.

* Listing agents on self-hosted installations without PgBouncer avoids intermittent timeouts and HTTP 500 errors.

* Direct links and bookmarks to workspace settings in personal organizations open the corresponding organization settings page instead of showing an upgrade prompt. Links without an organization-level equivalent open the default settings page.

* Slow sandbox memory-diff persistence during stops and checkpoints no longer blocks unrelated sandbox creation.

* When an organization invitation is unavailable to the current SSO session, users can switch accounts or sign-in methods and return to the invitation. Invitation links show all available login methods and prefill the invited email instead of automatically reusing the remembered SSO login.

* The snapshot selector on the **Sandboxes** page keeps the search field separate from scrolling options, preventing overlap in long snapshot lists.

* Attribute-based access policies evaluate requested tags when creating datasets, projects, experiments, prompts, and sandboxes, allowing administrators to restrict access-sensitive tag keys, and editors and deployment-runtime keys can tag sandboxes at creation. After upgrading, add deny policies for sensitive keys to those roles to prevent unrestricted assignment.

* Settings documentation links open the correct guides for API key management, model pricing, and retention auto-upgrades. Gateway policy empty states link to the guide for the active policy tab.

* Generated CLI commands no longer expose `--accept`, preventing requests with `--accept text/event-stream` from exiting successfully without output, and `sessions dashboard` always requests JSON and no longer accepts `--accept`. Dedicated streaming commands and SDK behavior remain unchanged.

* Run rule webhook header values are masked for callers without `rules:update`, including workspace viewers and read-only API keys, preventing credential exposure. Attempts to save the masked placeholder return HTTP 400 instead of overwriting stored credentials.

* OAuth connections to MCP-discovered providers such as Datadog succeed when providers grant expanded scopes rather than their advertised scopes. Token exchanges and refreshes accept and record granted scopes, while manually configured providers retain strict scope checks.

* CLI and Go SDK profiles can resolve API keys from an environment variable or a command instead of storing them in plaintext, although Go SDK trace uploads do not yet support these keys. Create CLI profiles with `--api-key-env` or `--api-key-cmd`.

* Insights analysis and reports, along with evaluations that access trace data, require project-level permissions to read traces and their inputs and outputs. Issue access alone or trace-conditioned grants no longer authorize these reads.

* MCP tools discovery responses include an optional `server_icon_url` for server-advertised icons, validated to use HTTPS and match the server's host and port. Existing cached responses gain this metadata on refresh or after the 12-hour cache expires.

* Basic authentication, session-based OAuth, and SCIM do not cache successful authentication results when the underlying database transaction fails to commit. Basic authentication also rejects these failures before returning a successful response.

* The coding agent **Usage** tab calculates merge rate as merged PRs divided by all PRs, matching the pull request count card, and distinguishes improvements from regressions in period comparisons with colors and accessible labels. Conversation-length buckets link to matching threads, and **User** and **Harness** filter suggestions include high-cost values that trace-count rankings miss.

* An organization-scoped access policy catalog exposes supported resource-permission pairs to keep policy authoring aligned with server validation. Access requires the ABAC entitlement and access-control management permission.

* Canceled Custom Apps requests return HTTP 499 instead of an internal server error. When opening the editor or creating an app, canceled write requests trigger a check to determine whether the write succeeds.

* Agent Builder uses configured OAuth authentication for saved custom model configurations, including subagent models, without blocking chat or requiring a static provider API key. Token acquisition and refresh failures display actionable errors, and other required secrets remain visible in API key settings.

* The JavaScript SDK lets you select a `langsmith auth login` profile and configuration file, with an option to prefer that login over `LANGSMITH_API_KEY`. Authentication behavior remains unchanged unless you set the new options.

* After a dropped connection, `runs.join_stream` and `runs.join` preserve `stream_mode` and `cancel_on_disconnect` when reconnecting. Reconnection retains the expected stream modes without requiring an SDK update.

* Default tenant ingest limits increase to 300,000 events per minute, 1,000,000 tracing requests per hour, and 15GB of tracing payloads per hour. On upgrade, tenants using the previous defaults automatically receive the higher limits, while customized limits, including unlimited values, remain unchanged.

* The workspace picker and dropdown display each workspace's data plane name and region to help distinguish where workspaces run. Hover over truncated details to see the full values.

* Sandbox runtimes enforce one active runtime per cluster name, preventing competing runtimes from incorrectly marking hosts gone and stopping their sandboxes. Conflicting runtimes receive HTTP 409, and moving a runtime to another namespace or cluster can require waiting up to six minutes after the previous runtime stops reporting.

* Self-hosted installations using basic authentication can configure the LLM auth proxy, including enabling it and setting its JWT audience and allowed URLs, without receiving a 400 error. Existing permission, entitlement, and audience validation requirements still apply.

* Organization admins and operators see a warning banner when sandbox runtimes lag behind LangSmith for more than 72 hours, run a newer release for more than 30 minutes, or stop reporting. The banner provides guidance on which component to upgrade or check without enforcing version alignment.

* Recent filter searches are saved when you leave the search bar, so newly applied searches remain in recent history even when you navigate away quickly.

* Failed sandbox creations clean up even if the caller disconnects, preventing request cancellation from leaving sandboxes stuck in provisioning and consuming quota.

* You can upload a CSV to add email addresses when inviting organization members, with duplicates removed and invalid rows reported. Invitations show a clear warning and disable submission when the list exceeds available seats or the 500-address request limit, rather than silently stopping address entry.

* Thread history reads and checkpoint cleanup work on PostgreSQL for threads whose first run uses `durability="exit"` with a DeltaChannel. Stalled TTL cleanup and deferred deletions resume automatically after upgrading, without a migration.

* Stateless runs return valid `Location` and `Content-Location` URLs, allowing clients to reconnect to dropped streams without a 404 while the temporary thread exists. SDK `on_run_created` callbacks receive the run's temporary `thread_id`.

* When `http.disable_webhooks` is set, run and cron requests discard supplied webhook URLs without resolving their hostnames or storing them. Cron updates containing only a webhook return a 422 error indicating that webhooks are disabled.

* Run and thread event streams release resources when a client stops reading and a Redis read fails during optimized streaming.

* Thread streams replay events when resumed with a `Last-Event-ID` of `0` or a bare millisecond timestamp, and accept negative integers such as `-1` to replay all events from the start instead of returning a 422 validation error. Thread streams and run joins also accept `<ms>-*` IDs without an error.

* Authorized administrators can delete access policies after confirming the full policy name, with a warning that deletion can change access and removes role and team attachments. Failed deletions display the error and keep the policy available for retry.

* Dataset and experiment CSV downloads offer a single-line option that replaces line breaks within cells with literal `\r` and `\n` sequences for downstream parser compatibility. Downloads preserve original cell values by default, and JSONL exports remain unchanged.

* JavaScript graphs using legacy `messages` streaming mode keep each model reply under a single message ID, aligning metadata, partial updates, and completion events. Anthropic replies no longer appear as an empty message followed by a separate text message.

* LangSmith's MCP server treats empty optional arguments as omitted, preventing false argument conflicts when querying runs or pushing prompts. Empty cursors start at the first page, while empty filters are excluded from queries.

* You can select multiple roles when creating an access policy in Visual or JSON mode and attach or remove roles from policy details. Assigned roles offer read-only base-permission previews, including for users without policy-management permission.

* The `events` streaming mode omits events from runs tagged `nostream`, including their child runs, so tagged model calls do not expose tokens through this mode. JavaScript graphs also support `langsmith:nostream`, while other streaming modes remain unchanged.

* The annotation queue API accepts `required_if` and `visible_if` conditions on rubric items, with rules limited to referencing earlier items in the rubric. The API stores and validates these conditions but does not enforce conditional requirements or visibility.

* Annotation queue sidebar rows show run names, input previews, and short IDs together, making items with identical names easier to distinguish. Hovering reveals the full ID and details, and keyboard navigation keeps focus aligned with the selected row.

* BYOC data planes require explicit local Engine enrollment instead of inheriting enrollment from LangSmith Cloud. On upgrade, unset enrollment defaults to off and requires explicit opt-in, while existing explicit on/off choices remain unchanged.

* The CLI commands `runs list`, `run list`, and `run export` support `--limit` values above 1,000 without a page-size error, automatically fetching additional pages up to the requested limit.

* None. Generated with [Claude Code](https://claude.com/claude-code).

* The `langsmith api` command prints hints to `stderr` when raw run requests have equivalent `runs list`, `traces list`, or `runs get` commands. Standard output remains unchanged.

* The CLI prints a troubleshooting hint once per run when authentication fails with a 401 or 403, covering endpoint configuration, revoked keys, workspace access, and signing in again. Error responses and standard output remain unchanged.

* Fixed security vulnerabilities. See CVE-2026-114605 for details.

**Download the Helm chart:** [`langsmith-0.18.0-rc.50.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.18.0-rc.50/langsmith-0.18.0-rc.50.tgz)

**2026-10-29**

## langsmith-0.18.0-rc.49

**LangSmith version:** `0.18.17rc1`

* This release packages the same LangSmith application version as langsmith-0.18.0-rc.45. Refer to the [langsmith-0.18.0-rc.45](#langsmith-0-18-0-rc-45) release notes below.

**Download the Helm chart:** [`langsmith-0.18.0-rc.49.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.18.0-rc.49/langsmith-0.18.0-rc.49.tgz)

**2026-10-29**

## langsmith-0.17.33

**LangSmith version:** `0.17.59`

* This release packages the same LangSmith application version as langsmith-0.17.31. Refer to the [langsmith-0.17.31](#langsmith-0-17-31) release notes below.

**Download the Helm chart:** [`langsmith-0.17.33.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.33/langsmith-0.17.33.tgz)

**2026-10-29**

## langsmith-0.18.0-rc.48

**LangSmith version:** `0.18.17rc1`

* This release packages the same LangSmith application version as langsmith-0.18.0-rc.45. Refer to the [langsmith-0.18.0-rc.45](#langsmith-0-18-0-rc-45) release notes below.

**Download the Helm chart:** [`langsmith-0.18.0-rc.48.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.18.0-rc.48/langsmith-0.18.0-rc.48.tgz)

**2026-10-29**

## langsmith-0.17.32

**LangSmith version:** `0.17.59`

* This release packages the same LangSmith application version as langsmith-0.17.31. Refer to the [langsmith-0.17.31](#langsmith-0-17-31) release notes below.

**Download the Helm chart:** [`langsmith-0.17.32.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.32/langsmith-0.17.32.tgz)

**2026-10-28**

## langsmith-0.17.31

**LangSmith version:** `0.17.59`

* The LLM gateway can call Azure AI Foundry with an Entra ID service principal instead of an API key, while workspaces with `AZURE_FOUNDRY_API_KEY` keep using that key. Add `AZURE_TENANT_ID`, `AZURE_CLIENT_ID`, and `AZURE_CLIENT_SECRET` to workspace secrets to use a service principal.
* Run lists show token usage and cost totals for parent and intermediate runs, including their descendants. First-token timing uses the earliest observed timestamp in each run's subtree.

**Download the Helm chart:** [`langsmith-0.17.31.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.31/langsmith-0.17.31.tgz)

**2026-10-28**

## langsmith-0.18.0-rc.47

**LangSmith version:** `0.18.17rc1`

* This release packages the same LangSmith application version as langsmith-0.18.0-rc.45. Refer to the [langsmith-0.18.0-rc.45](#langsmith-0-18-0-rc-45) release notes below.

**Download the Helm chart:** [`langsmith-0.18.0-rc.47.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.18.0-rc.47/langsmith-0.18.0-rc.47.tgz)

**2026-10-27**

## langsmith-0.17.30

**LangSmith version:** `0.17.58`

* Internal improvements and maintenance updates

**Download the Helm chart:** [`langsmith-0.17.30.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.30/langsmith-0.17.30.tgz)

**2026-10-27**

## langsmith-0.18.0-rc.46

**LangSmith version:** `0.18.17rc1`

* This release packages the same LangSmith application version as langsmith-0.18.0-rc.45. Refer to the [langsmith-0.18.0-rc.45](#langsmith-0-18-0-rc-45) release notes below.

**Download the Helm chart:** [`langsmith-0.18.0-rc.46.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.18.0-rc.46/langsmith-0.18.0-rc.46.tgz)

**2026-10-27**

## langsmith-0.17.29

**LangSmith version:** `0.17.57`

* This release packages the same LangSmith application version as langsmith-0.17.27. Refer to the [langsmith-0.17.27](#langsmith-0-17-27) release notes below.

**Download the Helm chart:** [`langsmith-0.17.29.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.29/langsmith-0.17.29.tgz)

**2026-10-27**

## langsmith-0.17.28

**LangSmith version:** `0.17.57`

* This release packages the same LangSmith application version as langsmith-0.17.27. Refer to the [langsmith-0.17.27](#langsmith-0-17-27) release notes below.

**Download the Helm chart:** [`langsmith-0.17.28.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.28/langsmith-0.17.28.tgz)

**2026-10-27**

## langsmith-0.17.27

**LangSmith version:** `0.17.57`

* Internal improvements and maintenance updates

* Fixed security vulnerabilities. See CVE-2026-114605 for details.

**Download the Helm chart:** [`langsmith-0.17.27.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.27/langsmith-0.17.27.tgz)

**2026-10-26**

## langsmith-0.17.26

**LangSmith version:** `0.17.56`

* Internal improvements and maintenance updates

**Download the Helm chart:** [`langsmith-0.17.26.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.26/langsmith-0.17.26.tgz)

**2026-10-26**

## langsmith-0.18.0-rc.45

**LangSmith version:** `0.18.17rc1`

* The Python SDK finishes sending buffered runs before a flush returns, preventing missing traces when a process exits immediately afterward. This works with and without compression.

* Sandbox mutations, including updates, start/stop actions, browser changes, and service URL/link operations, always require runtime access authorization. Denied requests return HTTP 403, and authorization errors block the operation with HTTP 500.

* Sandbox TCP forwarding rejects connections above configurable limits, defaulting to 128 per sandbox and 4,096 per host process, with a lower host limit when file descriptors are constrained. Buffered forwarding and connection cleanup bound descriptor usage, but replacing zero-copy forwarding can affect throughput.

* Workspace MCP connections reject cross-origin redirects to prevent custom credential headers from leaking while allowing same-origin redirects. Register MCP servers that redirect to a different origin using their final URL, even when no authentication is configured.

* API key settings preserve column widths and visibility, search all results before pagination, store filters in the URL, and export CSVs with the full schema. Keys assigned to multiple workspaces offer a searchable workspace list, and maximum-expiry settings are accessible from the key creation dialog.

* Root-cause analysis investigates metric regressions even when runs lack a Git revision. It uses a time-bounded range of changes in a connected repository to identify the responsible pull request.

* The `/v2/run/analytics` endpoint aggregates multiple metrics, such as token usage and costs, in a single request, eliminating separate requests for each metric.

* The `GET` and `PATCH` responses for `/v1/platform/workspaces/current/info` include `dashboard_url` from the configured `LANGSMITH_URL`, helping clients find dashboards hosted separately from the API. The URL preserves configured path prefixes and removes trailing slashes.

* Embedded browser windows in follow mode stay still until you hover over an edge panning zone, rather than panning with every pointer movement. The viewer waits for the first frame before displaying the screen, avoiding a broken-image placeholder.

* In BYOC deployments, rules that add runs to annotation queues no longer fail with a 401 "Invalid token" error when the usage-limits cache is cold.

* Automation rule backfill progress no longer overstates completion when a batch starts but has not processed any data. Previously completed progress remains accurately reflected.

* You can retrieve, create, and revoke public dataset shares with `langsmith datasets share get`, `create`, and `delete-all`. Sharing an already shared dataset returns the existing token with HTTP 200 instead of failing with HTTP 409.

* The Gateway **Usage** tab supports grouping spend by any custom `X-Gateway-*` header through the **Custom Dimension** option, without requiring a spend policy. Header-value drilldowns show spend by model, provider, user, or API key and link to matching traces.

* Numeric categorical feedback labels remain visibly selected after saving in annotation queue rubrics and run-page feedback cards. Clicking the selected label again clears the feedback.

* You can retrieve and create dataset splits with `langsmith datasets splits get` and `langsmith datasets splits create`.

* Waterfall timeline labels avoid overlap on long runs and in narrow panels while preserving detail when zoomed in. Elapsed times of one minute or longer display in minutes, with one decimal place when needed, while shorter times remain in seconds.

* Gemini text-to-speech and transcription runs use the correct audio pricing instead of showing zero cost. Vertex model pricing updates no longer fail when a model lacks an output price.

* Webhook credential repair restores delivery for affected webhooks by repairing credentials encrypted with a placeholder key during an earlier migration.

* Selecting **View trace** in the Gateway simulator opens the trace in a side pane, keeping the simulator and response visible and preserving the selected data plane. Traces open without requiring access to the Gateway **Traces** tab.

* `GET` and `POST /threads/{thread_id}/history` accept `select` to return only specified fields, including individual state values such as `values.messages`. On PostgreSQL-backed servers, field selection also avoids loading unselected state, reducing memory use for large histories.

* On self-hosted deployments before version 0.16, `langsmith traces get TRACE_ID` searches the workspace without requiring `--project`, while `--project`, `--project-id`, or `LANGSMITH_PROJECT` can narrow the lookup. Deployments on version 0.16 and later still require a project.

* You can view the current workspace's ID, display name, and handle with `langsmith settings list`, or select a workspace with `--workspace`.

* You can retrieve and query publicly shared runs using a share token with `langsmith public runs retrieve` and `langsmith public runs query`. The CLI still requires an API key or login, even though these endpoints do not require authentication.

* You can update and resolve projects and open their dashboards with `langsmith projects update`, `resolve`, and `dashboard`. The CLI also supports updating and deleting project insights, retrieving their runs, and creating insights configurations.

* You can retrieve a previously submitted product feedback note with `langsmith product-feedback retrieve --id <id>`, including notes sent with `langsmith report`.

* Organization admins can create workspaces with `langsmith workspaces create` using an API key or OAuth profile.

* You can create and update online evaluators and view their spend with `langsmith online-evaluators create`, `update`, and `spend`.

* You can create external agents with the Java SDK without explicitly specifying the agent type.

* The CLI supports retrieving, updating, and deleting run feedback, creating feedback tokens, submitting feedback with a token, and deleting feedback configurations, and no longer supports the deprecated `langsmith feedback "<note>"` alias. Use `langsmith report` instead.

* The `langsmith` CLI supports retrieving, updating, deleting, and populating annotation queues, managing queue items, and checking their status, count, and placement, but not creating or listing queues. Use `langsmith annotation-queues retrieve-queues --run-id` to find queue IDs.

* Workspaces created with the new navigation experience can switch back to the classic experience.

* Traces for bring-your-own-key calls to OpenAI and Anthropic include a redacted provider API key hint, helping you identify the key a call uses and reconcile usage with provider charges.

* The `langsmith sandboxes` CLI supports registry operations, beta browser commands, service URL sharing, snapshot lookup by name, and usage cost queries, with browser deletion and attachment creation unavailable in the beta browser commands. Dedicated commands support registry updates with `sandboxes registries update --new-name` and browser attachment creation with `sandboxes browsers attachments create --window-name`, where `--name` identifies the existing registry or browser.

* You can retrieve and update dataset examples, count examples, delete all examples, and create examples in bulk with `langsmith examples retrieve`, `update`, `retrieve-count`, `delete-all`, and `langsmith examples bulk create`.

* You can tag a dataset version selected by timestamp or existing tag with `langsmith datasets update-tags`, moving the tag if it already exists. The update response includes all tags on the version instead of returning `null`.

* Issue-validation replays for Open SWE preserve signed run context, allowing repository checkout and authenticated GitHub access to work correctly.

* You can copy examples from one dataset to another with `langsmith datasets clone`.

* You can hide and show Studio's right-side Interact/Trace panel. Its hidden state persists across Graph/Chat switches and page reloads, and showing it restores its previous width.

* The example-list API supports `exclude_default_fields=true` to return only explicitly selected fields without default fields or unselected `null` placeholders, including ID-only responses with `select=id`. The Python SDK's synchronous and asynchronous `list_examples` methods expose typed, documented `select` and `exclude_default_fields` options, and the JavaScript SDK's `listExamples` supports `select` and `excludeDefaultFields`, allowing selected-field retrieval without downloading inputs while requests that omit these options remain unchanged.

* New users can start account registration with `langsmith auth signup` and complete CLI authorization after onboarding instead of getting stuck on "Unable to load organizations."

* Custom roles support granular workspace permissions with independent selections in the role editor. Existing roles, role API integrations, and Terraform configurations remain compatible, including roles that combine legacy and granular permissions.

* Hovering anywhere on an evaluator's selection button shows its full description in a tooltip when the description is truncated.

* World folder uploads require `environment-spec.yaml` or `world/environment-spec.yaml`. Run creation validates the world versions pinned to selected tasks and returns HTTP 400 for missing or incomplete world specifications instead of queuing runs that fail later.

* The JavaScript SDK batches `createFeedback` calls that include `traceId` with pending trace uploads when multipart batching is available, except when `extendTraceRetention: false` is set, and batched calls resolve before delivery and log send errors rather than throwing. Use `awaitPendingTraceBatches()` or, in manual flush mode, `flush()` to wait for delivery.

* The date range picker stays within the viewport on short screens, keeping **Cancel** and **Apply** reachable when selecting dates, including in the annotation queue's **Download CSV** dialog.

* Automation rules correctly account for pending runs when processing crosses an hour boundary.

* History reads, state reads, and single or bulk state updates no longer fail with server errors for factory graphs using the gRPC checkpointer.

* Tables such as the API keys table show horizontal scrollbars, making off-screen columns and actions accessible on smaller screens.

* The Python SDK provides a helper for resolving a tracing destination, prioritizing an explicit project or address over environment settings and falling back to the default project. It validates addresses and rejects conflicting or incomplete destination settings.

* Self-hosted installations using OAuth with PKCE (`AUTH_TYPE=oauth`) show organization managers a dismissible deprecation warning with a link to the guide for migrating to client-secret authentication.

* Apps using the React `useStream` hook with `onToolEvent` or `toolProgress` can send messages through v1 run endpoints without 422 errors or unexpected tool-event errors. These endpoints accept `stream_mode: "tools"` but do not emit tool events.

* Thread streams honor the `stream_mode` filter sent by the Python and JavaScript SDKs instead of returning every run event. Filters support repeated query parameters, JSON arrays, and comma-separated values.

* Runs continue to completion and save their final state when stream events cannot be published, rather than stopping early and being incorrectly recorded as successful. Timed-out runs emit a `TimeoutError` event on their stream, and resumable runs in `messages` mode replay message events when clients reconnect with `Last-Event-ID`.

* JavaScript graphs streamed in legacy `messages` mode with subgraphs enabled emit `messages/complete` events without misreporting subgraph messages as root-graph messages, and mixed JavaScript/Python in-memory deployments preserve Python checkpoint interrupts. Intermittent JavaScript process crashes no longer stop the entire server after four lifetime exits, as the server stops restarting only after four exits within ten minutes.

* API connections recover faster after restarts, avoiding prolonged 500 errors. Thread streams release server resources promptly when clients disconnect.

* You can update datasets with `langsmith datasets update`, leaving omitted fields unchanged while replacing schemas, metadata, and transformations in full. Updates reject `null` names and baseline experiments not run on the dataset, and `patch_examples` applies only alongside schema or transformation changes and cannot modify examples in other datasets.

* The `langsmith info list` command displays server information, including the version, instance flags, batch-ingest configuration, and maximum SDK versions.

* Workspace administration supports action-specific permissions with matching UI controls, while existing `workspaces:manage` grants remain valid and independent permission requirements still apply. Assigning API-key roles requires role-assignment authority in every target workspace, and disabling a default model also requires permission to clear the default.

* When a storage outage leaves a running sandbox's filesystem read-only, its host automatically restarts the sandbox, usually within two minutes, so you do not need to stop and start it to restore writes.

* Model fallback policies support an optional `ejection` configuration through the API to temporarily skip candidates after a configurable number of trigger failures within a time window, while never skipping the last candidate. Editing and saving a policy in the UI removes this configuration until UI support is available.

* Agent overview pages consistently show the updated layout, header, and profile. Coding agents retain their separate overview.

* Sandbox evaluator **Test** failures show tracebacks in expandable error details, helping you identify the failing evaluator function and line instead of seeing only the exception message.

* Service-key-only callers, including run rules and evaluators, can synchronize tracing projects and look up organization user information without authentication errors in bring-your-own-cloud deployments.

* Saving a shared annotation queue custom view asks for confirmation even when other queues using it are hidden by access controls or the usage count is unavailable, and the count is no longer capped at 100 queues. Polly chat on queue pages is available only while creating or editing a custom view.

* You can reorder table columns by dragging the column label or empty header space instead of targeting a small button. A drag grip appears on hover or keyboard focus, while sorting, column menus, and resizing remain separate interactions.

* OAuth tokens and their agent connections remain intact when refresh tokens are rejected or expired tokens lack a refresh token, allowing accounts to reconnect without losing connections. Background authorization checks also update token status without starting an OAuth consent flow.

* Custom-app builds and edits provide periodic progress updates and pause after 45 minutes so you can review the preview before continuing. Stalled model streams time out after 90 seconds without output and retry once, while commands stop after two minutes, or ten minutes for package installs.

* Agent evaluator traces stay scoped to the current agent. Evaluator spend charts no longer offer Project / Dataset grouping, while workspace spend remains grouped by evaluator.

* Annotation queue sidebars show run names, input previews, and relative start times instead of truncated IDs without previews. Thread rows show a chat icon and the first user message, making queue items easier to distinguish.

* Organizations can use `anthropic_gateway` and `openai_gateway` in `ENGINE_MODEL_PROVIDERS` to route Claude and GPT requests through the installation's gateway, with selected gateways preferred over direct providers. The `ENGINE_GATEWAY_APIS` setting declares which APIs the gateway supports, and unconfigured gateway providers are unavailable.

* You can cancel agent runs started in Slack using Slack's native **Stop** button, which existing Slack apps gain when their channel setup next syncs the manifest. Customer-owned apps use their actual granted permissions, refresh them when you redeploy an active channel, and show **Stop** when granted the required permission, while generated manifests request Agent view support.

* Slack agent sessions stream thinking progress, tool-call status, and reply text into a single message alongside the **Stop** button. If streaming cannot start, replies continue to appear as regular messages.

* Slack run progress displays agent-provided status messages and task steps in timeline or plan view. Default progress messages remain the fallback when no custom status is provided.

* Slack feedback button clicks, including thumbs-up and thumbs-down ratings, reach connected agents. Forwarded button interactions and modal submissions no longer include Slack's legacy verification token.

* Redeploying a Slack channel without resending credentials preserves its active customer-owned Slack app instead of resetting the channel. Customer-owned apps can also move between deployments with explicit confirmation and update permission on the source deployment, and deleted channels no longer block app reuse.

* Issue validation can replay saved runs whose configuration omits the graph name by using graph metadata from the saved run or trace instead of leaving the issue inconclusive.

* Evaluator creation through the API validates that the evaluator type matches the model in its saved prompt, and existing evaluators cannot switch between JEV and regular AI judge types. Create a new evaluator to use a different type.

* Gateway calls to Anthropic Claude through Amazon Bedrock Runtime produce traces, spend records, and policy-violation records, including for inference profiles and streaming responses.

* You can register existing Linear OAuth apps through `/v1/agent-auth/apps`. Creating and deleting these apps requires deployment-update permissions rather than workspace-management access.

* Expanded sections in the dataset example side panel refresh when you switch between large examples, so their contents match the selected example instead of showing data from the previous one.

* Shared trace links on experiment comparison pages load without a "Something went wrong" error when exactly one experiment is selected, even if the trace's row has not yet loaded in the table.

* JavaScript graphs can use the SDK client to call their own deployment by passing the `langgraph_api:url` context variable as `apiUrl`, including with custom authentication. These calls preserve the run's user context, so authorization rules and thread ownership apply correctly.

* A security fix addresses a Brotli decoder vulnerability (CVE-2026-111497) that compressed responses from user-controlled URLs, such as webhook destinations and custom model endpoints, can trigger.

* Self-hosted deployments using the bundled operator support attaching `ServiceAccount` and `SecretProviderClass` resources through the deployment UI or `extra_manifests` API field, with deployment-update users able to view and edit saved resources in deployment settings, an editor showing the required deployment-resource-name-plus-`-` prefix, and `SecretProviderClass` resources restricted to pod workload identity and documented provider parameters. Enable this default-off feature with Helm `extraManifests.enabled`, and do not include credentials because manifests are stored in plaintext.

* Creating or editing an MCP server with manual OAuth requires an OAuth provider. Failed saves show an inline error and retain entered values, while automatic per-user OAuth continues to work without a provider ID.

* MCP tool discovery no longer stalls when a server sends continuous SSE pings during the initial fetch. Discovery enforces total timeouts and reports timed-out handshakes as upstream unavailability rather than misleading authentication errors.

* Workspace admins can enable or disable personal and built-in MCP servers for the entire workspace using `PATCH /v1/managed-tools/servers/{id}`. Disabled servers reject calls from all users, including admins, and their tools are omitted from tool kits.

* Workspace admins can use `GET /v1/managed-tools/servers?owned_by=any` to list workspace members' personal MCP servers and identify their owners without exposing connection details or credentials. The default server list remains unchanged.

* Granular workspace permissions let administrators delegate credential metadata access, credential management, and connection actions independently. Existing `workspaces:manage` grants retain access to these actions.

* Sandbox tags use resource-tag permissions, and Hub handle settings use workspace settings permissions, with the Hub UI reflecting the user's access. Existing `workspaces:manage` access remains supported alongside granular permissions.

* Fixed security vulnerabilities. See CVE-2026-111497 for details.

**Download the Helm chart:** [`langsmith-0.18.0-rc.45.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.18.0-rc.45/langsmith-0.18.0-rc.45.tgz)

**2026-10-26**

## langsmith-0.18.0-rc.44

**LangSmith version:** `0.18.14rc1`

* This release packages the same LangSmith application version as langsmith-0.18.0-rc.37. Refer to the [langsmith-0.18.0-rc.37](#langsmith-0-18-0-rc-37) release notes below.

**Download the Helm chart:** [`langsmith-0.18.0-rc.44.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.18.0-rc.44/langsmith-0.18.0-rc.44.tgz)

**2026-10-24**

## langsmith-0.17.25

**LangSmith version:** `0.17.53`

* Engine runs on OpenAI models summarize their history before a request exceeds 272K input tokens, the threshold at which OpenAI bills the whole request at long-context rates. Runs that fall back from Claude to OpenAI use the same limit.
* New Fleet agents default to Per-user connections, so each person connects their own accounts. Exported agent ZIP files preserve the agent's connection format when you import them.
* When a storage outage makes a running sandbox's filesystem read-only, its host automatically restarts the sandbox, usually within two minutes. This restores writes without requiring you to stop and start the sandbox.

**Download the Helm chart:** [`langsmith-0.17.25.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.25/langsmith-0.17.25.tgz)

**2026-10-24**

## langsmith-0.16.47

**LangSmith version:** `0.16.75`

* Internal improvements and maintenance updates

**Download the Helm chart:** [`langsmith-0.16.47.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.16.47/langsmith-0.16.47.tgz)

**2026-10-24**

## langsmith-0.18.0-rc.43

**LangSmith version:** `0.18.14rc1`

* This release packages the same LangSmith application version as langsmith-0.18.0-rc.37. Refer to the [langsmith-0.18.0-rc.37](#langsmith-0-18-0-rc-37) release notes below.

**Download the Helm chart:** [`langsmith-0.18.0-rc.43.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.18.0-rc.43/langsmith-0.18.0-rc.43.tgz)

**2026-10-22**

## langsmith-0.18.0-rc.42

**LangSmith version:** `0.18.14rc1`

* This release packages the same LangSmith application version as langsmith-0.18.0-rc.37. Refer to the [langsmith-0.18.0-rc.37](#langsmith-0-18-0-rc-37) release notes below.

**Download the Helm chart:** [`langsmith-0.18.0-rc.42.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.18.0-rc.42/langsmith-0.18.0-rc.42.tgz)

**2026-10-22**

## langsmith-0.18.0-rc.41

**LangSmith version:** `0.18.14rc1`

* This release packages the same LangSmith application version as langsmith-0.18.0-rc.37. Refer to the [langsmith-0.18.0-rc.37](#langsmith-0-18-0-rc-37) release notes below.

**Download the Helm chart:** [`langsmith-0.18.0-rc.41.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.18.0-rc.41/langsmith-0.18.0-rc.41.tgz)

**2026-10-22**

## langsmith-0.17.24

**LangSmith version:** `0.17.52`

* Internal improvements and maintenance updates

**Download the Helm chart:** [`langsmith-0.17.24.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.24/langsmith-0.17.24.tgz)

**2026-10-22**

## langsmith-0.17.23

**LangSmith version:** `0.17.51`

* Internal improvements and maintenance updates

**Download the Helm chart:** [`langsmith-0.17.23.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.23/langsmith-0.17.23.tgz)

**2026-10-22**

## langsmith-0.16.46

**LangSmith version:** `0.16.74`

* Internal improvements and maintenance updates

**Download the Helm chart:** [`langsmith-0.16.46.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.16.46/langsmith-0.16.46.tgz)

**2026-10-21**

## langsmith-0.18.0-rc.40

**LangSmith version:** `0.18.14rc1`

* This release packages the same LangSmith application version as langsmith-0.18.0-rc.37. Refer to the [langsmith-0.18.0-rc.37](#langsmith-0-18-0-rc-37) release notes below.

**Download the Helm chart:** [`langsmith-0.18.0-rc.40.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.18.0-rc.40/langsmith-0.18.0-rc.40.tgz)

**2026-10-21**

## langsmith-0.17.22

**LangSmith version:** `0.17.49`

* When `GO_INGESTION_CONCURRENCY_PER_CPU` is unset, each ingest-queue pod runs 8 tasks per CPU in its CPU limit, capped at the node's CPU count. If your ingest-queue pods have less than 1 CPU, raise their CPU limit to the chart's 2-CPU limit or set `GO_INGESTION_CONCURRENCY_PER_CPU=1`.
* Engine runs that use your own model providers no longer stop partway through with an `Invalid signature in thinking block` error. Engine also keeps more of a run's history before summarizing it.

**Download the Helm chart:** [`langsmith-0.17.22.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.22/langsmith-0.17.22.tgz)

**2026-10-21**

## langsmith-0.17.21

**LangSmith version:** `0.17.48`

* Command-click or Ctrl-click a trace in the traces table to open it in a new tab. Regular clicks continue to open the side panel.

**Download the Helm chart:** [`langsmith-0.17.21.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.21/langsmith-0.17.21.tgz)

**2026-10-21**

## langsmith-0.16.45

**LangSmith version:** `0.16.73`

* Command-click or Ctrl-click a trace in the traces table to open it in a new tab. Regular clicks continue to open the side panel.

**Download the Helm chart:** [`langsmith-0.16.45.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.16.45/langsmith-0.16.45.tgz)

**2026-10-21**

## langsmith-0.18.0-rc.39

**LangSmith version:** `0.18.14rc1`

* This release packages the same LangSmith application version as langsmith-0.18.0-rc.37. Refer to the [langsmith-0.18.0-rc.37](#langsmith-0-18-0-rc-37) release notes below.

**Download the Helm chart:** [`langsmith-0.18.0-rc.39.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.18.0-rc.39/langsmith-0.18.0-rc.39.tgz)

**2026-10-20**

## langsmith-0.17.20

**LangSmith version:** `0.17.47`

* Fleet records lowercase user emails for new UI and API runs so email casing does not split usage into separate user rows.
* You can choose which default alert fields to include in webhook bodies or omit all default fields for receivers such as Google Chat that require a specific payload.

**Download the Helm chart:** [`langsmith-0.17.20.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.20/langsmith-0.17.20.tgz)

**2026-10-20**

## langsmith-0.17.19

**LangSmith version:** `0.17.46`

* Queue workers run `GO_INGESTION_CONCURRENCY_PER_CPU` tasks per CPU of the pod CPU limit instead of the node, keeping task counts consistent across node sizes (2 tasks per ingest-queue pod with the default chart). To run more tasks, set `GO_INGESTION_CONCURRENCY_PER_CPU` in `ingestQueue.deployment.extraEnv`.
* API requests return HTTP 429 instead of HTTP 503 when the query service reports exhausted resources, allowing clients to handle throttling correctly.
* Bedrock model configurations support automatic routing or explicit selection of the Bedrock Runtime or Bedrock Mantle endpoint. This supports models available through both endpoints when AWS permissions allow access to only one.

**Download the Helm chart:** [`langsmith-0.17.19.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.19/langsmith-0.17.19.tgz)

**2026-10-20**

## langsmith-0.16.44

**LangSmith version:** `0.16.72`

* You can choose which default alert fields to include in webhook bodies or omit all default fields for receivers such as Google Chat that require a specific payload.

**Download the Helm chart:** [`langsmith-0.16.44.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.16.44/langsmith-0.16.44.tgz)

**2026-10-19**

## langsmith-0.18.0-rc.38

**LangSmith version:** `0.18.14rc1`

* This release packages the same LangSmith application version as langsmith-0.18.0-rc.37. Refer to the [langsmith-0.18.0-rc.37](#langsmith-0-18-0-rc-37) release notes below.

**Download the Helm chart:** [`langsmith-0.18.0-rc.38.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.18.0-rc.38/langsmith-0.18.0-rc.38.tgz)

**2026-10-19**

## langsmith-0.18.0-rc.37

**LangSmith version:** `0.18.14rc1`

* Organization settings support tracing-only API keys scoped to one or more workspaces. These organization-owned keys submit traces and create tracing projects without granting access to stored traces or administrative operations. They use the service-key expiration policy, and authorized key managers can delete them. A dedicated Tracing tab provides search, pagination, and CSV export.
* The trace input view displays OpenAI Responses and Chat Completions inputs as message cards instead of a raw data tree when SDK calls include request options such as an abort signal. The JSON view preserves the complete original input, including request options and metadata.
* Organization-scoped Playground model settings support reads and updates without an `X-Tenant-Id` header. Reads require `organization:read`, and changes require `organization:manage-model-configs`.
* Insights reports generated from saved configurations through the job queue include trace feedback.
* Thread event streams return HTTP 403/404 for access failures and 422 for malformed thread IDs before streaming starts, avoiding generic errors after HTTP 200 that can trigger endless reconnects. WebSocket streams expose corresponding close codes (4403, 4404, and 4422), and HTTP subscriptions with custom authorization filters return 404 for threads that do not yet exist.
* On the protocol v2 API, `run.start` input during an active run follows the multitask strategy immediately (queuing by default) without a wait of up to five seconds, and messages are not dropped while answered interrupts process or after cancellation with no open interrupt. Use `input.respond` when answering interrupts through HTTP clients during an active run.
* Granting an organization-wide team access to a workspace automatically creates a workspace team, and revoking access deletes it. Workspace teams start with no inherited members or policies and cannot be created, edited, or deleted directly through the teams API.
* The composite score picker includes all feedback keys with numeric scores, including keys with categorical feedback configurations and keys without a configuration. These keys no longer disappear from the picker.
* The Playground hides unsupported `seed` settings for OpenAI Responses API models and keeps reasoning settings consistent with the selected API mode. Requests with unsupported `seed` or `input_schema` settings for OpenAI and Azure OpenAI Responses API models return a 422 error that identifies the fields without exposing their values. Invocations have a 290-second limit, preserve shorter caller timeouts and cancellation, and return an actionable 504 error before the ingress timeout.
* The model pricing API supports case-insensitive filtering by one or more providers and sorting by start date. The new `GET /model-price-map/providers` endpoint lists providers and their model pricing entry counts. **Settings** > **Model pricing** supports the same filtering and sorting, and preserves the selections in the URL.
* Opening a queued run that belongs to a thread shows the full conversation in the thread pane, with the Trajectory tab selected. Runs without a thread continue to open in the run pane.
* Filter queries hide errors for a trailing `AND` or `OR` while you type after the operator. The error returns when you leave the filter bar or move the cursor before the operator.
* Studio no longer shows an unnecessary tracing upgrade warning when connected to a JavaScript Agent Server.
* Feedback filter suggestions distinguish numeric scores from text values and category labels. Select a typed feedback field to build trace and thread filters.
* Evaluator rule errors contain only the exception instead of the full response payload, preventing oversized error messages from causing database errors and rule execution failures.
* In annotation queues, the View item pane's Details tab displays long run inputs and outputs in full, with Attributes below them instead of overlapping the content.
* Model pricing settings show model types, supported input types, and consolidated pricing in a searchable grid. Select a model to view its matching rules and full price breakdown, or to edit, clone, or delete its pricing.
* The Fleet usage UI's user and agent cost reports are available through `GET /v1/fleet/usage/users` and `GET /v1/fleet/usage/agents`. Each report supports a time window, sorting, and cursor pagination with up to 100 results per page.
* Clicking an agent's breadcrumb opens its overview. A separate arrow button opens the agent switcher, and the close control is separate.
* Automation rule batches that exceed PostgreSQL size limits or model context limits fail permanently instead of being retried.
* The side navigation clears the selected agent context on pages that show all agents, such as the full annotation queue list, keeping it consistent with the breadcrumbs.
* Engine separates organization configuration access from spend and pause controls using dedicated permissions. Existing Organization Admin and Operator access is preserved.
* Prompt tag creation and update webhooks use the same author attribution as prompt commits, including identity-provider display names and fallback names. Email addresses serve as a fallback only for private prompts in non-anonymous organizations.
* The new `POST /feedback-configs/by-session/query` endpoint returns the feedback configuration IDs associated with each experiment's scores, grouped by feedback key. It also indicates whether any scores lack a configuration ID and fall back to the key's first configuration.
* Manual feedback and annotation queue forms use each feedback key's enforced configuration and catch out-of-range scores before submission.
* Validation replay accepts equivalent user-message formats and added memory-file context instead of incorrectly rejecting valid histories. Exact replay works for threads with more than 100 checkpoints on deployments that require structured checkpoint cursors. Replay also reduces timeouts on long-running threads and retries transient failures when reading history.
* Individual trace views use the same trajectory processing as thread views to display messages, tool results, and subagent previews.
* Managed evaluation consent and organization evaluator spending controls check dedicated permissions. Existing Organization Admin and Operator access is preserved.
* Workspace deletion and MCP tool cache updates and cleanup succeed on databases configured with an all-tables logical replication publication.
* TypeSafe gateway configurations support selecting `jev-1.14.0` and `jev-preview`, which also appear in gateway Model Access suggestions. `jev-latest` remains the default.
* Dashboard ratio KPI charts offer a "Display as percentage" option, showing values such as 0.16 as 16%. Decimal display remains the default, and the selected format is preserved when saving and editing a chart.
* Opening a deleted or inaccessible prompt shows a not-found page with a link back to the list instead of remaining stuck loading. Other prompt-loading failures show an error message.
* Polly caches system prompts when using Claude through a Vertex AI model configuration, reducing input token costs on repeated model calls.
* Code evaluator attachments distinguish between trace, thread, and trajectory scopes and reject attachments that mix thread and trajectory scopes.
* Issue recurrence and metric charts mark when fix pull requests merge, making it easier to see whether recurrences stop after a fix. Markers also appear for previously merged fixes when their merge times fall within the chart's date range.
* The Engine and Set up breadcrumbs preserve your selected agent, including All agents, when navigating.
* Single-run and pairwise annotation queues no longer show a previous item's Reference Outputs when navigating between items. In alignment queues, Add to Dataset no longer prefills another run's reference outputs for a run without a reference example.
* Red-team runs focus on correctness, guardrails, and explicit policies, allocating their call budget across these areas and marking other attack families as untested. Clear violations of unconditional instructions or explicit policies qualify as findings on their own.
* Code evaluators run correctly when their code is not initially loaded, preventing incorrect "Evaluator prompt missing or deleted" errors and missing feedback. If evaluator code is missing, the rule reports an error while its other actions continue.

**Download the Helm chart:** [`langsmith-0.18.0-rc.37.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.18.0-rc.37/langsmith-0.18.0-rc.37.tgz)

**2026-10-19**

## langsmith-0.17.18

**LangSmith version:** `0.17.45`

* Internal improvements and maintenance updates

**Download the Helm chart:** [`langsmith-0.17.18.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.18/langsmith-0.17.18.tgz)

**2026-10-16**

## langsmith-0.18.0-rc.36

**LangSmith version:** `0.18.13rc1`

* This release packages the same LangSmith application version as langsmith-0.18.0-rc.32. Refer to the [langsmith-0.18.0-rc.32](#langsmith-0-18-0-rc-32) release notes below.

**Download the Helm chart:** [`langsmith-0.18.0-rc.36.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.18.0-rc.36/langsmith-0.18.0-rc.36.tgz)

**2026-10-16**

## langsmith-0.18.0-rc.35

**LangSmith version:** `0.18.13rc1`

* This release packages the same LangSmith application version as langsmith-0.18.0-rc.32. Refer to the [langsmith-0.18.0-rc.32](#langsmith-0-18-0-rc-32) release notes below.

**Download the Helm chart:** [`langsmith-0.18.0-rc.35.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.18.0-rc.35/langsmith-0.18.0-rc.35.tgz)

**2026-10-16**

## langsmith-0.18.0-rc.34

**LangSmith version:** `0.18.13rc1`

* This release packages the same LangSmith application version as langsmith-0.18.0-rc.32. Refer to the [langsmith-0.18.0-rc.32](#langsmith-0-18-0-rc-32) release notes below.

**Download the Helm chart:** [`langsmith-0.18.0-rc.34.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.18.0-rc.34/langsmith-0.18.0-rc.34.tgz)

**2026-10-16**

## langsmith-0.18.0-rc.33

**LangSmith version:** `0.18.13rc1`

* This release packages the same LangSmith application version as langsmith-0.18.0-rc.32. Refer to the [langsmith-0.18.0-rc.32](#langsmith-0-18-0-rc-32) release notes below.

**Download the Helm chart:** [`langsmith-0.18.0-rc.33.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.18.0-rc.33/langsmith-0.18.0-rc.33.tgz)

**2026-10-16**

## langsmith-0.17.17

**LangSmith version:** `0.17.44`

* Fleet usage reports return `agent_id` instead of `assistant_id` and `user_email` instead of `owner_email`. Agent reports omit `owner_email`, and reported costs are estimates in USD.

**Download the Helm chart:** [`langsmith-0.17.17.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.17/langsmith-0.17.17.tgz)

**2026-10-16**

## langsmith-0.17.16

**LangSmith version:** `0.17.43`

* Retrieve user and agent cost reports from the Fleet usage UI through `GET /v1/fleet/usage/users` and `GET /v1/fleet/usage/agents`. Both endpoints support time windows, sorting, and cursor pagination with up to 100 results per page.

**Download the Helm chart:** [`langsmith-0.17.16.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.16/langsmith-0.17.16.tgz)

**2026-10-16**

## langsmith-0.18.0-rc.32

**LangSmith version:** `0.18.13rc1`

* Queue worker concurrency scales with the pod's CPU limit rather than the node's CPU count, so each ingest-queue pod runs 2 tasks concurrently with the default Helm chart. To increase concurrency, set `GO_INGESTION_CONCURRENCY_PER_CPU` in `ingestQueue.deployment.extraEnv` or override the CPU count with `GOMAXPROCS`.
* You can add custom providers that use the Anthropic Messages API with a full endpoint URL and a workspace API key. The gateway uses the configured URL without appending a path and does not forward Anthropic subscription credentials.
* Tracing quickstart snippets use updated models: `gpt-6-luna` for OpenAI, `claude-haiku-5-5` for Anthropic, and `gemini-3.8-flash` for Google. The LangGraph example also omits the unsupported temperature setting to avoid request failures.
* Tracing quickstart snippets for Microsoft Agent Framework and LiveKit correctly escape project names in OpenTelemetry headers, including spaces and special characters. This prevents copied configurations from failing to export traces or sending them to the default project instead of the selected project.
* Role permission previews in the API key creation dialog remain fully visible, keeping the heading, search, and scrollable permission list accessible even in smaller windows.
* When attaching an evaluator from a dataset, you can choose from all evaluators in the workspace. Adding a dataset to an evaluator also attaches it to the associated agent.
* When adding datasets to an agent, you can select from all datasets in the workspace. Selected datasets are tagged to the agent.
* You can save ScaleDown Chat Completions and Decisions endpoints as model configurations served through the LLM Gateway.
* You can filter evaluator spend by `agent_id` on GET `/v1/platform/evaluators/spend` to count only spend associated with that agent. Listing evaluators with `agent_id` also scopes returned run rules and per-evaluator spend, run counts, and resources to that agent.
* Multi-turn validation replays restore cumulative conversation history when checkpoints omit write metadata instead of silently running with an empty history. Replays verify the restored thread state before execution and reject unsupported or inconsistent histories.
* API keys the platform mints for new deployments use the Deployment Runtime role instead of Workspace Admin, providing Workspace Editor permissions plus LLM Gateway access, sandbox exec, and Agent Auth credential use. Existing deployment keys remain unchanged.
* Deployment logs remain available when application timestamps are missing, invalid, or lack a timezone, using Kubernetes timestamps as a fallback. Valid application timestamps remain unchanged, and logs from multiple pods remain in order.
* Run-rule webhooks respect `WEBHOOK_REQUEST_TIMEOUT_SEC` (10 seconds by default) instead of timing out after 5 seconds. Requests that time out continue to be retried.

**Download the Helm chart:** [`langsmith-0.18.0-rc.32.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.18.0-rc.32/langsmith-0.18.0-rc.32.tgz)

**2026-10-15**

## langsmith-0.18.0-rc.31

**LangSmith version:** `0.18.11rc1`

* Internal improvements and maintenance updates

**Download the Helm chart:** [`langsmith-0.18.0-rc.31.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.18.0-rc.31/langsmith-0.18.0-rc.31.tgz)

**2026-10-15**

## langsmith-0.17.15

**LangSmith version:** `0.17.42`

* Internal improvements and maintenance updates

**Download the Helm chart:** [`langsmith-0.17.15.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.15/langsmith-0.17.15.tgz)

**2026-10-15**

## langsmith-0.17.14

**LangSmith version:** `0.17.41`

* Internal improvements and maintenance updates

**Download the Helm chart:** [`langsmith-0.17.14.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.14/langsmith-0.17.14.tgz)

**2026-10-15**

## langsmith-0.16.43

**LangSmith version:** `0.16.71`

* This release packages the same LangSmith application version as langsmith-0.16.42. Refer to the [langsmith-0.16.42](#langsmith-0-16-42) release notes below.

**Download the Helm chart:** [`langsmith-0.16.43.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.16.43/langsmith-0.16.43.tgz)

**2026-10-15**

## langsmith-0.18.0-rc.30

**LangSmith version:** `0.18.11rc1`

* This release packages the same LangSmith application version as langsmith-0.18.0-rc.24. Refer to the [langsmith-0.18.0-rc.24](#langsmith-0-18-0-rc-24) release notes below.

**Download the Helm chart:** [`langsmith-0.18.0-rc.30.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.18.0-rc.30/langsmith-0.18.0-rc.30.tgz)

**2026-10-15**

## langsmith-0.18.0-rc.29

**LangSmith version:** `0.18.11rc1`

* This release packages the same LangSmith application version as langsmith-0.18.0-rc.24. Refer to the [langsmith-0.18.0-rc.24](#langsmith-0-18-0-rc-24) release notes below.

**Download the Helm chart:** [`langsmith-0.18.0-rc.29.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.18.0-rc.29/langsmith-0.18.0-rc.29.tgz)

**2026-10-15**

## langsmith-0.18.0-rc.28

**LangSmith version:** `0.18.11rc1`

* This release packages the same LangSmith application version as langsmith-0.18.0-rc.24. Refer to the [langsmith-0.18.0-rc.24](#langsmith-0-18-0-rc-24) release notes below.

**Download the Helm chart:** [`langsmith-0.18.0-rc.28.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.18.0-rc.28/langsmith-0.18.0-rc.28.tgz)

**2026-10-14**

## langsmith-0.18.0-rc.27

**LangSmith version:** `0.18.11rc1`

* This release packages the same LangSmith application version as langsmith-0.18.0-rc.24. Refer to the [langsmith-0.18.0-rc.24](#langsmith-0-18-0-rc-24) release notes below.

**Download the Helm chart:** [`langsmith-0.18.0-rc.27.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.18.0-rc.27/langsmith-0.18.0-rc.27.tgz)

**2026-10-14**

## langsmith-0.18.0-rc.26

**LangSmith version:** `0.18.11rc1`

* This release packages the same LangSmith application version as langsmith-0.18.0-rc.24. Refer to the [langsmith-0.18.0-rc.24](#langsmith-0-18-0-rc-24) release notes below.

**Download the Helm chart:** [`langsmith-0.18.0-rc.26.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.18.0-rc.26/langsmith-0.18.0-rc.26.tgz)

**2026-10-14**

## langsmith-0.17.13

**LangSmith version:** `0.17.40`

* Updated Fleet to load and invoke custom MCP tools at their registered URL, preserving trailing slashes, and to show an actionable connection error for redirecting servers instead of a generic tools-loading failure.

**Download the Helm chart:** [`langsmith-0.17.13.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.13/langsmith-0.17.13.tgz)

**2026-10-14**

## langsmith-0.16.42

**LangSmith version:** `0.16.71`

* Fixed the Playground to use the custom API key name when loading a default model preset instead of falling back to the provider's default key, such as `OPENAI_API_KEY`.
* Updated LangSmith to render `additional_tools` in OpenAI Responses traces as expandable tool definitions under a Developer message while preserving Developer message roles in the trace view.
* Added support for OIDC-authenticated users to list and manage workspace secrets according to their workspace permissions.
* Fixed the Active, Pending, and Deactivated tabs on the Members settings page to switch on the first click while keeping pagination and sorting in sync.

**Download the Helm chart:** [`langsmith-0.16.42.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.16.42/langsmith-0.16.42.tgz)

**2026-10-14**

## langsmith-0.17.12

**LangSmith version:** `0.17.39`

* Updated shared Fleet agents to use the running user's name and email for current-user context instead of values saved by the agent's creator, including in headless and LangGraph SDK runs.
* Added Fleet role-based access control for agents, skills, tools, OAuth connections, and files. Set the `FLEET_RBAC_PERMISSIONS_ENABLED` environment variable to turn it on. It is off by default and requires no role migration or backfill.
* Updated the agent hover card to show Delete only when you have permission to delete that agent.

**Download the Helm chart:** [`langsmith-0.17.12.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.12/langsmith-0.17.12.tgz)

**2026-10-14**

## langsmith-0.18.0-rc.25

**LangSmith version:** `0.18.11rc1`

* This release packages the same LangSmith application version as langsmith-0.18.0-rc.24. Refer to the [langsmith-0.18.0-rc.24](#langsmith-0-18-0-rc-24) release notes below.

**Download the Helm chart:** [`langsmith-0.18.0-rc.25.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.18.0-rc.25/langsmith-0.18.0-rc.25.tgz)

**2026-10-14**

## langsmith-0.18.0-rc.24

**LangSmith version:** `0.18.11rc1`

* Added support for routing self-hosted sandbox egress through corporate forward proxies that require a username and password. You supply credentials in the proxy URL, and sandboxes never see them.
* Updated the `X-LangSmith-Gateway-Metadata` response header to include `blocking_policies` with the ID, name, and type of each gateway policy that blocked a request.
* Improved app loading by loading syntax highlighting on demand instead of on every page, reducing background asset requests.
* Fixed Studio's condensed Interact view to show the model's reply as the turn's output when middleware hooks run after the model, and to display reasoning model replies as messages instead of raw JSON.
* Added per-call prompt-cache token and cost breakdowns to trace messages' conversation group metadata, including cache reads, writes, and durations when available, while retaining the existing response format for calls without cache breakdowns.
* Improved the annotation queue's run list and feedback panel to scale with the window, preventing messages from overflowing their bubbles in half-screen views.
* Added links to blocking policy names in simulator request errors. A link highlights the corresponding policy and expands its default policy when needed.
* Removed the app's local Find bar and Cmd+F and Ctrl+F handling from thread trajectory and messages views while retaining search in run details.
* Improved Members tables by keeping email addresses on one line, aligning status pills across rows, and revealing full email addresses on hover or focus.
* Fixed the agent selection dropdown to include all available environments, including those previously missing.
* Added the ability to add an agent to an existing evaluator directly from the evaluator empty state.
* Fixed Engine to exclude `.github/workflows/` files from fix commits that GitHub would reject and describe required workflow changes as manual steps, preventing the entire fix from being lost.
* Fixed shared Fleet agents' current-user context to use the running user's name and email instead of the creator's saved values, including in headless and LangGraph SDK runs.
* Updated the horizontal Dashboards tab in Monitoring to Analytics to distinguish it from Dashboards in the sidebar.
* Added support for ranking top-K groups in run analytics by total cost as well as run count, with run count as the default when no ranking metric is specified.
* Improved experiment headers at narrow widths by keeping progress indicators and Git metadata readable and wrapping controls below the title instead of crowding it.

**Download the Helm chart:** [`langsmith-0.18.0-rc.24.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.18.0-rc.24/langsmith-0.18.0-rc.24.tgz)

**2026-10-13**

## langsmith-0.18.0-rc.23

**LangSmith version:** `0.18.10rc1`

* This release packages the same LangSmith application version as langsmith-0.18.0-rc.22. Refer to the [langsmith-0.18.0-rc.22](#langsmith-0-18-0-rc-22) release notes below.

**Download the Helm chart:** [`langsmith-0.18.0-rc.23.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.18.0-rc.23/langsmith-0.18.0-rc.23.tgz)

**2026-10-13**

## langsmith-0.17.11

**LangSmith version:** `0.17.38`

* This release packages the same LangSmith application version as langsmith-0.17.10. Refer to the [langsmith-0.17.10](#langsmith-0-17-10) release notes below.

**Download the Helm chart:** [`langsmith-0.17.11.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.11/langsmith-0.17.11.tgz)

**2026-10-13**

## langsmith-0.18.0-rc.22

**LangSmith version:** `0.18.10rc1`

* Added ScaleDown to the LLM Gateway simulator UI.
* Updated AI search selection to preserve the existing query and add a separate AI search row for populated search scopes, while empty scopes still switch to AI search in place.
* If you reached a Memorystore Cluster discovery endpoint through extra environment variables, move the endpoint to `redis.external.cluster.nodeUris` (for example, `redis://<discovery endpoint>:6379`) before upgrading.
* Updated Redis Cluster mode to seed from node URIs or, if none are configured, from the Redis connection URL (such as a Memorystore discovery endpoint or ElastiCache configuration endpoint), then discover the other nodes.
* Updated IAM-authenticated Redis Cluster connections to honor `redis.external.cluster.tlsEnabled` for `redis://` node URIs.
* Removed the redundant "Go to traces" shortcut from the Engine page.
* Updated the sandbox JuiceFS formatter to use `access-key` and `secret-key` from the JuiceFS configuration Secret, enabling self-hosted sandboxes to store data in S3-compatible object stores such as MinIO or in Azure Blob Storage using a storage account key instead of workload identity.
* Fixed the LLM Gateway to preserve tool-result images when translating between Anthropic and Responses API formats, preventing translation failures for Claude Code image reads on Responses API routes, including `bedrock/openai` models.
* Updated the consent and device activation screens to preselect the last-chosen organization or the organization in use in LangSmith and support searching organizations when changing the selection.
* Added support for self-hosted sandboxes to reach private addresses, such as internal Git servers or databases, when `allow_list` names the host or IP explicitly. Other private addresses stay blocked, and wildcard entries do not grant access.
* Added support for `encryption.kms_key` on mounts so S3 mounts encrypt every upload with the specified KMS key using SSE-KMS, and fixed writable S3 mounts on buckets with SSE-KMS default encryption to prevent upload deletion after a checksum mismatch.
* Added support for addressing self-hosted sandbox egress proxies by an in-cluster Service name, such as `squid.proxy.svc.cluster.local`. An invalid proxy setting now stops `sandbox-host` at startup instead of failing each sandbox creation.
* Updated ScaleDown requests to `/v1/chat/completions` through the LLM Gateway to appear as `scaledown.chat.completions` runs with the operation as the model, token usage, and cost.
* Added support for calling ScaleDown through unified LLM Gateway routes with `scaledown/<operation>` models, such as `scaledown/summarize` on `/v1/chat/completions` and Decisions models such as `scaledown/classify-1` on `/v1/systemone`.

**Download the Helm chart:** [`langsmith-0.18.0-rc.22.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.18.0-rc.22/langsmith-0.18.0-rc.22.tgz)

**2026-10-13**

## langsmith-0.18.0-rc.21

**LangSmith version:** `0.18.8rc1`

* This release packages the same LangSmith application version as langsmith-0.18.0-rc.19. Refer to the [langsmith-0.18.0-rc.19](#langsmith-0-18-0-rc-19) release notes below.

**Download the Helm chart:** [`langsmith-0.18.0-rc.21.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.18.0-rc.21/langsmith-0.18.0-rc.21.tgz)

**2026-10-13**

## langsmith-0.17.10

**LangSmith version:** `0.17.38`

* Updated the app to load syntax highlighting on demand instead of preloading it on every page, reducing background asset requests.

**Download the Helm chart:** [`langsmith-0.17.10.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.10/langsmith-0.17.10.tgz)

**2026-10-12**

## langsmith-0.17.9

**LangSmith version:** `0.17.36`

* Self-hosted sandbox egress proxies can be addressed by an in-cluster Service name, such as `squid.proxy.svc.cluster.local`. An invalid proxy setting now stops `sandbox-host` at startup instead of failing each sandbox creation.

**Download the Helm chart:** [`langsmith-0.17.9.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.9/langsmith-0.17.9.tgz)

**2026-10-12**

## langsmith-0.17.8

**LangSmith version:** `0.17.35`

* On self-hosted installs, a sandbox can reach a private address, such as an internal Git server or database, when its `allow_list` names the host or IP explicitly. Other private addresses stay blocked, and wildcard entries do not open them.
* Mounts accept `encryption.kms_key`. S3 mounts encrypt every upload with that KMS key using SSE-KMS, and writable S3 mounts on buckets whose default encryption is SSE-KMS no longer delete uploads after a checksum mismatch.
* The sandbox JuiceFS formatter now uses the `access-key` and `secret-key` from the JuiceFS configuration Secret, so self-hosted sandboxes can store data in S3-compatible object stores such as MinIO, or in Azure Blob Storage with a storage account key instead of workload identity.

**Download the Helm chart:** [`langsmith-0.17.8.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.8/langsmith-0.17.8.tgz)

**2026-10-12**

## langsmith-0.18.0-rc.20

**LangSmith version:** `0.18.8rc1`

* This release packages the same LangSmith application version as langsmith-0.18.0-rc.19. Refer to the [langsmith-0.18.0-rc.19](#langsmith-0-18-0-rc-19) release notes below.

**Download the Helm chart:** [`langsmith-0.18.0-rc.20.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.18.0-rc.20/langsmith-0.18.0-rc.20.tgz)

**2026-10-12**

## langsmith-0.17.7

**LangSmith version:** `0.17.33`

* This release packages the same LangSmith application version as langsmith-0.17.6. Refer to the [langsmith-0.17.6](#langsmith-0-17-6) release notes below.

**Download the Helm chart:** [`langsmith-0.17.7.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.7/langsmith-0.17.7.tgz)

**2026-10-12**

## langsmith-0.18.0-rc.19

**LangSmith version:** `0.18.8rc1`

* Sandbox connections routed through an upstream forward proxy now pass a half-close on to the destination, so protocols that wait for end of input before replying no longer hang, including through an HTTPS proxy.
* Compute size, database size, and the scale-down period moved from a separate Scaling button to the deployment settings pane. Saving a scaling change redeploys, and the Save button indicates this.
* Hovering over a filter scope displays its preview. The scope selector stays compact until you hover over an option.
* Self-hosted LangSmith prevents deletion of the workspace that owns Engine sandboxes while Engine is deployed. To delete it, configure another Engine sandbox workspace or disable Engine first.
* GitHub repository pickers load each page of repositories with a single GitHub request instead of re-listing the whole installation, so large installations load much faster. The deployment repository picker shows repositories as each page arrives.
* Feedback chips stay visible while thread details load. Thread feedback queries run faster, and the Details pane reads feedback for the selected run.
* Noul answer scales show false and true endpoint descriptions, including for fractional answers.
* The dataset examples table, shared dataset view, and experiment comparison view preview the input field that best distinguishes examples, instead of the first field in storage order.
* The Custom headers section in a deployment's Connect dialog shows header values in plain text, marks the field that needs fixing, and rejects header names and values the browser cannot send.
* Organization administration checks dedicated permissions for membership, roles, service keys, authentication, security settings, and audit logs. Organization Admin and Operator keep their existing access.
* Studio's custom headers editors have a YAML view that accepts YAML or JSON. Pasting a cURL command imports its headers.
* The deployment Overview shows a Revisions card under Details, with the latest revision pinned and earlier revisions below. Traces are one click away from the Details card, and the separate Revisions tab is removed.
* Additional tool descriptions and unknown tool definitions respect the input Markdown setting.
* Model prices previously reached self-hosted installs only through a migration, so a new or corrected price waited for a full update. A licensed instance now pulls current prices from beacon every hour, with nothing to configure. An instance that does not phone home never calls out, and prices set by users still take precedence.
* Workspace provisioning, data planes, private networking, and operational controls check dedicated organization permissions. Existing Organization Admin and Operator access is preserved.
* Each annotation queue rubric item saves the feedback config it uses: the key's enforced config when there is one, otherwise the config picked or created in the queue form. The annotation queue API returns this as `feedback_config_id` on each rubric item, and feedback config responses include their `id`.
* Sandbox egress through an upstream forward proxy sends plain HTTP as standard forward-proxy requests instead of CONNECT tunnels, so proxies that refuse CONNECT to port 80 work. `noProxy` follows standard `NO_PROXY` matching, including subdomains of bare domains, IP addresses, and CIDR ranges.
* Command-click or Ctrl-click on a trace in the traces table opens it in a new tab. A regular click still opens the side panel.
* When an application asks for API or MCP access, the consent screen preselects a default workspace: the one you chose last time, or else the one you last used. You can still change it, and the application can work in any workspace you can access in the organization.
* Partial annotation queue updates preserve omitted reviewer count and reservation settings, so queues no longer complete after fewer reviews than configured.
* Experiments started from the Playground write every run to the experiment by ID, so renaming the experiment while it runs no longer leaves runs stuck in pending or moves them to a project under the old name.
* Semantic run, trace, and thread queries have configurable limits per endpoint, workspace, and authentication source. YAML rules support workspace-specific limits and dry-run mode. Requests above an enforced limit return HTTP 429 with a `Retry-After` header.
* The device authorization response includes `verification_uri_complete`, which opens the activation page with the code already filled in, so you only need to check that it matches the one in your terminal.
* Creating or reusing internal tracing projects, such as playground and evaluators, no longer creates agents. Renaming an agent-owned project to a reserved internal name returns a clear conflict error.

**Download the Helm chart:** [`langsmith-0.18.0-rc.19.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.18.0-rc.19/langsmith-0.18.0-rc.19.tgz)

**2026-10-08**

## langsmith-0.18.0-rc.18

**LangSmith version:** `0.18.6rc1`

* This release packages the same LangSmith application version as langsmith-0.18.0-rc.17. Refer to the [langsmith-0.18.0-rc.17](#langsmith-0-18-0-rc-17) release notes below.

**Download the Helm chart:** [`langsmith-0.18.0-rc.18.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.18.0-rc.18/langsmith-0.18.0-rc.18.tgz)

**2026-10-08**

## langsmith-0.18.0-rc.17

**LangSmith version:** `0.18.6rc1`

* OpenAI Responses traces render `additional_tools` as expandable tool definitions under a Developer message, keeping their role in the trace view.
* Studio chat shows images, files, and text documents that agents return as LangChain v1 content blocks, and you can preview them as attachments.
* You can invoke OpenAI Decisions through the LLM Gateway using your workspace's OpenAI credentials and gateway policies, including model access lists. Requests and responses keep their native formats.
* Copying a TypeSafe answer preserves all fields from the traced response without adding display-only fields.
* Links to the former Engine tab in tracing projects redirect to the project's Engine page, preserving the selected issue and view.
* Claude Haiku 5.5 is available in Playground and gateway model configurations for Anthropic, Bedrock, and Vertex AI.
* Organization settings use more granular access permissions for each field. Organization Admins and Operators keep their existing access.
* The Gateway simulator's View Trace link opens the request in the Gateway Traces tab instead of the tracing project.
* Polly opens in a resizable side pane instead of a floating chat window, and opening Polly collapses the left navigation to give you more space.
* Insights jobs report an error when parent-category generation fails, instead of publishing a report with placeholder categories.
* Sandbox creation and filesystem updates enforce a 640 GiB maximum capacity by default. Operators can set a different limit in bytes with `SANDBOX_MAX_FS_CAPACITY_BYTES`.
* The platform backend waits up to 30 seconds for Redis to accept connections before it runs license checks and loads queue scripts. This prevents crash loops in self-hosted deployments while Redis or the Istio sidecar is still starting.

**Download the Helm chart:** [`langsmith-0.18.0-rc.17.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.18.0-rc.17/langsmith-0.18.0-rc.17.tgz)

**2026-10-08**

## langsmith-0.18.0-rc.16

**LangSmith version:** `0.18.5rc1`

* This release packages the same LangSmith application version as langsmith-0.18.0-rc.14. Refer to the [langsmith-0.18.0-rc.14](#langsmith-0-18-0-rc-14) release notes below.

**Download the Helm chart:** [`langsmith-0.18.0-rc.16.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.18.0-rc.16/langsmith-0.18.0-rc.16.tgz)

**2026-10-08**

## langsmith-0.17.6

**LangSmith version:** `0.17.33`

* Self-hosted deployments can run Engine with FIPS-validated cryptographic providers using the `langsmith-insights-engine-fips` image.

**Download the Helm chart:** [`langsmith-0.17.6.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.6/langsmith-0.17.6.tgz)

**2026-10-08**

## langsmith-0.17.5

**LangSmith version:** `0.17.32`

* Sandbox hosts can route outbound TCP, HTTP, and HTTPS connections through an operator-configured HTTP or HTTPS forward proxy, set with `sandboxes.authProxy.httpProxy` in the self-hosted chart. Hosts listed in `noProxy` are dialed directly, and an HTTPS proxy is trusted through `config.customCa`.

**Download the Helm chart:** [`langsmith-0.17.5.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.5/langsmith-0.17.5.tgz)

**2026-10-08**

## langsmith-0.17.4

**LangSmith version:** `0.17.31`

* Delegated sandboxes can reach a private LangSmith API.
* Self-hosted installations using `authType: mixed` with OIDC SSO and basic auth disabled now authenticate every remote MCP tool, including dataset, workspace, and run tools that previously returned `401 Invalid token`.
* Deleted deployments begin cleanup without an artificial delay, and their names become available for reuse once cleanup finishes.
* The self-hosted frontend image now uses the same code-split build as LangSmith cloud. The first page load downloads compressed JavaScript of about 1 MB, down from about 9 MB, and other pages load their code on demand. Assets are precompressed at image build time, content-hashed assets get an immutable browser cache policy, and HTML stays uncached so runtime configuration stays fresh. Browser tabs left open across an upgrade reload once when they open a page whose code changed. Deployments that enable `frontend.includeNonce` with a strict `style-src` policy also apply the nonce to stylesheets loaded on demand.

**Download the Helm chart:** [`langsmith-0.17.4.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.4/langsmith-0.17.4.tgz)

**2026-10-07**

## langsmith-0.18.0-rc.14

**LangSmith version:** `0.18.5rc1`

* Self-hosted sandboxes on Azure can connect to the JuiceFS metadata Redis with Microsoft Entra ID through Azure Workload Identity, so Azure Managed Redis can run with access keys disabled. Add `?auth-provider=azure` to a `rediss://` `sandboxes.juicefs.redis.metaURL` with no username or password.
* OAuth applications registered under **Settings** > **OAuth applications** can use one access token for both the LangSmith API and the Remote MCP server, instead of authorizing each separately. BYOC data planes still accept only tokens issued for their own MCP server.
* You can download all rows matching the current tab, search, and filters from Organization Members and API Keys. Exports preserve existing visibility restrictions and include only key metadata, never full API keys.
* A deployment's details appear in a Details card below the trace chart on its Overview tab, so every other tab uses the full page width. The card groups them into Agent Server (URL and version), Source, Runtime (deployment type, compute and database size), and Identifiers (copyable deployment and active revision IDs), with hints that explain the less obvious fields.
* The Source section of a deployment's Details card matches how the deployment was built. A GitHub deployment shows its repository, the branch or tag it tracks, and whether pushes auto-deploy. A Docker deployment shows its image, and a CLI-uploaded deployment notes that it was deployed with `langgraph deploy`. A nested LangGraph config file or Managed Deep Agents project directory links straight to it.
* Canceling or rolling back a resume run before its first checkpoint keeps the thread interrupted instead of idle, and the canceled run records why it was canceled.
* Creating an evaluator that uses a TypeSafe Compatible Endpoint no longer fails with `Manifest type langchain.schema.runnable.RunnableSequence is not supported`.
* Triggering a run rule by hand returns 422 when the deployment cannot run it, for example, a rule that reads ClickHouse while ClickHouse querying is disabled, or a trajectory rule on a data plane without a trajectory service. Previously, the trigger was accepted and silently did nothing.
* Thread details display newly ingested traces as soon as their runs are available, even before the thread listing catches up. When a turn number is unavailable, a refresh button lets you check again.
* The deployment Monitoring tab shows trace count, latency, and error rate alongside server metrics, all driven by one time range. The Overview tab no longer has the trace count chart, so deployment details appear first.
* Self-hosted installations using `authType: mixed` with OIDC SSO and basic auth disabled now authenticate every remote MCP tool, including dataset, workspace, and run tools that previously returned `401 Invalid token`.
* The new LangSmith experience welcome modal appears once on any authenticated page for users in migrated workspaces, rather than only on All Agents.
* Workspace deletion batches project cleanup to avoid request-size errors when a workspace has more than 100 agent-owned tracing projects.
* LangSmith restores the most recently used organization and workspace separately for each login identity, including separate SSO and regular logins. Saved preferences survive logout and session expiry.
* The sandbox list scrolls within the page, so you can reach sandboxes below the visible rows.
* Studio loads child run inputs and outputs when converting a trace into thread state. Cloned threads keep the values recorded by each graph node.
* ClickHouse migration jobs report connection errors and HTTP status codes instead of only a readiness timeout. TLS readiness checks use the backend's CA directory alongside the configured CA bundle.
* Traces sent to the OpenTelemetry endpoint are rejected with a 429 once the workspace reaches its monthly trace limit, matching the other ingestion endpoints. Multipart and OpenTelemetry ingestion also count toward the hourly ingested-events and payload-size limits.
* Sandbox S3 mounts correctly sign requests for object keys that contain spaces, punctuation, and non-ASCII characters, avoiding signature mismatch errors when reading these files.
* Delegated sandboxes can reach a private LangSmith API.
* The self-hosted frontend image now uses the same code-split build as LangSmith cloud. The first page load downloads compressed JavaScript of about 1 MB, down from about 9 MB, and other pages load their code on demand. Assets are precompressed at image build time, content-hashed assets get an immutable browser cache policy, and HTML stays uncached so runtime configuration stays fresh. Browser tabs left open across an upgrade reload once when they open a page whose code changed. Deployments that enable `frontend.includeNonce` with a strict `style-src` policy also apply the nonce to stylesheets loaded on demand.
* Edit a deployment's custom headers under Custom headers in the Connect dialog instead of the Settings dialog. They are still stored only in your browser.
* Set `sandboxes.juicefs.redis.iamAuthProvider: azure` to use Microsoft Entra ID for the JuiceFS metadata Redis, the same way `redis.external.iamAuthProvider` configures core LangSmith Redis. This also works with a customer-managed metadata URL Secret.
* The ingest queue sets its Go memory limit to 90% of its container memory limit by default, so garbage collection frees memory before a pod reaches its limit and is OOM-killed. To change the ratio, set `AUTOMEMLIMIT` in `ingestQueue.deployment.extraEnv`, or set it to `off` to disable it. An explicit `GOMEMLIMIT` still takes precedence.
* Feedback comments and evaluator reasoning render Markdown, so headings, lists, bold text, and line breaks display formatted in trace, annotation queue, and experiment views.
* `GET /api/v2/runs/{run_id}` returns the "run exceeds the response size limit" error.
* Insights jobs using Fireworks include the request-scoped LangSmith authentication header when the LLM auth proxy is enabled.
* When a model's configuration includes a parameter the provider does not accept, the Playground names that parameter instead of showing a generic "Failed to call model" error.
* Trajectory evaluators show supported filters from both tracing projects and the evaluator library, and preserve them when saved and reopened. You must remove unsupported trace and tree filters before saving.
* The default sandbox image ships apt's package indexes and caches, so `apt-get install` works without a prior `apt-get update` and apt commands start faster. Run `apt-get update` first to get the latest package versions.
* The permissions UI labels built-in roles as Workspace Admin, Workspace Editor, and Workspace Viewer to distinguish them from organization roles.
* Deleted deployments begin cleanup without an artificial delay, and their names become available for reuse once cleanup finishes.
* View your workspace's Gateway traces directly from the LLM Gateway, and open filtered traces from the Usage drilldown without selecting an agent.
* Insights reports using Claude Sonnet 5.5 on Amazon Bedrock generate summaries without unsupported forced tool choice errors.
* Run, trace, and thread query responses include query metadata with semantic match scores when a semantic filter is used. Trace query metadata appears directly on each trace item.
* Bulk deleting prompts skips restricted-mode prompts the caller does not own and reports them as failed, matching single-prompt deletes.
* Studio chat accepts TXT, CSV, TSV, Markdown, and JSON attachments, sends them to the agent, and previews their text. Unsupported files show an error instead of silently blocking Send.
* When a model preset with a custom API key name is the Playground default, the Playground uses that key name on load instead of falling back to the provider's default key, such as `OPENAI_API_KEY`.
* The Reviewer Notes section in annotation queues is a single note per reviewer that saves automatically while you type. It replaces the send button and the list of posted notes.
* Files dropped onto the Studio chat composer attach the same way as files picked with the upload button.
* Self-hosted deployments can run Engine with FIPS-validated cryptographic providers using the `langsmith-insights-engine-fips` image.
* The evaluator overview shows what each prompt variable is mapped to, or "unmapped variable" when it is not mapped, instead of auto-generated names like `var1`.
* Sandbox hosts can route outbound TCP, HTTP, and HTTPS connections through an operator-configured HTTP or HTTPS forward proxy, set with `sandboxes.authProxy.httpProxy` in the self-hosted chart. Hosts listed in `noProxy` are dialed directly, and an HTTPS proxy is trusted through `config.customCa`.
* Dataset example details refresh nested output values when you switch between examples.
* Bedrock model configurations can use automatic routing or explicitly select the Bedrock Runtime or Bedrock Mantle endpoint. This supports models available through both endpoints when AWS permissions allow only one.
* API requests return HTTP 429 instead of HTTP 503 when the query service reports exhausted resources, so clients can handle throttling correctly.
* OAuth providers that use HTTP Basic client authentication encode the client ID and secret as the OAuth spec requires, so secrets containing characters such as `:`, `%`, or `+` no longer fail at the token endpoint.
* When reading a thread's or run's events fails, event streams end with an `error` frame instead of closing as if they had finished. This covers `POST /threads/{thread_id}/stream/events` (SSE and WebSocket) and the v1 thread and run streaming endpoints. The `/wait` endpoints now fail instead of returning partial state as the final result.
* The gear button on a deployment opens settings in a side pane instead of a dialog, with General, Source, and LLM Gateway sections and one Save button. Closing the pane with unsaved changes asks before discarding them.
* The Submit button on the new deployment form is disabled while the deployment is being created, so clicking it again no longer sends a second create request.
* Claude Sonnet 5.5, Claude Opus 5.5, GPT-6.1 Sol, and Gemini 3.8 Flash are available as directly selectable models in Fleet and Agent Builder. The new Claude models run with adaptive thinking.

**Download the Helm chart:** [`langsmith-0.18.0-rc.14.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.18.0-rc.14/langsmith-0.18.0-rc.14.tgz)

**2026-10-07**

## langsmith-0.18.0-rc.13

**LangSmith version:** `0.18.4rc1`

* This release packages the same LangSmith application version as langsmith-0.18.0-rc.8. Refer to the [langsmith-0.18.0-rc.8](#langsmith-0-18-0-rc-8) release notes below.

**Download the Helm chart:** [`langsmith-0.18.0-rc.13.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.18.0-rc.13/langsmith-0.18.0-rc.13.tgz)

**2026-10-07**

## langsmith-0.17.3

**LangSmith version:** `0.17.30`

* This release packages the same LangSmith application version as langsmith-0.17.1. Refer to the [langsmith-0.17.1](#langsmith-0-17-1) release notes below.

**Download the Helm chart:** [`langsmith-0.17.3.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.3/langsmith-0.17.3.tgz)

**2026-10-06**

## langsmith-0.18.0-rc.12

**LangSmith version:** `0.18.4rc1`

* This release packages the same LangSmith application version as langsmith-0.18.0-rc.8. Refer to the [langsmith-0.18.0-rc.8](#langsmith-0-18-0-rc-8) release notes below.

**Download the Helm chart:** [`langsmith-0.18.0-rc.12.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.18.0-rc.12/langsmith-0.18.0-rc.12.tgz)

**2026-10-06**

## langsmith-0.18.0-rc.11

**LangSmith version:** `0.18.4rc1`

* This release packages the same LangSmith application version as langsmith-0.18.0-rc.8. Refer to the [langsmith-0.18.0-rc.8](#langsmith-0-18-0-rc-8) release notes below.

**Download the Helm chart:** [`langsmith-0.18.0-rc.11.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.18.0-rc.11/langsmith-0.18.0-rc.11.tgz)

**2026-10-06**

## langsmith-0.18.0-rc.10

**LangSmith version:** `0.18.4rc1`

* This release packages the same LangSmith application version as langsmith-0.18.0-rc.8. Refer to the [langsmith-0.18.0-rc.8](#langsmith-0-18-0-rc-8) release notes below.

**Download the Helm chart:** [`langsmith-0.18.0-rc.10.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.18.0-rc.10/langsmith-0.18.0-rc.10.tgz)

**2026-10-06**

## langsmith-0.17.2

**LangSmith version:** `0.17.30`

* This release packages the same LangSmith application version as langsmith-0.17.1. Refer to the [langsmith-0.17.1](#langsmith-0-17-1) release notes below.

**Download the Helm chart:** [`langsmith-0.17.2.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.2/langsmith-0.17.2.tgz)

**2026-10-06**

## langsmith-0.16.41

**LangSmith version:** `0.16.70`

* This release packages the same LangSmith application version as langsmith-0.16.40. Refer to the [langsmith-0.16.40](#langsmith-0-16-40) release notes below.

**Download the Helm chart:** [`langsmith-0.16.41.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.16.41/langsmith-0.16.41.tgz)

**2026-10-06**

## langsmith-0.16.40

**LangSmith version:** `0.16.70`

* Internal improvements and maintenance updates.

**Download the Helm chart:** [`langsmith-0.16.40.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.16.40/langsmith-0.16.40.tgz)

**2026-10-05**

## langsmith-0.18.0-rc.9

**LangSmith version:** `0.18.4rc1`

* This release packages the same LangSmith application version as langsmith-0.18.0-rc.8. Refer to the [langsmith-0.18.0-rc.8](#langsmith-0-18-0-rc-8) release notes below.

**Download the Helm chart:** [`langsmith-0.18.0-rc.9.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.18.0-rc.9/langsmith-0.18.0-rc.9.tgz)

**2026-10-05**

## langsmith-0.18.0-rc.8

**LangSmith version:** `0.18.4rc1`

* Internal improvements and maintenance updates.

**Download the Helm chart:** [`langsmith-0.18.0-rc.8.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.18.0-rc.8/langsmith-0.18.0-rc.8.tgz)

**2026-10-05**

## langsmith-0.17.1

**LangSmith version:** `0.17.30`

* Evaluator tests show configuration errors, such as a missing compatible endpoint URL, directly in the evaluator panel.
* Self-hosted sandboxes on Azure can connect to the JuiceFS metadata Redis with Microsoft Entra ID through Azure Workload Identity, so Azure Managed Redis can run with access keys disabled. Add `?auth-provider=azure` to a `rediss://` `sandboxes.juicefs.redis.metaURL` with no username or password.

**Download the Helm chart:** [`langsmith-0.17.1.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.1/langsmith-0.17.1.tgz)

**2026-10-03**

## langsmith-0.17.0-rc.65

**LangSmith version:** `0.17.29`

* Editing a Context Hub webhook loads its saved custom headers instead of unrelated response headers, so saving no longer overwrites them.
* Self-hosted Insights deployments can opt in to Google Application Default Credentials for Vertex AI models instead of storing service account JSON.
* Self-hosted LangSmith Chat can authenticate Vertex AI workspace models with Google Application Default Credentials when no stored service account credential or LLM auth proxy credential is available.
* Custom Apps offers browser creation and editing only when sandbox service URLs and signing keys are configured, preventing provisioning failures on incompletely configured deployments.
* Self-hosted LangSmith operators can allowlist exact OpenAI-compatible endpoints and Azure scopes, so Playground and evaluator calls authenticate with refreshable Azure workload identity tokens.
* The Messages view shows the user message on OpenAI Responses API calls that send it as a plain string, which is how calls chained with `previous_response_id` or a conversation send each new turn. Previously, those user messages were dropped.
* The model configuration editor and Gateway homepage code samples explain that Gateway applies model and connection settings, while generation parameters such as max tokens and temperature must be set in API requests.
* On self-hosted and BYOC deployments, organization admins can choose which model providers Engine runs on, see whether each provider's keys are ready, and add missing keys from **Settings** > **Engine** > **Model providers**.
* V1 dashboard legends stay within their chart cards on ClickHouse deployments. Extra series are available in a menu when the legend runs out of space.
* LLM-as-a-judge evaluators using Claude Opus 5.5 or Sonnet 5.5 on AWS Bedrock no longer fail because of unsupported forced tool choice.
* Air-gapped self-hosted installs cannot get Engine's rates, so Engine settings, project settings, and the Engine overview say that spend is not available instead of showing local estimates. Spend limits are not enforced on those installs, although a project or organization limit of 0 still pauses Engine.
* Engine accepts operator-configured GitHub App page URLs without restricting their path layout, including enterprise-scoped GitHub Enterprise Cloud Apps.
* LLM-as-a-judge evaluators whose prompt carries both an old and a current output schema check scores against the schema the judge actually used, so scores are saved and errors are recorded under the right feedback keys.
* Replacing a dataset's examples in one request with `PUT /v1/platform/datasets/{dataset_id}/examples` succeeds again when it updates existing examples. Previously, it returned a 500 error on installs using the newer examples storage, including fresh self-hosted installs.
* Sorting tracing projects by Most Recent Run orders projects whose runs reference dataset examples by their latest run, instead of grouping them with empty projects.
* Trace ingestion puts less load on Redis by reusing model pricing data more efficiently, while preserving custom pricing and calculated costs.
* When a customer-hosted model provider rejects an Engine scan, the project page explains whether credentials, model access, or provider quota needs attention.
* Google Vertex AI model configurations route Anthropic Claude models to Vertex's native Anthropic Messages API, while Gemini and open models continue to use the OpenAI-compatible endpoint. Existing bare Claude IDs still work, and publisher-qualified IDs are normalized automatically.
* Creating a public trace or thread share link requires permission to read the runs, including their inputs and outputs.
* The LLM Gateway applies existing custom provider fallback policies when you call a saved model configuration through a unified endpoint. Existing policies work without modification, and explicit model configuration policies take precedence.
* LangSmith Chat can take about four times as many steps in one turn, so a large custom app build can finish instead of ending with a "Recursion limit of 250 reached" error.
* Deleting a tracing project removes its agent environment when no runtime is attached. Agent reads continue to work when the Production environment is removed.
* Clicking Test on a thread or trajectory evaluator shows export and validation failures instead of appearing to do nothing.
* Self-hosted Engine can opt in to native Amazon Bedrock Runtime with an explicitly configured system inference profile for Engine's model. Mantle remains the default for all credential types, and Engine never automatically selects a global profile.
* Self-hosted Engine's GitHub App settings use `ENGINE_GITHUB_*` names, such as `ENGINE_GITHUB_APP_ID` and `ENGINE_GITHUB_APP_PRIVATE_KEY`. The previous `FORGE_GITHUB_*` names still work and apply when the new name is unset or empty.

**Download the Helm chart:** [`langsmith-0.17.0-rc.65.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.0-rc.65/langsmith-0.17.0-rc.65.tgz)

**2026-10-02**

## langsmith-0.18.0-rc.7

**LangSmith version:** `0.18.2rc1`

* This release packages the same LangSmith application version as langsmith-0.18.0-rc.1. Refer to the [langsmith-0.18.0-rc.1](#langsmith-0-18-0-rc-1) release notes below.

**Download the Helm chart:** [`langsmith-0.18.0-rc.7.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.18.0-rc.7/langsmith-0.18.0-rc.7.tgz)

**2026-10-02**

## langsmith-0.18.0-rc.6

**LangSmith version:** `0.18.2rc1`

* Internal improvements and maintenance updates.

**Download the Helm chart:** [`langsmith-0.18.0-rc.6.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.18.0-rc.6/langsmith-0.18.0-rc.6.tgz)

**2026-10-02**

## langsmith-0.17.0-rc.64

**LangSmith version:** `0.17.29rc7`

* This release packages the same LangSmith application version as langsmith-0.17.0-rc.61. Refer to the [langsmith-0.17.0-rc.61](#langsmith-0-17-0-rc-61) release notes below.

**Download the Helm chart:** [`langsmith-0.17.0-rc.64.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.0-rc.64/langsmith-0.17.0-rc.64.tgz)

**2026-10-02**

## langsmith-0.17.0-rc.63

**LangSmith version:** `0.17.29rc7`

* This release packages the same LangSmith application version as langsmith-0.17.0-rc.61. Refer to the [langsmith-0.17.0-rc.61](#langsmith-0-17-0-rc-61) release notes below.

**Download the Helm chart:** [`langsmith-0.17.0-rc.63.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.0-rc.63/langsmith-0.17.0-rc.63.tgz)

**2026-10-02**

## langsmith-0.17.0-rc.62

**LangSmith version:** `0.17.29rc7`

* This release packages the same LangSmith application version as langsmith-0.17.0-rc.61. Refer to the [langsmith-0.17.0-rc.61](#langsmith-0-17-0-rc-61) release notes below.

**Download the Helm chart:** [`langsmith-0.17.0-rc.62.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.0-rc.62/langsmith-0.17.0-rc.62.tgz)

**2026-10-02**

## langsmith-0.17.0

**LangSmith version:** `0.17.29`

LangSmith v0.17 is the recommended release for self-hosted deployments. Upgrade to get the latest security updates, product improvements, and bug fixes.

### Breaking changes

* Pagination using `limit` and `offset` is deprecated for sandbox and snapshot listings.
* Self-hosted bulk exports now default to `zstandard` compression when the `compression` parameter is omitted at creation time. Previously, the default was `gzip`. To override this default in the Helm chart, see [Compression](../../../Monitor/Debug/Bulk%20export%20trace%20data/Bulk%20export%20trace%20data.md#compression).
* Creating a tracing project through tracing operations now requires both `projects:create` and `runs:create`. Previously, only `runs:create` was required.
* For installations with SmithDB enabled:
  * The default cache now uses a PersistentVolumeClaim per pod instead of a local SSD `emptyDir`. To keep local SSD storage, apply the v0.17 local SSD values before upgrading. See [Cache storage](../SmithDB/Install%20SmithDB/Prepare%20SmithDB%20supporting%20infrastructure.md#cache-storage).
  * HPA settings for query, ingestion, and compaction workers now live under `autoscaling.hpa.*`.
  * Migration Job settings moved from `smithdb.migration.deployment` to `smithdb.migration.job`, with the same keys. See [Migrate ClickHouse history to SmithDB](../SmithDB/Install%20SmithDB/Migrate%20ClickHouse%20history%20to%20SmithDB.md).
  * Metrics now default to the `critical` profile. Set `SMITHDB_<SERVICE>__METRICS__MODE=all` in `smithdb.commonEnv` to export every metric family.
* JuiceFS moved into the `sandbox-host` deployment. Move any associated permissions and workload identity configuration to that deployment.
* Blob storage is required starting in v0.18. Set up blob storage before upgrading to that version.

### LangSmith Engine

* [Engine](../../../Engine/LangSmith%20Engine.md) supports bring-your-own-key (BYOK). Find and fix agent issues while keeping data in your environment and making model calls with your own provider key.
* Engine detects inefficient agent work to help reduce latency and LLM costs.

### LLM Gateway

* Manage [spend limits](../../../LLM%20Gateway/Governance/Spend%20policies.md), [rate limits](../../../LLM%20Gateway/Governance/Rate%20limit%20policies.md), [model access policies](../../../LLM%20Gateway/Governance/Model%20access%20policies.md), and [sensitive data handling](../../../LLM%20Gateway/Governance/Data%20policies.md).
* Configure cross-provider [model fallbacks](../../../LLM%20Gateway/Models%20and%20reliability/Model%20fallbacks.md), including translation between OpenAI and Anthropic API formats.
* Scope spend caps and rate limits by custom `X-Gateway-*` headers, such as [per customer or team](../../../LLM%20Gateway/Governance/Header-based%20policies.md).

### Access control and security

* Configure [organization-scoped model configurations](../../Govern/Organization/Workspace%20setup/Manage%20model%20configurations.md#organization-wide-provider-control) and model provider secrets.
* Use the [Organization Restricted role](../../Govern/Users%20%26%20access%20control/Role-based%20access%20control.md#organization-restricted) to give contractors and partners workspace access without exposing billing, settings, or usage.
* Organization Admins and Operators can [deactivate and reactivate members' personal access tokens](../../Account/Create%20an%20account%20and%20API%20key.md#deactivate-or-delete-a-personal-access-token).

### Sandboxes

* Sandboxes are generally available in all clouds.
* Sandboxes no longer require an explicit JuiceFS dependency.

### Observability and evaluation

* Analyze traces in the conversational trajectory view, score them with online evaluators, and add them to annotation queues and datasets.
* Build and publish [custom apps](../../../Monitor/Observe/Monitoring%20%26%20alerting/Custom%20Apps.md) for annotation, experiments, traces, and other LangSmith data using LangSmith Chat, templates, or your coding agent. Building and editing with chat requires the [self-hosted chat setup](../../../Monitor/Observe/Monitoring%20%26%20alerting/Custom%20Apps.md#configure-self-hosted-chat), including sandbox service URLs and a signing key.
* Use Jev and SemIf decision models for online and offline evaluators.
* Construct filter queries with a new, expressive query syntax and filtering interface.
* Custom charts include built-in templates, more supported metrics, and layout improvements.

### SmithDB

* [SmithDB](../SmithDB/Overview/Enable%20SmithDB%20on%20self-hosted%20LangSmith.md) is generally available on GCP, AWS, and Azure.
* Compaction workers support [KEDA scaling](../SmithDB/Install%20SmithDB/Configure%20SmithDB%20for%20scale.md#scale-with-keda-instead).
* ClickHouse support ends in v0.19. Start [migrating to SmithDB-backed SDK methods](../../../Monitor/Reference/SmithDB%20API%20migration/Migrate%20to%20SmithDB-backed%20APIs.md) before upgrading to that version.

Review the [upgrade guide](../Manage%20an%20instance/Upgrade%20an%20installation.md) before upgrading.

**Download the Helm chart:** [`langsmith-0.17.0.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.0/langsmith-0.17.0.tgz)

**2026-10-02**

## langsmith-0.16.39

**LangSmith version:** `0.16.69`

* LangSmith reduced Redis load during trace ingestion by reusing model pricing data more efficiently while preserving custom pricing and calculated costs.

**Download the Helm chart:** [`langsmith-0.16.39.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.16.39/langsmith-0.16.39.tgz)

**2026-10-02**

## langsmith-0.18.0-rc.5

**LangSmith version:** `0.18.2rc1`

* This release packages the same LangSmith application version as langsmith-0.18.0-rc.1. Refer to the [langsmith-0.18.0-rc.1](#langsmith-0-18-0-rc-1) release notes below.

**Download the Helm chart:** [`langsmith-0.18.0-rc.5.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.18.0-rc.5/langsmith-0.18.0-rc.5.tgz)

**2026-10-02**

## langsmith-0.17.0-rc.61

**LangSmith version:** `0.17.29rc7`

* LLM-as-judge evaluators whose prompts contained both an old and a current output schema now checked scores against the schema the judge actually used, so their scores were saved, and errors were recorded under the correct feedback keys.
* Replacing a dataset's examples in one request with `PUT /v1/platform/datasets/{dataset_id}/examples` succeeded again when it updated existing examples; before, it returned a 500 error on installations using the newer example storage, including fresh self-hosted installations.

**Download the Helm chart:** [`langsmith-0.17.0-rc.61.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.0-rc.61/langsmith-0.17.0-rc.61.tgz)

**2026-10-02**

## langsmith-0.17.0-rc.60

**LangSmith version:** `0.17.29rc6`

* LLM-as-a-judge evaluators using Claude Opus 5.5 or Sonnet 5.5 on AWS Bedrock no longer failed due to unsupported forced tool choice.
* Air-gapped self-hosted installs couldn't access Engine's rates, so Engine settings, project settings, and the Engine overview now indicated that spend wasn't available instead of showing local estimates; spend limits weren't enforced on those installs, though a project or organization limit of 0 still paused Engine.
* Moved the model clear button into the model config combobox.
* Engine accepted operator-configured GitHub App page URLs without restricting their path layout, including enterprise-scoped GitHub Enterprise Cloud Apps.

**Download the Helm chart:** [`langsmith-0.17.0-rc.60.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.0-rc.60/langsmith-0.17.0-rc.60.tgz)

**2026-10-01**

## langsmith-0.17.0-rc.59

**LangSmith version:** `0.17.29rc5`

* V1 dashboard legends stayed within their chart cards on ClickHouse deployments, with extra series available in a menu when the legend ran out of space.
* Trace and run lists displayed a vertical scrollbar that scrolled the table rows and reflected their position, without an extra outer scrollbar.

**Download the Helm chart:** [`langsmith-0.17.0-rc.59.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.0-rc.59/langsmith-0.17.0-rc.59.tgz)

**2026-10-01**

## langsmith-0.18.0-rc.4

**LangSmith version:** `0.18.2rc1`

* This release packages the same LangSmith application version as langsmith-0.18.0-rc.1. Refer to the [langsmith-0.18.0-rc.1](#langsmith-0-18-0-rc-1) release notes below.

**Download the Helm chart:** [`langsmith-0.18.0-rc.4.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.18.0-rc.4/langsmith-0.18.0-rc.4.tgz)

**2026-10-01**

## langsmith-0.16.38

**LangSmith version:** `0.16.68`

* This release packages the same LangSmith application version as langsmith-0.16.37. Refer to the [langsmith-0.16.37](#langsmith-0-16-37) release notes below.

**Download the Helm chart:** [`langsmith-0.16.38.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.16.38/langsmith-0.16.38.tgz)

**2026-10-01**

## langsmith-0.17.0-rc.58

**LangSmith version:** `0.17.29rc4`

* This release packages the same LangSmith application version as langsmith-0.17.0-rc.56. Refer to the [langsmith-0.17.0-rc.56](#langsmith-0-17-0-rc-56) release notes below.

**Download the Helm chart:** [`langsmith-0.17.0-rc.58.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.0-rc.58/langsmith-0.17.0-rc.58.tgz)

**2026-10-01**

## langsmith-0.18.0-rc.3

**LangSmith version:** `0.18.2rc1`

* This release packages the same LangSmith application version as langsmith-0.18.0-rc.1. Refer to the [langsmith-0.18.0-rc.1](#langsmith-0-18-0-rc-1) release notes below.

**Download the Helm chart:** [`langsmith-0.18.0-rc.3.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.18.0-rc.3/langsmith-0.18.0-rc.3.tgz)

**2026-10-01**

## langsmith-0.17.0-rc.57

**LangSmith version:** `0.17.29rc4`

* This release packages the same LangSmith application version as langsmith-0.17.0-rc.56. Refer to the [langsmith-0.17.0-rc.56](#langsmith-0-17-0-rc-56) release notes below.

**Download the Helm chart:** [`langsmith-0.17.0-rc.57.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.0-rc.57/langsmith-0.17.0-rc.57.tgz)

**2026-10-01**

## langsmith-0.17.0-rc.56

**LangSmith version:** `0.17.29rc4`

* Optionally embedded trajectory gRPC server in Smith-go.
* Self-hosted LangSmith operators could allowlist exact OpenAI-compatible endpoints and Azure scopes so Playground and evaluator calls authenticated with refreshable Azure workload identity tokens.
* The Messages view showed the user message on OpenAI Responses API calls that sent it as a plain string, which is how calls chained with previous\_response\_id or a conversation sent each new turn; previously, those user messages were dropped.
* The model configuration editor and Gateway homepage code samples explained that Gateway applies model and connection settings, while generation parameters such as max tokens and temperature must be set in API requests.
* On self-hosted and BYOC deployments, organization admins could choose which model providers Engine ran on, see whether each provider's keys were ready, and add missing keys from Settings > Engine > Model providers.

**Download the Helm chart:** [`langsmith-0.17.0-rc.56.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.0-rc.56/langsmith-0.17.0-rc.56.tgz)

**2026-10-01**

## langsmith-0.16.37

**LangSmith version:** `0.16.68`

* Internal improvements and maintenance updates

**Download the Helm chart:** [`langsmith-0.16.37.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.16.37/langsmith-0.16.37.tgz)

**2026-09-30**

## langsmith-0.17.0-rc.55

**LangSmith version:** `0.17.29rc3`

* This release packages the same LangSmith application version as langsmith-0.17.0-rc.54. Refer to the [langsmith-0.17.0-rc.54](#langsmith-0-17-0-rc-54) release notes below.

**Download the Helm chart:** [`langsmith-0.17.0-rc.55.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.0-rc.55/langsmith-0.17.0-rc.55.tgz)

**2026-09-30**

## langsmith-0.17.0-rc.54

**LangSmith version:** `0.17.29rc3`

* Edited a Context Hub webhook to load its saved custom headers instead of unrelated response headers, preventing overwriting upon saving.
* Allowed self-hosted Insights deployments to explicitly opt in to Google Application Default Credentials for Vertex AI models instead of storing service account JSON.
* Enabled self-hosted LangSmith Chat to authenticate Vertex AI workspace models with Google Application Default Credentials when no stored service account credential or LLM auth proxy credential was available.
* Offered Custom Apps browser creation and editing only when sandbox service URLs and signing keys were configured, preventing provisioning failures on incompletely configured deployments. See [Configure self-hosted chat](../../../Monitor/Observe/Monitoring%20%26%20alerting/Custom%20Apps.md#configure-self-hosted-chat) for setup requirements.

**Download the Helm chart:** [`langsmith-0.17.0-rc.54.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.0-rc.54/langsmith-0.17.0-rc.54.tgz)

**2026-09-30**

## langsmith-0.18.0-rc.2

**LangSmith version:** `0.18.2rc1`

* This release packages the same LangSmith application version as langsmith-0.18.0-rc.1. Refer to the [langsmith-0.18.0-rc.1](#langsmith-0-18-0-rc-1) release notes below.

**Download the Helm chart:** [`langsmith-0.18.0-rc.2.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.18.0-rc.2/langsmith-0.18.0-rc.2.tgz)

**2026-09-30**

## langsmith-0.17.0-rc.53

**LangSmith version:** `0.17.29rc2`

* This release packages the same LangSmith application version as langsmith-0.17.0-rc.52. Refer to the [langsmith-0.17.0-rc.52](#langsmith-0-17-0-rc-52) release notes below.

**Download the Helm chart:** [`langsmith-0.17.0-rc.53.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.0-rc.53/langsmith-0.17.0-rc.53.tgz)

**2026-09-30**

## langsmith-0.16.36

**LangSmith version:** `0.16.67`

* This release packages the same LangSmith application version as langsmith-0.16.34. Refer to the [langsmith-0.16.34](#langsmith-0-16-34) release notes below.

**Download the Helm chart:** [`langsmith-0.16.36.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.16.36/langsmith-0.16.36.tgz)

**2026-09-30**

## langsmith-0.18.0-rc.1

**LangSmith version:** `0.18.2rc1`

* The Playground no longer encountered a React nested-update crash when streaming longer responses.
* The model configuration editor and Gateway homepage code samples now explained that Gateway applied model and connection settings, while generation parameters such as max tokens and temperature must be set in API requests.
* Made hosted model request cap configurable.
* Select dropdowns supported keyboard selection and returned focus when closed. Search fields preserved queries across updates, text areas respected controlled values, and sliders exposed their labels to screen readers.
* The LLM Gateway preserved deferred tool declarations and ordered tool additions between Anthropic Messages and OpenAI Responses, mapped hosted tool-search declarations with a warning when search algorithms differed, and rejected unsupported search history and deferred tools on Chat Completions routes instead of silently changing their behavior.
* Allowed slower ThinkingState animation.
* Collapsing a section of a long interrupt payload in the Studio thread panel kept the section under your pointer instead of jumping back to the start of the thread.
* Resolved usage limiting unique violation errors.
* Deployment pages showed access and custom authentication guidance when assistant, thread, cron, or connection requests failed instead of showing an empty state.
* Changing the role on a workspace-scoped service key now required permission to manage keys in every workspace the key covered, matching the rule for deleting it.
* The LLM Gateway preserved ordered and repeated activations of matching deferred tools when translating between OpenAI Responses and Anthropic Messages, without duplicating tool definitions. Conflicting definitions, ambiguous names, and collisions with initially available tools remained rejected.
* Deleting a code evaluator no longer waited for sandbox snapshot cleanup, so the delete succeeded instead of timing out. The snapshot ID was queued so cleanup still ran if the API shut down.
* A new SankeyChart design-system component visualized stage-to-stage volume — sources through models to outcomes, spend across environments and workloads, or any weighted flow. Nodes sized by flow, legend rows filtered stages, and hovering a stage emphasized its links.
* Custom model price entries now had a Clone action, like built-in entries. The model pricing panel asked before discarding unsaved changes when you clicked outside it, pressed Escape, or closed it.
* The unified LLM Gateway enforced Messages stop sequences when translating completed and streaming Responses output, including model fallback. Matching truncated delivered text and later content while preserving full upstream usage; it did not cancel upstream generation. Synthetic emulation accepted at most four stop sequences of up to 1024 UTF-8 bytes each; oversized inputs were rejected before a Responses request was sent.
* A brief storage backend error no longer left a sandbox's filesystem returning I/O errors until restart. Reads succeeded again once the backend recovered.
* Chat now kept working past the first tool call when a workspace Model Configuration pointed at Gemini on Vertex AI, and no longer rejected tool-calling turns on saved Gemini API configurations.
* Annotation queue rubric items now appeared in the order they were added instead of alphabetically, in the queue editor, the review sidebar, and CSV exports. Existing rubrics kept their current order.
* Implemented weekly per-tenant limit on bulk run deletes.
* Read the metadata delete queue in pages.
* Auto-ran BYOC preview E2E after deploy and reported on PR.
* Gemini OpenAI-compatible requests now filled absent tool-call thought signatures with Google's documented skip\_thought\_signature\_validator sentinel, including configured Gemini routes. Supplied signatures were preserved. This workaround permitted clients that cannot round-trip signatures to continue tool conversations, but did not restore reasoning state and may have reduced model quality.
* Online and Preview Test sandbox evaluators that required attachments now resolved each attachment's MIME type via a metadata HEAD before scoring. Built-in voice metrics could therefore pick call recordings even when the attachment key had no audio extension, as long as storage reported an audio Content-Type.
* Example timestamp parsing accepted compact calendar timestamps, times without seconds, and additional UTC offset formats. Historical example queries retained microsecond precision and dataset-tag handling. Metadata filters preserved apostrophes inside double-quoted keys.
* Costs now resolved for the OpenAI models listed under "All models" on the pricing page, such as GPT-5.6 Luna and Terra. The daily price sync had only been reading the three models the page showed by default, so the rest kept whatever price they were first created with. Runs that reported no provider were also corrected: GPT-5.6 Luna and Terra were still priced at their launch rates, 5x and 1.25x what OpenAI charges today.
* Monitoring chart descriptions now wrapped onto multiple lines so the full text remained visible.
* Loading a saved Bedrock Converse configuration whose model ID was an application inference profile ARN now kept the provider set in Extra Parameters, so the preset ran without re-entering it.
* Chat on a Gemini 3.x model via Vertex AI now completed turns that called several tools in a row, instead of failing once the model narrated its work between calls.
* Selected Claude Sonnet 5.5 in Playground and model configurations for Anthropic, Bedrock, and Vertex AI.
* Mounted the main-fe Nginx config on AWS frontend previews.
* Google Vertex AI model configurations now routed Anthropic Claude models to Vertex's native Anthropic Messages API while Gemini and open models kept using the OpenAI-compatible endpoint. Existing bare Claude IDs continued to work, and publisher-qualified IDs were normalized automatically.
* Traces could now contain up to 100,000 runs before the run limit was reached.
* Gave ingest-backend the sandbox callback signing key.
* Fixed routing for workspace with no agents.
* LangSmith Chat now read and wrote the `field:value` filter syntax on the revamped tracing table, and picked the right scope — single run, root run, any run, or thread — for what you asked. A filter it could not express in the scope you were on was refused rather than silently emptying the table.

**Download the Helm chart:** [`langsmith-0.18.0-rc.1.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.18.0-rc.1/langsmith-0.18.0-rc.1.tgz)

**2026-09-30**

## langsmith-0.17.0-rc.52

**LangSmith version:** `0.17.29rc2`

* Internal improvements and maintenance updates

**Download the Helm chart:** [`langsmith-0.17.0-rc.52.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.0-rc.52/langsmith-0.17.0-rc.52.tgz)

**2026-09-30**

## langsmith-0.17.0-rc.51

**LangSmith version:** `0.17.28rc1`

* This release packages the same LangSmith application version as langsmith-0.17.0-rc.42. Refer to the [langsmith-0.17.0-rc.42](#langsmith-0-17-0-rc-42) release notes below.

**Download the Helm chart:** [`langsmith-0.17.0-rc.51.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.0-rc.51/langsmith-0.17.0-rc.51.tgz)

**2026-09-29**

## langsmith-0.17.0-rc.50

**LangSmith version:** `0.17.28rc1`

* This release packages the same LangSmith application version as langsmith-0.17.0-rc.42. Refer to the [langsmith-0.17.0-rc.42](#langsmith-0-17-0-rc-42) release notes below.

**Download the Helm chart:** [`langsmith-0.17.0-rc.50.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.0-rc.50/langsmith-0.17.0-rc.50.tgz)

**2026-09-29**

## langsmith-0.17.0-rc.49

**LangSmith version:** `0.17.28rc1`

* This release packages the same LangSmith application version as langsmith-0.17.0-rc.42. Refer to the [langsmith-0.17.0-rc.42](#langsmith-0-17-0-rc-42) release notes below.

**Download the Helm chart:** [`langsmith-0.17.0-rc.49.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.0-rc.49/langsmith-0.17.0-rc.49.tgz)

**2026-09-29**

## langsmith-0.17.0-rc.48

**LangSmith version:** `0.17.29rc1`

* This release packages the same LangSmith application version as langsmith-0.17.0-rc.44. Refer to the [langsmith-0.17.0-rc.44](#langsmith-0-17-0-rc-44) release notes below.

**Download the Helm chart:** [`langsmith-0.17.0-rc.48.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.0-rc.48/langsmith-0.17.0-rc.48.tgz)

**2026-09-29**

## langsmith-0.17.0-rc.46

**LangSmith version:** `0.17.28rc1`

* This release packages the same LangSmith application version as langsmith-0.17.0-rc.42. Refer to the [langsmith-0.17.0-rc.42](#langsmith-0-17-0-rc-42) release notes below.

**Download the Helm chart:** [`langsmith-0.17.0-rc.46.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.0-rc.46/langsmith-0.17.0-rc.46.tgz)

**2026-09-29**

## langsmith-0.17.0-rc.47

**LangSmith version:** `0.17.29rc1`

* This release packages the same LangSmith application version as langsmith-0.17.0-rc.44. Refer to the [langsmith-0.17.0-rc.44](#langsmith-0-17-0-rc-44) release notes below.

**Download the Helm chart:** [`langsmith-0.17.0-rc.47.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.0-rc.47/langsmith-0.17.0-rc.47.tgz)

**2026-09-29**

## langsmith-0.16.35

**LangSmith version:** `0.16.67`

* This release packages the same LangSmith application version as langsmith-0.16.34. Refer to the [langsmith-0.16.34](#langsmith-0-16-34) release notes below.

**Download the Helm chart:** [`langsmith-0.16.35.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.16.35/langsmith-0.16.35.tgz)

**2026-09-29**

## langsmith-0.17.0-rc.45

**LangSmith version:** `0.17.28rc1`

* This release packages the same LangSmith application version as langsmith-0.17.0-rc.42. Refer to the [langsmith-0.17.0-rc.42](#langsmith-0-17-0-rc-42) release notes below.

**Download the Helm chart:** [`langsmith-0.17.0-rc.45.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.0-rc.45/langsmith-0.17.0-rc.45.tgz)

**2026-09-28**

## langsmith-0.17.0-rc.44

**LangSmith version:** `0.17.29rc1`

* The Trace Tools tab showed function tools alongside provider server tools, such as OpenAI tool\_search, and unrecognized entries no longer hid the other tools in a run.

**Download the Helm chart:** [`langsmith-0.17.0-rc.44.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.0-rc.44/langsmith-0.17.0-rc.44.tgz)

**2026-09-26**

## langsmith-0.17.0-rc.43

**LangSmith version:** `0.17.28rc1`

* This release packages the same LangSmith application version as langsmith-0.17.0-rc.42. Refer to the [langsmith-0.17.0-rc.42](#langsmith-0-17-0-rc-42) release notes below.

**Download the Helm chart:** [`langsmith-0.17.0-rc.43.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.0-rc.43/langsmith-0.17.0-rc.43.tgz)

**2026-09-24**

## langsmith-0.17.0-rc.42

**LangSmith version:** `0.17.28rc1`

* The evaluators list API accepted an agent\_id filter to return evaluators attached to the agent's environments or tagged datasets.
* Self-hosted Playground and LLM evaluators could authenticate to Azure OpenAI with Azure Kubernetes Service workload identity when no API key was configured.
* Emitted checkout step views for billing-page checkouts.
* Charts showed shape-aware loading skeletons instead of temporary zero values while data loaded, and evaluator spend charts used bar and metric placeholders that preserved the final layout.
* Engine issue descriptions preserved their concise prose while rendering mentioned file paths, functions, classes, tools, and code identifiers as inline code.
* Answered 204 instead of a bodiless 200.
* Self-hosted upgrades could rerun the usage metering migration without duplicate-trigger errors or replacing existing model pricing with default rates.
* The LLM Gateway supported direct passthrough requests to TypeSafe's System One API using workspace credentials.
* Evaluator variable mapping explained clearly that trajectory and non-trajectory variables could not be used together.
* Agent Auth automatically registered MCP OAuth clients that required client-secret authentication, storing their credentials securely alongside existing public-client support.
* Charts showed loading placeholders that matched their final visualization, including bar, line, donut, metric, and sparkline charts.
* Categorical evaluator fields resized with the editor pane, keeping descriptions and remove-category buttons inside the feedback configuration card.
* New custom apps opened the preview panel when Polly started writing files, and the unfinished first draft stayed covered until generation completed and the preview was ready.
* Custom app previews showed an animated loading illustration while starting, with a static version for reduced motion, and published previews faded in when ready.
* Agent updates rejected changes to the backend type or sandbox scope, matching the existing UI behavior, with new agents required to use a different backend; other sandbox settings remained editable.
* Kept the split view pane resize handle grabbable.
* A trajectory evaluator's retention upgrade no longer bounded the trace by an approximate start time, upgrading the root run and its earliest children along with the rest, and the evaluated-run link on a trajectory evaluator's trace was withheld until it could point at the right run.
* The Gateway provider search field used a more comfortable height while remaining aligned with standard component sizes.
* A thread or trajectory automation batch that failed its last retry no longer left a partial page cursor behind, so the next scheduled window started from the beginning of the window instead of mid-page, and an automation whose trajectory service URL was not configured now recorded one failed rule-log entry instead of retrying until the attempt limit.
* The LangSmith Go and Java SDKs could list, update, and delete saved Insights report configurations, including their recurring schedules.
* Kept the top bar on the agent picker page.
* The thread traces API accepted `trace_filter` and `tree_filter` query parameters for filtering root runs and matching runs anywhere in a trace tree.
* Filtered the custom apps list by creator and preserved the selection in the page URL.
* Kept red-team probe claims\_no\_terminal\_answer.
* Hid feedback shortcuts without matching keys.
* Evaluator side panels disabled Save while the configuration was invalid and displayed the reasons; correcting the configuration enabled saving again.
* Browser Back retained navigation guards when returning to the initially loaded page, including cleanup of empty, undeployed custom apps.
* Downloading experiment results with "Include annotator name and comment per row" now kept automated evaluator scores in every feedback column, alongside human annotations.
* Evaluator forms explained validation errors in the Save tooltip instead of a banner; Save remained disabled until the configuration was valid.
* Sandboxes could call the LangSmith API on your behalf without an API key inside the sandbox; passing `access_delegation` on create granted either your full access or a specific list of permissions; the sandbox never held the credential, and the grant was capped by what you could do at the time of each request.
* Created sandboxes from a shared, read-only catalog of system snapshots: system/default:latest, system/custom-apps:latest with Smith Apps tooling, and system/code-evaluators:latest with NumPy preinstalled, choosing system or workspace snapshots from the same sandbox and Fleet selectors.
* An evaluator using an organization-scoped model configuration that authenticated with an API key no longer attempted a per-model OAuth token exchange, and Amazon Bedrock models configured this way were no longer rejected as unsupported.
* Gateway requests logged traces only to the shared gateway project instead of also creating duplicates in API-key or user-specific projects; existing caller-specific projects and their historical traces remained unchanged.
* A sandbox calling the API under an access-delegation grant could still create sandboxes but could no longer give one a grant of its own, and audit entries for a delegated call now named the sandbox that made it.
* Engine read the contents of successful tool results rather than only their status, filing issues where a call returned less data than its own result claimed or where a value arrived truncated, with defects that never surfaced as an error no longer passed over.
* Evaluator side panels showed mapping errors and prevented saving when run evaluators used thread or trajectory sources, or thread and trajectory evaluators used run sources, with validation updated when the evaluator target changed.
* Gave red-team HIGH severity its own chart color.
* The Columns menu on a tracing project's traces and runs table let you deselect Status and Name, and drag them into any order alongside the other columns.
* LangSmith supported TypeSafe in model access policies and provided System One examples for direct Gateway requests.
* LLM Gateway traces for TypeSafe Jev calls included token usage and calculated costs at TypeSafe's published rate.
* Used a 30-minute staging ABAC latency window.
* The system/code-evaluators:latest snapshot included pandas, jsonschema, SciPy, and scikit-learn alongside NumPy, so evaluators could use ACE's supported Python packages without installing them.
* Propagated available tools through trajectory processing (2/7).
* Extracted available tools from OpenAI traces (3/7).
* LangChain trajectories used message IDs from root runs to identify the main conversation, falling back to the existing selection when no unique match was available or optional root enrichment failed, with other formats not fetching this enrichment, and processing runs and optional roots shared one byte budget, with the default message-view and trajectory contribution limits being 200 MB.
* The project stats sidebar showed Cache Hit % above streaming rate, helping you see the share of input tokens served from the prompt cache.
* Opened Notifications in the sidebar to view platform announcements and account notices without interrupting your work; incident alerts remained at the top of the page.
* An Engine Red Team run on a project that Engine had already scanned started from that project's Agent Overview and ran a shorter confirmation scan, instead of re-deriving the application map every time.
* Trajectory evaluation selected the latest trace by its root run's start time rather than a child LLM run's start time; trajectory metadata reported each trace's actual root start time and marked scopes with missing root timestamps as incomplete.
* A sandbox's service URLs could be listed, showing which ports were shared and how, with sharing able to be turned off for one port or all of them; previously a service URL could be created but never inspected or withdrawn.
* Kept the target's answer inside the judge's read window.
* The evaluator configuration form displayed the complete sampling-rate percentage at every supported input size.
* Saving an issue board's GitHub settings cleared the fix branch and pull request link on every issue in the project, even when the repository itself hadn't changed—so editing only the base branch or the auto-open-PR toggle silently detached issues from pull requests that were already open or merged; board settings no longer touched those links at all.
* When a tracing batch took longer to upload than the server would wait, /runs/multipart and /runs/batch stopped reading and returned 408 Request Timeout instead of a 503; a timeout caused by the server rather than the upload returned 504.
* Organizations could disable API-key-authenticated key creation from General settings; signed-in users with organization management permission could update the setting, and existing keys continued to work.
* When a graph called interrupt() with a response\_schema, Studio rendered typed fields for the resume value instead of a free-form JSON editor; interrupts without a schema kept the JSON editor.
* Deployment forms trimmed surrounding whitespace from environment variable names before submission, preventing accidental spaces from causing deployment failures; environment variable values remained unchanged.
* Workspace tooltips on the API Keys page stayed compact and let you scroll through the full list while keeping the heading visible.
* The LLM Gateway omitted temperature from unified API requests and fallbacks unless the destination OpenAI model and reasoning setting were explicitly supported, preventing unsupported-temperature errors on newer models; custom OpenAI-compatible providers and native passthrough requests remained unchanged.

**Download the Helm chart:** [`langsmith-0.17.0-rc.42.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.0-rc.42/langsmith-0.17.0-rc.42.tgz)

**2026-09-24**

## langsmith-0.16.34

**LangSmith version:** `0.16.67`

* Internal improvements and maintenance updates

**Download the Helm chart:** [`langsmith-0.16.34.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.16.34/langsmith-0.16.34.tgz)

**2026-09-23**

## langsmith-0.16.33

**LangSmith version:** `0.16.66`

* Updated the sandbox guest Linux kernel to 6.1.186 to include security fixes in self-hosted sandbox images.

**Download the Helm chart:** [`langsmith-0.16.33.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.16.33/langsmith-0.16.33.tgz)

**2026-09-23**

## langsmith-0.17.0-rc.41

**LangSmith version:** `0.17.25rc1`

* This release packages the same LangSmith application version as langsmith-0.17.0-rc.33. Refer to the [langsmith-0.17.0-rc.33](#langsmith-0-17-0-rc-33) release notes below.

**Download the Helm chart:** [`langsmith-0.17.0-rc.41.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.0-rc.41/langsmith-0.17.0-rc.41.tgz)

**2026-09-23**

## langsmith-0.17.0-rc.40

**LangSmith version:** `0.17.25rc1`

* This release packages the same LangSmith application version as langsmith-0.17.0-rc.33. Refer to the [langsmith-0.17.0-rc.33](#langsmith-0-17-0-rc-33) release notes below.

**Download the Helm chart:** [`langsmith-0.17.0-rc.40.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.0-rc.40/langsmith-0.17.0-rc.40.tgz)

**2026-09-23**

## langsmith-0.16.32

**LangSmith version:** `0.16.65`

* Evaluator column headers in the experiments table no longer truncated at a fixed width—widening a column revealed the complete evaluator name, and dragging a column now changes its width immediately, instead of appearing to do nothing.

**Download the Helm chart:** [`langsmith-0.16.32.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.16.32/langsmith-0.16.32.tgz)

**2026-09-23**

## langsmith-0.17.0-rc.39

**LangSmith version:** `0.17.25rc1`

* This release packages the same LangSmith application version as langsmith-0.17.0-rc.33. Refer to the [langsmith-0.17.0-rc.33](#langsmith-0-17-0-rc-33) release notes below.

**Download the Helm chart:** [`langsmith-0.17.0-rc.39.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.0-rc.39/langsmith-0.17.0-rc.39.tgz)

**2026-09-22**

## langsmith-0.17.0-rc.38

**LangSmith version:** `0.17.25rc1`

* This release packages the same LangSmith application version as langsmith-0.17.0-rc.33. Refer to the [langsmith-0.17.0-rc.33](#langsmith-0-17-0-rc-33) release notes below.

**Download the Helm chart:** [`langsmith-0.17.0-rc.38.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.0-rc.38/langsmith-0.17.0-rc.38.tgz)

**2026-09-22**

## langsmith-0.16.31

**LangSmith version:** `0.16.63`

* Internal improvements and maintenance updates

**Download the Helm chart:** [`langsmith-0.16.31.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.16.31/langsmith-0.16.31.tgz)

**2026-09-22**

## langsmith-0.16.30

**LangSmith version:** `0.16.62`

* Internal improvements and maintenance updates

**Download the Helm chart:** [`langsmith-0.16.30.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.16.30/langsmith-0.16.30.tgz)

**2026-09-22**

## langsmith-0.17.0-rc.37

**LangSmith version:** `0.17.25rc1`

* This release packages the same LangSmith application version as langsmith-0.17.0-rc.33. Refer to the [langsmith-0.17.0-rc.33](#langsmith-0-17-0-rc-33) release notes below.

**Download the Helm chart:** [`langsmith-0.17.0-rc.37.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.0-rc.37/langsmith-0.17.0-rc.37.tgz)

**2026-09-21**

## langsmith-0.16.29

**LangSmith version:** `0.16.61`

* Internal improvements and maintenance updates

**Download the Helm chart:** [`langsmith-0.16.29.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.16.29/langsmith-0.16.29.tgz)

**2026-09-19**

## langsmith-0.16.28

**LangSmith version:** `0.16.60`

* Internal improvements and maintenance updates

**Download the Helm chart:** [`langsmith-0.16.28.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.16.28/langsmith-0.16.28.tgz)

**2026-09-19**

## langsmith-0.17.0-rc.36

**LangSmith version:** `0.17.25rc1`

* This release packages the same LangSmith application version as langsmith-0.17.0-rc.33. Refer to the [langsmith-0.17.0-rc.33](#langsmith-0-17-0-rc-33) release notes below.

**Download the Helm chart:** [`langsmith-0.17.0-rc.36.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.0-rc.36/langsmith-0.17.0-rc.36.tgz)

**2026-09-18**

## langsmith-0.16.27

**LangSmith version:** `0.16.59`

* This release packages the same LangSmith application version as langsmith-0.16.26. Refer to the [langsmith-0.16.26](#langsmith-0-16-26) release notes below.

**Download the Helm chart:** [`langsmith-0.16.27.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.16.27/langsmith-0.16.27.tgz)

**2026-09-18**

## langsmith-0.17.0-rc.35

**LangSmith version:** `0.17.25rc1`

* This release packages the same LangSmith application version as langsmith-0.17.0-rc.33. Refer to the [langsmith-0.17.0-rc.33](#langsmith-0-17-0-rc-33) release notes below.

**Download the Helm chart:** [`langsmith-0.17.0-rc.35.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.0-rc.35/langsmith-0.17.0-rc.35.tgz)

**2026-09-18**

## langsmith-0.16.26

**LangSmith version:** `0.16.59`

* Internal improvements and maintenance updates

**Download the Helm chart:** [`langsmith-0.16.26.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.16.26/langsmith-0.16.26.tgz)

**2026-09-17**

## langsmith-0.16.25

**LangSmith version:** `0.16.58`

* This release packages the same LangSmith application version as langsmith-0.16.24. Refer to the [langsmith-0.16.24](#langsmith-0-16-24) release notes below.

**Download the Helm chart:** [`langsmith-0.16.25.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.16.25/langsmith-0.16.25.tgz)

**2026-09-17**

## langsmith-0.17.0-rc.34

**LangSmith version:** `0.17.25rc1`

* This release packages the same LangSmith application version as langsmith-0.17.0-rc.33. Refer to the [langsmith-0.17.0-rc.33](#langsmith-0-17-0-rc-33) release notes below.

**Download the Helm chart:** [`langsmith-0.17.0-rc.34.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.0-rc.34/langsmith-0.17.0-rc.34.tgz)

**2026-09-17**

## langsmith-0.16.24

**LangSmith version:** `0.16.58`

* Self-hosted Playground and LLM evaluators could authenticate to Azure OpenAI with Azure Kubernetes Service workload identity when no API key was configured.
* Self-hosted upgrades could rerun the usage metering migration without duplicate-trigger errors or replacing existing model pricing with default rates.

**Download the Helm chart:** [`langsmith-0.16.24.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.16.24/langsmith-0.16.24.tgz)

**2026-09-17**

## langsmith-0.17.0-rc.33

**LangSmith version:** `0.17.25rc1`

* Smoothed tab indicator transitions/animations.
* Removed extra filter error tooltip border.
* The Usage dashboard's "Group by" control now automatically detected the header configured on your default API key spend cap policy, allowing grouping by header directly instead of opening it from a Cost Controls policy row; if no header was configured, the option explained what to add and where.
* Grouped saved view controls.
* Recorded hourly storage attribution for sandbox cost breakdowns while preserving existing aggregate billing, with repeated samples atomically replacing entity details and the workspace aggregate.
* Filtered the annotation queue "View all items" page by when each trace ran, using the same preset ranges as the Traces page.
* The annotation queue "View all items" page now showed each item's run start time, allowing visibility of when a trace was triggered without opening it.
* Grouped LLM Gateway usage by Model Provider within an API key or user to compare spend across providers and filter to specific ones.
* Switching between thread items in an annotation queue now replaced the previous thread's messages instead of overlaying the new thread over them.
* Context Hub's markdown preview pane now rendered files without editing them, preventing the rich-text editor from unintentionally rewriting stored bytes; editing occurred in the Edit tab, affecting exact bytes in the repo, and your Preview/Edit choice persisted as you moved between files.
* Pinned every OpenAI client to the deployment's region.
* Authenticated Gateway requests could optionally send an opaque raw provider token in X-LangSmith-Anthropic-Passthrough. LangSmith OAuth used standard Authorization bearer authentication; only built-in Anthropic requests forwarded the token as a bearer without accessing workspace provider secrets, leaving token validity to Anthropic. Other providers and custom Anthropic-compatible endpoints used typical fetched keys. Saved models/routes, catalogs, and mixed fallback chains retained existing permissions, policies, entitlements, and provider-specific accounting.
* Restored EU Vertex inference on the combined deployment.
* Corrected Jira destination branding.
* Publicly shared thread pages no longer showed a share action that could not succeed.
* Stopped gating flaky tests on user groups.
* Aligned red teaming beta badge.
* Aligned environment picker.
* Fixed name on the tooltip for environment id.
* Tracked proactive red-team coverage.
* A safety refusal from the model now rendered an explanation instead of an empty reply, a failed tool call indicated failure instead of completion, and evaluator search clarified which runs each evaluator scored. Removed the non-functioning voice button from the chat panel.
* Insights no longer warned about optimization only for OpenAI or Anthropic when both selected models used another provider.
* When a tracing project lacked traces in the default time range, the range now widened to include the most recent trace, up to 30 days back. If an explicit range was set, an option to expand it appeared next to the empty table.
* Enabled streamable HTTP MCP for ungated actions.
* Persisted Trivy action permissions for langgraph-api.
* Edit and deletion in the experiments table now checked project permission to match BE.
* Renamed Messages to Trajectory when navigation flag was on.
* The issue detail header now read its timestamp from the issue's last-modified time, preventing routine updates like Engine linking new evidence and refreshing the description from making a closed issue appear freshly marked done; it now read "Updated \<when>," with details on who closed the issue and when shown below in the history.
* Avoided expensive error hydration.
* The Columns menu on a tracing project's traces and runs table now allowed deselecting Status and Name and dragging them into any order with the other columns.
* Disabled APAC shadow builds.
* Automations grouped by thread could now send webhook payloads with matched conversations and their runs.
* Labeled export buttons as trajectory when navigation view was on.
* Introduced a new public endpoint breaking down recorded hourly usage costs by sandbox and snapshot, with resource filters and cursor pagination. Checkpoint storage remained with its sandbox, and the full storage breakdown reconciled with the recorded workspace total.
* An Engine scan no longer failed outright when its project-stats request was not returned; it continued with the errored and baseline traces it could select, informed the agent about missing selections, and recorded the stats call failure reason.
* Kept the trace pane open for hovercard interactions.
* Prioritized realistic red-team probes.
* Engine now scanned projects whose names included punctuation, Unicode, or special characters, preventing their boards from stalling while analysis started.
* Returned an error when mitigating SSRF instead of a 500.
* Updated code evaluator defaults for Python 3.14.
* Fleet agents on Amazon Bedrock no longer failed on every turn after a truncated tool call or a response containing only thinking was saved to the conversation, resuming with the next message instead.
* Insights now recommended a capable thinking model and a fast summarization model with a large context window without warning against mixing providers.
* The LangSmith Go and Java SDKs could now save Insights report configurations, enabling clients to create UI-visible Insights reports programmatically.
* Turning an automation off now ceased its backfill and live evaluation, not resuming them upon reactivation; a disabled automation continued advancing its position while off, meaning reactivation resumed roughly from its pause point, avoiding redundant evaluation of every trace submitted while it was off.
* The header count and delete confirmation on the annotation queue "View all items" page now reflected the active time range instead of the whole queue, with the item count endpoint accepting min\_start\_time and max\_start\_time.
* When an evaluator score from a rule, playground experiment, or UI code evaluator violated the workspace feedback key configuration (e.g., a 5 against a 0–1 range), LangSmith now recorded error feedback on the run with the rejection reason in the comment instead of silently dropping it.
* Added empty state for prompts.
* Installed pnpm and failed the build job on non-conflict failures.
* Routed the sandbox service-URL handshake to smith-go.
* Hid single-turn trajectory navigation.
* Limited inherited thread filters to ten turns.
* Changing a feedback score on a completed queue item previously raised a "Failed to update review time" error despite the score saving; the toast was removed, but the score still saved as before.
* Detail panes now filled narrow screens without wasting space on the left edge, with resize handles supporting keyboard navigation using arrow keys, Home, and End, and showing a visible focus indicator.
* A backfill that found every run on a page already processed now continued to the next page instead of ending the window early, allowing evaluation of runs behind that page.
* Switched to page on ingestion queue wait instead of pending count.
* Publicly exposed OIDC integrations.
* Fixed stale run details contents when switching between items.
* Revoking a personal access token preserved its original expiry, and reinstating the token restored access only while that expiry remained valid.
* Offered reinstatement on a revoked personal access token (PAT).
* Selecting a Slack channel for alert notifications now functioned in workspaces large enough for the channel list to have stopped loading.
* Avoided Dorny API rate limit in Terraform changes job.
* Unified trace filtering and displayed matched run summaries.
* Enforced waterfall minimum width in shared trace panels.
* Rolled up RUN\_RULES\_TWO\_POINTER\_BACKFILL\_TENANTS to status check deprecate\_dual\_reads.
* Dashboard chart feedback key suggestions now included keys from both run-level and thread-level feedback.
* Revoked and reinstated personal access tokens directly from the API Keys table in Settings, with reinstatement preserving the token's expiry date, and expired tokens displaying a disabled Reinstate key action with an explanation.
* Fleet thread updates now preserved system-managed ownership metadata across typed, bulk, and LangGraph proxy requests.
* The Studio memory editor kept its close button visible while scrolling through long memory items.
* Alerts using input, output, or error text filters now matched runs regardless of the blob storage and ClickHouse search settings, with search tokens still written to ClickHouse only when both blob storage and ClickHouse search were enabled.
* Section dividers in agent overview cards and Gateway connection panels now have stronger contrast in light and dark mode.
* Selected TURN\_NUMBER when listing thread traces to return each trace's chronological position across pages. Turn numbers are also available for public shared threads.

**Download the Helm chart:** [`langsmith-0.17.0-rc.33.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.0-rc.33/langsmith-0.17.0-rc.33.tgz)

**2026-09-17**

## langsmith-0.16.23

**LangSmith version:** `0.16.57`

* Fixed the issue where listing an organization's roles failed when a role had no permissions; such a role is now returned with an empty permission list instead of making the whole roles list unavailable.

* Fixed security vulnerabilities. See CVE-2026-7210 for details.

**Download the Helm chart:** [`langsmith-0.16.23.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.16.23/langsmith-0.16.23.tgz)

**2026-09-17**

## langsmith-0.17.0-rc.32

**LangSmith version:** `0.17.24rc1`

* This release packages the same LangSmith application version as langsmith-0.17.0-rc.26. Refer to the [langsmith-0.17.0-rc.26](#langsmith-0-17-0-rc-26) release notes below.

**Download the Helm chart:** [`langsmith-0.17.0-rc.32.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.0-rc.32/langsmith-0.17.0-rc.32.tgz)

**2026-09-17**

## langsmith-0.17.0-rc.31

**LangSmith version:** `0.17.24rc1`

* This release packages the same LangSmith application version as langsmith-0.17.0-rc.26. Refer to the [langsmith-0.17.0-rc.26](#langsmith-0-17-0-rc-26) release notes below.

**Download the Helm chart:** [`langsmith-0.17.0-rc.31.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.0-rc.31/langsmith-0.17.0-rc.31.tgz)

**2026-09-15**

## langsmith-0.17.0-rc.30

**LangSmith version:** `0.17.24rc1`

* This release packages the same LangSmith application version as langsmith-0.17.0-rc.26. Refer to the [langsmith-0.17.0-rc.26](#langsmith-0-17-0-rc-26) release notes below.

**Download the Helm chart:** [`langsmith-0.17.0-rc.30.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.0-rc.30/langsmith-0.17.0-rc.30.tgz)

**2026-09-14**

## langsmith-0.17.0-rc.29

**LangSmith version:** `0.17.24rc1`

* This release packages the same LangSmith application version as langsmith-0.17.0-rc.26. Refer to the [langsmith-0.17.0-rc.26](#langsmith-0-17-0-rc-26) release notes below.

**Download the Helm chart:** [`langsmith-0.17.0-rc.29.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.0-rc.29/langsmith-0.17.0-rc.29.tgz)

**2026-09-14**

## langsmith-0.17.0-rc.28

**LangSmith version:** `0.17.24rc1`

* This release packages the same LangSmith application version as langsmith-0.17.0-rc.26. Refer to the [langsmith-0.17.0-rc.26](#langsmith-0-17-0-rc-26) release notes below.

**Download the Helm chart:** [`langsmith-0.17.0-rc.28.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.0-rc.28/langsmith-0.17.0-rc.28.tgz)

**2026-09-14**

## langsmith-0.17.0-rc.27

**LangSmith version:** `0.17.24rc1`

* This release packages the same LangSmith application version as langsmith-0.17.0-rc.26. Refer to the [langsmith-0.17.0-rc.26](#langsmith-0-17-0-rc-26) release notes below.

**Download the Helm chart:** [`langsmith-0.17.0-rc.27.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.0-rc.27/langsmith-0.17.0-rc.27.tgz)

**2026-09-14**

## langsmith-0.16.22

**LangSmith version:** `0.16.55`

* LangSmith services authenticated startup requests to the deployment info endpoint when endpoint authentication was enabled.

**Download the Helm chart:** [`langsmith-0.16.22.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.16.22/langsmith-0.16.22.tgz)

**2026-09-14**

## langsmith-0.17.0-rc.26

**LangSmith version:** `0.17.24rc1`

* Internal improvements and maintenance updates

**Download the Helm chart:** [`langsmith-0.17.0-rc.26.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.0-rc.26/langsmith-0.17.0-rc.26.tgz)

**2026-09-14**

## langsmith-0.16.21

**LangSmith version:** `0.16.54`

* This release packages the same LangSmith application version as langsmith-0.16.20. Refer to the [langsmith-0.16.20](#langsmith-0-16-20) release notes below.

**Download the Helm chart:** [`langsmith-0.16.21.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.16.21/langsmith-0.16.21.tgz)

**2026-09-14**

## langsmith-0.16.20

**LangSmith version:** `0.16.54`

* Internal improvements and maintenance updates

**Download the Helm chart:** [`langsmith-0.16.20.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.16.20/langsmith-0.16.20.tgz)

**2026-09-11**

## langsmith-0.16.19

**LangSmith version:** `0.16.52`

* This release packages the same LangSmith application version as langsmith-0.16.18. Refer to the [langsmith-0.16.18](#langsmith-0-16-18) release notes below.

**Download the Helm chart:** [`langsmith-0.16.19.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.16.19/langsmith-0.16.19.tgz)

**2026-09-10**

## langsmith-0.16.18

**LangSmith version:** `0.16.52`

* Avoided full mise installation in the v16 release.

**Download the Helm chart:** [`langsmith-0.16.18.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.16.18/langsmith-0.16.18.tgz)

**2026-09-09**

## langsmith-0.17.0-rc.25

**LangSmith version:** `0.17.20rc1`

* This release packages the same LangSmith application version as langsmith-0.17.0-rc.23. Refer to the [langsmith-0.17.0-rc.23](#langsmith-0-17-0-rc-23) release notes below.

**Download the Helm chart:** [`langsmith-0.17.0-rc.25.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.0-rc.25/langsmith-0.17.0-rc.25.tgz)

**2026-09-09**

## langsmith-0.16.17

**LangSmith version:** `0.16.50`

* This release packages the same LangSmith application version as langsmith-0.16.16. Refer to the [langsmith-0.16.16](#langsmith-0-16-16) release notes below.

**Download the Helm chart:** [`langsmith-0.16.17.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.16.17/langsmith-0.16.17.tgz)

**2026-09-09**

## langsmith-0.17.0-rc.24

**LangSmith version:** `0.17.20rc1`

* This release packages the same LangSmith application version as langsmith-0.17.0-rc.23. Refer to the [langsmith-0.17.0-rc.23](#langsmith-0-17-0-rc-23) release notes below.

**Download the Helm chart:** [`langsmith-0.17.0-rc.24.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.0-rc.24/langsmith-0.17.0-rc.24.tgz)

**2026-09-09**

## langsmith-0.17.0-rc.23

**LangSmith version:** `0.17.20rc1`

* Repaired frontend deploy and alert failures.
* No user-facing release note required; dependency-only maintenance update.
* Allowed deployments to leave managed mode.
* Priced Vertex Engine input tokens at the cache-read rate.
* Remediated open Dependabot alerts.
* When a Slack channel event failed before reaching your Managed Deep Agent because of a dropped delivery, a missing bot token, an interrupt that could not be shown, or an ambiguous route, it surfaced in `mda logs` and the deployment logs UI instead of failing silently.
* Routed Bedrock xAI inference profiles.
* Routed billing alerts to the dedicated billing channel.
* Configured agent auth OAuth callbacks.
* Ignored agents without names.
* Routed EU fix runs through regional OpenAI.
* Polled credential sessions on the shipped Agent Auth route.
* Led Slack issue alerts with the title.
* Sharing a thread created a link that anyone could open without a LangSmith account, showing every turn in the thread along with its run traces and feedback scores. The link always reflected the thread's current contents, including turns added after you shared it, and unsharing revoked it immediately.
* Set all three prompt-cache breakpoints on the Vertex path.
* Increased recent filter debounce.
* Kept Agent Overview edit below sticky header.
* Monitored Asynq rate-limit retries without logs.
* Reconciled sandbox provisioning.
* Removed messages view extra padding.
* Configuring an evaluator with a trace or tree filter no longer timed out while loading the sample run shown in the preview.
* Aligned agent hooks with Agent API contract.
* Isolated evaluator snapshots.
* Accepted blank API keys when the proxy or OAuth supplied the credential.
* Allowed exec to close a command's stdin.
* Exited the fallback chain when the request context was done.
* Moved BYOC Manager to infra.
* Documented validation errors as strings.
* Hid tracing filters without flicker.
* When an agent paused because a connected integration still needed OAuth, Slack now showed a Connect button that opened the authorization link directly. Previously the run paused with a generic notice and no way to finish connecting from Slack.
* LangSmith MCP connectors used Client ID Metadata Documents when supported, with dynamic client registration retained as a compatibility fallback.
* Workspace editors could now assign resources to an Application tag value from Settings > Resource Tags. The page previously failed with a permission error, even though editors were allowed to apply Application tags.
* Decoded the @openai/agents JS SDK's `function_call_result` items and camelCase `callId` fields on the trajectory endpoint, unblocking Messages view for JS agents that managed tool state client-side.
* Alembic git-revisions (dropped ALEMBIC\_HEAD merge conflicts).
* Reduced noisy BYOC Kubernetes alerts.
* Cleaned up failed thread sandboxes.
* Showed current SHA in commit lookup.
* Resumed org invite after signup.
* LLM Gateway fallback chains could now advance to the next model when a candidate did not return response headers within a configured timeout. Active response streams continued after headers arrived.
* Started local stack with workspace concurrently.
* Baked Alembic chain for the BYOC data-plane pin.
* Ran backend start stacks with local concurrently.
* Normalized APAC load balancer env.
* OAuth authorization sessions now accepted canonical `owner_type` and `owner_id` fields, allowing a human to authorize a managed credential for either a user or an agent. The deprecated `principal_id` and `agent_id` fields remained supported on legacy request and response shapes.
* Self-hosted deployments could now forward a REST caller's `X-Fleet-Forward-*` headers to the custom MCP servers an agent called, so a policy gateway in front of those servers could see per-invocation context such as an end-user identity. Off by default; enabled with `FLEET_MCP_FORWARD_CALLER_HEADERS=true`. Values were asserted by the caller and were not verified by LangSmith.
* Defaulted trace filters to root runs.
* GitHub Actions quota page.
* Aligned Studio message actions to the right.
* A deployment's custom install and build command now appeared in the Details panel, and the New Revision dialog prefilled them from the value currently in effect. Previously these commands persisted and were applied to every build but were not shown anywhere, so an inherited command was invisible to whoever had to debug the build.
* Updated organization plan badge colors.
* Commercial private ECR registries could now assume an AWS IAM role on demand, enabling repository and tag search while avoiding expiring saved authorization tokens.
* OAuth authorization sessions now accepted workspace owners, allowing one managed OAuth credential to be shared across a workspace.
* Thread query clients could request server-sent events to receive results progressively while preserving cursor pagination.
* The workspace switcher now accepted workspace IDs in addition to workspace names, making it easier to locate a workspace when only its ID was known.
* Used the new `/v2/threads/stats` endpoint to retrieve thread and trace counts, latency, token, cost, and feedback statistics for a tracing project.
* Fleet agents now supported saved Databricks model configurations, using your configured workspace URL, serving endpoint, and workspace credentials. You could connect through Databricks Model Serving or AI Gateway routes.

**Download the Helm chart:** [`langsmith-0.17.0-rc.23.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.0-rc.23/langsmith-0.17.0-rc.23.tgz)

**2026-09-05**

## langsmith-0.16.16

**LangSmith version:** `0.16.50`

* Internal improvements and maintenance updates

**Download the Helm chart:** [`langsmith-0.16.16.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.16.16/langsmith-0.16.16.tgz)

**2026-09-03**

## langsmith-0.17.0-rc.22

**LangSmith version:** `0.17.18rc1`

* This release packages the same LangSmith application version as langsmith-0.17.0-rc.20. Refer to the [langsmith-0.17.0-rc.20](#langsmith-0-17-0-rc-20) release notes below.

**Download the Helm chart:** [`langsmith-0.17.0-rc.22.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.0-rc.22/langsmith-0.17.0-rc.22.tgz)

**2026-09-02**

## langsmith-0.17.0-rc.21

**LangSmith version:** `0.17.18rc1`

* This release packages the same LangSmith application version as langsmith-0.17.0-rc.20. Refer to the [langsmith-0.17.0-rc.20](#langsmith-0-17-0-rc-20) release notes below.

**Download the Helm chart:** [`langsmith-0.17.0-rc.21.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.0-rc.21/langsmith-0.17.0-rc.21.tgz)

**2026-09-02**

## langsmith-0.17.0-rc.20

**LangSmith version:** `0.17.18rc1`

* Hid run tree expand/collapse control for flat trees.
* Created a tracing project that now waits for the project to become available before opening it, preventing false creation errors and not-found pages.
* Suspended smallest sandboxes first during host drain.
* Advanced past selected filter values.
* Rounded token and cost table values to four significant digits (fixed LSO-3999).
* Added investigation links to bulk export monitor.
* Prevented host enrichment on BYOC metrics.
* Kept issue header actions reachable when space is tight.
* Fell back for unknown message icon roles.
* Excluded playground from BYOC latency monitor.
* Required sustained max replicas.
* Prevented browser translation DOM mutations.
* Set a provider name on OpenAI-compatible model configurations to populate `ls_provider` trace metadata and match custom models to provider-specific pricing through the LLM Gateway.
* Used true 15m p95 for V2 runs latency monitor.
* Allowed users to view a chart and table breaking down an API key's spend by each header value when a cost policy splits an API key's spend limit by a custom header.
* Revamped target filters by organization.
* Notified on self-hosted and BYOC failures.
* Isolated untimed batching test.
* Allowed self-hosted LangSmith operators to configure how many days before license expiration the warning banner appears with `LICENSE_EXPIRATION_WARNING_DAYS`; the default remains seven days.
* Issues now had a Fix in Claude Code action that opened your local coding agent with the diagnosis, the linked traces, and the commands to fetch them already filled in, with a dropdown to switch to Codex or copy the prompt for any other agent.
* Prevented dashboard row hover from overlapping cards.
* Parsed nested Notion audit event metadata.
* Graphed Smith-agents LLM calls via SDK metrics.
* Disabled LSM backfill.
* Deployed Cloud Functions on source changes.
* Validated examples with unsupported completion outputs now reported a schema validation error instead of failing with an internal error.
* Made side nav hover states immediate.
* Aligned API-prefixed platform routes.
* Added Organization Restricted, a new organization-scoped, system-defined role that can access assigned workspaces while organization-level settings, billing, and usage surfaces stay hidden.
* Reduced GitHub API usage in preview PR comment upserts.
* Routed Bedrock Anthropic profiles to runtime.
* Gated Turns migration guidance on Messages view.
* Delayed internal HPA saturation alert.
* Preserved user-added filter scopes.
* Preserved Notion audit external table.
* Preserved active policy scope selections.
* Resolved the Eppo organization entity before assigning.
* Persisted partial cursor after deadline cancellation.
* Gated thread backfills by rollout status.
* When Engine marked an issue as a duplicate, the issue header now showed a Duplicate link to the original instead of a history note that included the other issue's ID.

**Download the Helm chart:** [`langsmith-0.17.0-rc.20.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.0-rc.20/langsmith-0.17.0-rc.20.tgz)

**2026-09-02**

## langsmith-0.16.15

**LangSmith version:** `0.16.48`

* Internal improvements and maintenance updates

**Download the Helm chart:** [`langsmith-0.16.15.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.16.15/langsmith-0.16.15.tgz)

**2026-09-01**

## langsmith-0.17.0-rc.19

**LangSmith version:** `0.17.17rc1`

* This release packages the same LangSmith application version as langsmith-0.17.0-rc.17. Refer to the [langsmith-0.17.0-rc.17](#langsmith-0-17-0-rc-17) release notes below.

**Download the Helm chart:** [`langsmith-0.17.0-rc.19.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.0-rc.19/langsmith-0.17.0-rc.19.tgz)

**2026-09-01**

## langsmith-0.17.0-rc.17

**LangSmith version:** `0.17.17rc1`

* Disabled Redis RDB snapshotting.
* Preserved controller runtime configuration.
* Regenerated prompt snapshots stale against feature\_gap change.
* Fixed auth bootstrap after org-row seat gating.
* Azure AI Foundry was added as a first-party LLM Gateway provider.
* Sourced dev platform apps from LangChainPlus.
* Restored reworked notification editor after merge.
* Grouped filter shortcut values with OR.
* Set AWS region for EKS auth on the API server.
* Showed spend limit currency.
* Provisioned LangGraph flat image repositories.
* Context Hub directory writes now supported explicit LATEST and COMMIT selectors for linked agents and skills; omitted selector for LATEST; to pin a link, replaced legacy `{"commit_id":"<uuid>"}` with `{"selector":{"type":"COMMIT","commit_id":"<uuid>"}}`.
* Scaled checkbox radius by size.
* Preserved v2 filters for prod cutover.
* Used design-system link color for share panel URL.
* Allowed LangSmith preview CORS preflights.
* Stabilized inline filter controls.
* Simplified usage configuration heading.
* Aligned revamped filter scope defaults.
* Ran FE preview builds on conflicted PRs.
* Reduced false positives in chart v2 shadow comparisons.
* Stopped dropping long issue validation reasons.
* Removed replay capability gate.
* Renewed credentials in idle tabs.
* Added targets to NLB.
* Standardized sandbox CORS origin in migrated deployments.
* Increased lag and fixed feedback value comparisons.
* Throttled EU feedback traffic for noisy tenant.
* Increased feedback ingest queue maxreplicas in EU prod.
* Increased EU-prod feedback mutation RPS limits to prod levels.
* Authenticated validation replays with LangSmith keys.
* Allowed audit webhook alert creation.

**Download the Helm chart:** [`langsmith-0.17.0-rc.17.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.0-rc.17/langsmith-0.17.0-rc.17.tgz)

**2026-08-31**

## langsmith-0.17.0-rc.16

**LangSmith version:** `0.17.14rc1`

* This release packages the same LangSmith application version as langsmith-0.17.0-rc.13. Refer to the [langsmith-0.17.0-rc.13](#langsmith-0-17-0-rc-13) release notes below.

**Download the Helm chart:** [`langsmith-0.17.0-rc.16.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.0-rc.16/langsmith-0.17.0-rc.16.tgz)

**2026-08-28**

## langsmith-0.17.0-rc.15

**LangSmith version:** `0.17.14rc1`

* This release packages the same LangSmith application version as langsmith-0.17.0-rc.13. Refer to the [langsmith-0.17.0-rc.13](#langsmith-0-17-0-rc-13) release notes below.

**Download the Helm chart:** [`langsmith-0.17.0-rc.15.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.0-rc.15/langsmith-0.17.0-rc.15.tgz)

**2026-08-28**

## langsmith-0.16.14

**LangSmith version:** `0.16.47`

* This release packages the same LangSmith application version as langsmith-0.16.13. Refer to the [langsmith-0.16.13](#langsmith-0-16-13) release notes below.

**Download the Helm chart:** [`langsmith-0.16.14.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.16.14/langsmith-0.16.14.tgz)

**2026-08-28**

## langsmith-0.17.0-rc.14

**LangSmith version:** `0.17.14rc1`

* This release packages the same LangSmith application version as langsmith-0.17.0-rc.13. Refer to the [langsmith-0.17.0-rc.13](#langsmith-0-17-0-rc-13) release notes below.

**Download the Helm chart:** [`langsmith-0.17.0-rc.14.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.0-rc.14/langsmith-0.17.0-rc.14.tgz)

**2026-08-27**

## langsmith-0.16.13

**LangSmith version:** `0.16.47`

* Users with `runs:read` granted through an ABAC policy were able to open traces in projects whose tags matched the policy, while trace access remained denied for projects outside the policy scope.
* Run rules and automations avoided cross-slot transaction failures when Redis cluster-safe mode was enabled.

**Download the Helm chart:** [`langsmith-0.16.13.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.16.13/langsmith-0.16.13.tgz)

**2026-08-24**

## langsmith-0.16.12

**LangSmith version:** `0.16.46`

* Self-hosted Fleet attached access profiles whose callback URLs used Kubernetes-internal service names when the deployment enabled internal Kubernetes destinations.

**Download the Helm chart:** [`langsmith-0.16.12.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.16.12/langsmith-0.16.12.tgz)

**2026-08-24**

## langsmith-0.17.0-rc.13

**LangSmith version:** `0.17.14rc1`

* POST /v1/fleet/sandboxes created a sandbox from a snapshot and returned it ready to use, allowing a headless client on external OIDC to provision one without accessing the platform sandboxes API; you could choose the boot image with snapshot\_id or a name:tag reference, or omit both for the workspace default.
* Added Homebase breadcrumb to Langster.
* DELETE /v1/fleet/sandboxes/{sandbox_slug} removed one sandbox, allowing a headless client on external OIDC to clean up a sandbox without accessing the platform sandboxes API; it was idempotent—deleting a sandbox that was already gone still returned 204—and the sandbox was torn down in the background, so a read taken immediately after showed it in a deleting state rather than absent.
* POST /v1/fleet/sandboxes/{sandbox_slug}/files wrote a file into a sandbox from a multipart/form-data body, completing the Fleet file API alongside the existing list and read endpoints, with the path query parameter naming the destination on its own, so the upload no longer depended on accessing a sandbox's dataplane URL directly; files were streamed rather than buffered, and one over 100MB was refused with 413.
* Self-hosted Fleet could attach access profiles whose callback URLs used Kubernetes-internal service names when the deployment enabled internal Kubernetes destinations.
* Tuned Evaluators were now hidden in BYOC workspaces and self-hosted deployments, where LangChain-managed inference was unavailable.
* Fleet usage charts now displayed spend, tool, and model data instead of appearing blank.
* Deployments could now have the general-purpose agent build a new agent directly in the chat, writing its name, description, tools, triggers, and instructions, instead of showing a Create agent button that handed setup to the new agent, with FLEET\_INLINE\_AGENT\_GENERATION needed to be set on the Fleet API server, the Fleet queue, and the platform backend to turn it on; it was off by default.
* Controlled inputs no longer created redundant local state updates, preventing rare page crashes while typing in tracing filters.
* Attached a free-form description when creating or capturing a snapshot, and to proxy rules and proxy configs, with descriptions stored and returned on reads, allowing an agent to have a plain-language summary of what its sandbox image and network access could do.

**Download the Helm chart:** [`langsmith-0.17.0-rc.13.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.0-rc.13/langsmith-0.17.0-rc.13.tgz)

**2026-08-22**

## langsmith-0.17.0-rc.12

**LangSmith version:** `0.17.12rc1`

* Updated a sandbox's proxy configuration so that it no longer required the sandbox to be running; a stopped sandbox stored the new configuration and applied it the next time it started instead of rejecting the request.
* GET /v1/fleet/users listed and searched the members of your workspace by email or name, returning the user ID that agent sharing took; API-only Fleet clients no longer needed a user ID from elsewhere before sharing an agent.
* Moved periodic loops to SAQ.
* The LLM Gateway now supported xAI API keys and Grok models through native and unified Responses and Chat Completions endpoints, with tracing and spend attribution.
* LangSmith Chat now read as a record of what it did; every tool it ran got a row naming the action and what it acted on, with the result one click away; a plan appeared when it took one on, and a subagent showed the steps it was working through; long results folded to a readable height, files and diffs rendered as files and diffs, and the panel could be resized or docked to the sidebar.
* Fixed BarChart storybook sidebar bug.
* The Gateway Credits balance card now explained that credits accessed models hosted by LangChain, and the Gateway home quickstart noted that running a request cost a trace but no additional LangChain fee.
* The Model Fallbacks tab in LLM Gateway now supported filtering routing configurations by workspace and by fallback trigger status code, making it easier to find the routes that applied to a given workspace or error condition.
* Sandboxes now mounted Context Hub repositories through a read-only, host-served filesystem, so files were directly accessible without polling for asynchronous guest materialization; repository updates appeared atomically, and mounts recovered across memory-backed stop and start.
* LLM Gateway fallback policies could now route failed provider-model requests through an ordered chain of native provider models and saved model configurations; configure which HTTP status codes advanced to the next candidate, while successful requests continued directly to the original model.
* GET /v2/sandboxes/snapshots now paged with page\_size and an opaque cursor, returning items and next\_cursor; the limit and offset parameters and the snapshots and offset response fields still worked but were deprecated.
* Workspace API key creation and deletion were now gated by a new workspaces:manage-keys permission, separate from workspaces:manage; organization admins could grant a custom workspace role the ability to manage API keys without granting full workspace management.
* Automation rules scoped to threads now showed the project's thread idle time, with a link to change it in project settings.
* Default gateway spend and rate limits could now track and enforce separate buckets for each value of a configured X-Gateway request header.
* Freeform rubric items in an annotation queue now supported an optional regex validator; a reviewer's comment that didn't match the configured pattern was blocked from saving, with an inline error, instead of silently persisting.
* Custom roles could now grant feedback-configs:create, feedback-configs:update, and feedback-configs:delete independently of feedback submission, so a role could be scoped to submit feedback without also being able to create, edit, or delete feedback config (rubric) definitions.
* Context Hub repositories containing legacy files beneath linked directories could now be read, materialized, cloned, and edited; reads used the linked directory contents, and the next successful edit removed conflicting legacy entries without changing linked repositories.
* Webhook test notifications now showed the destination's HTTP status and reason phrase, helping you diagnose URL, availability, and authentication failures.
* GET /v2/sandboxes/boxes now paged with page\_size and an opaque cursor, returning items and next\_cursor; the limit and offset parameters and the sandboxes and offset response fields still worked but were deprecated.
* Gateway spend limit forms could configure custom-header buckets, and cost policy tables showed which header separated each default limit.
* Created and edited alert actions now remained in a sticky footer, so you could submit changes without scrolling to the bottom of the form.
* Annotation queues now supported a Data Formatting setting that hid selected JSON paths from a run's inputs and outputs while reviewing—pick fields via checkboxes generated from a sample run, or type a path manually; applied to run items only, not threads.
* The LLM Gateway now forwarded Claude Code Max OAuth credentials for every organization, without requiring a workspace Anthropic API key.
* Runs using the bare "gpt-5.6" model ID now calculated cost correctly; the pricing rule previously only matched the "gpt-5.6-sol" ID variant.
* Tolerated disappearing Agent Builder popover.
* The Model Fallbacks tab now let you create and manage automatic fallback chains for provider models, choosing ordered backup models or saved model configurations, selecting which HTTP errors triggered fallback, and copying a ready-to-use Gateway request example.
* Enabled shadowing v1 -> v2 charts to compare data.
* GET /v1/fleet/users now worked for Fleet deployments authenticating through an external OIDC provider, not only for API-key callers; headless clients on OIDC could resolve a colleague's user ID for agent sharing.
* GET /v1/fleet/sandboxes/{sandbox_slug}/files returned the files under a path in a sandbox, matched by a glob pattern and paged with page\_size and an opaque cursor; paging replaced the silent result cap the sandbox glob applied, so a large directory could be read in full instead of stopping partway.
* GET /v1/fleet/sandboxes/{sandbox_slug}/files/content returned the raw bytes of a file in a sandbox; byte ranges were supported via the Range header, and HEAD reported a file's size without transferring it.
* Excluded first bucket from shadowing.
* GET /v1/fleet/sandbox-snapshots/{snapshot_id} returned one sandbox snapshot, so a client could watch a snapshot's build status without re-reading the whole list; the path parameter accepted a snapshot ID or a Docker-style reference, where a bare name meant name:latest.
* Workspace roles could grant API key creation and deletion without granting full workspace administration; key managers could scope service keys to permitted workspaces and assign unrestricted roles.
* LLM Gateway model fallback policies could now route between providers that used OpenAI Chat Completions, OpenAI Responses, or Anthropic Messages formats; the gateway translated requests, non-streaming responses, and streaming responses for both unified and direct provider endpoints.
* DELETE /v1/fleet/sandbox-snapshots/{snapshot_id} removed a sandbox snapshot, which paired with snapshot creation for the delete-then-recreate retry after a failed build; it was idempotent and returned 409 while any sandbox was still booted from the snapshot, including a stopped one.

**Download the Helm chart:** [`langsmith-0.17.0-rc.12.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.0-rc.12/langsmith-0.17.0-rc.12.tgz)

**2026-08-22**

## langsmith-0.16.11

**LangSmith version:** `0.16.45`

* Deleted an agent cleanly and removed the agent's files along with it, as previously the deletion could return a permission error after the agent had already disappeared from the agent list.
* Updated the GET /v1/fleet/users endpoint to list and search members of your workspace by email or name, returning the user ID needed for agent sharing; API-only Fleet clients no longer needed a user ID from elsewhere before sharing an agent.

**Download the Helm chart:** [`langsmith-0.16.11.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.16.11/langsmith-0.16.11.tgz)

**2026-08-21**

## langsmith-0.17.0-rc.11

**LangSmith version:** `0.17.10rc1`

* This release packages the same LangSmith application version as langsmith-0.17.0-rc.7. Refer to the [langsmith-0.17.0-rc.7](#langsmith-0-17-0-rc-7) release notes below.

**Download the Helm chart:** [`langsmith-0.17.0-rc.11.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.0-rc.11/langsmith-0.17.0-rc.11.tgz)

**2026-08-20**

## langsmith-0.16.10

* This release packages the same LangSmith application version as langsmith-0.16.9. Refer to the [langsmith-0.16.9](#langsmith-0-16-9) release notes below.

**Download the Helm chart:** [`langsmith-0.16.10.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.16.10/langsmith-0.16.10.tgz)

**2026-08-20**

## langsmith-0.17.0-rc.10

* This release packages the same LangSmith application version as langsmith-0.17.0-rc.7. Refer to the [langsmith-0.17.0-rc.7](#langsmith-0-17-0-rc-7) release notes below.

**Download the Helm chart:** [`langsmith-0.17.0-rc.10.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.0-rc.10/langsmith-0.17.0-rc.10.tgz)

**2026-08-19**

## langsmith-0.17.0-rc.9

* This release packages the same LangSmith application version as langsmith-0.17.0-rc.7. Refer to the [langsmith-0.17.0-rc.7](#langsmith-0-17-0-rc-7) release notes below.

**Download the Helm chart:** [`langsmith-0.17.0-rc.9.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.0-rc.9/langsmith-0.17.0-rc.9.tgz)

**2026-08-19**

## langsmith-0.17.0-rc.8

* This release packages the same LangSmith application version as langsmith-0.17.0-rc.7. Refer to the [langsmith-0.17.0-rc.7](#langsmith-0-17-0-rc-7) release notes below.

**Download the Helm chart:** [`langsmith-0.17.0-rc.8.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.0-rc.8/langsmith-0.17.0-rc.8.tgz)

**2026-08-19**

## langsmith-0.17.0-rc.7

* Pinned full UV workspace for BYOC FE skew e2e.
* Self-hosted used model aliases.
* Engine worked in supported self-hosted deployments without Eppo rollout configuration, while organization enablement and existing permissions remained enforced.
* LangSmith Chat traces now showed the model you configured instead of mislabeling it as GPT-3.5-Turbo when a custom model endpoint was used.
* Engine no longer emitted its own LangSmith traces in self-hosted deployments, so no run content left the deployment; cloud deployments remained unchanged.
* Custom dashboard charts could now aggregate feedback scores by sum, P50, P90, P95, and P99, in addition to the existing average, min, and max.
* Online evaluator definitions now included an advanced setting to turn evaluator execution tracing on or off, with feedback generation continuing to run when tracing was disabled.
* Stopped retrying trace query timeouts, limiting to 5 attempts.
* Accepted a previous Fernet key so the key could be rotated.
* Deleting a LangGraph deployment now tore down its running resources after a one-hour grace period and permanently removed its database and metadata one week later, leaving a window to recover from an accidental deletion.
* Uploading a .csv or .jsonl dataset now worked regardless of the Content-Type the browser reported; Windows browsers labeled .csv files as an Excel type, which previously caused valid uploads to fail, and uppercase filenames such as DATASET.CSV were also accepted.
* Files attached to Slack messages were now available under /workspace/uploads for sandbox-backed agents, matching files uploaded from Fleet.
* LangSmith exposed annotation queue item endpoints for adding, listing, updating, deleting, counting, positioning, and reviewing run or thread queue items through the public API and SDK generation flow.
* Self-hosted Fleet agents could use sandbox-backed computer access without requiring a cloud billing plan tier.
* Metadata columns in the experiment comparison grid, including `example.metadata.<key>`, now rendered their values instead of staying empty.
* The Granular Usage page now showed a notice that long-lived trace usage wasn't tracked in self-hosted deployments, so the "Long-lived only" filter was expected to show zero results there.
* API-key-scoped LLM Gateway spend-cap and rate-limit policies could now add a custom X-Gateway-\* header condition, so a single API key could match different limits per header value, for example, a reseller could set separate caps per downstream customer without distributing multiple keys.
* Cleaned up Agents Context to reduce initial Token cost.
* Trace detail panes once again used an elevated background that matched their section headers.
* The custom X-Gateway-\* header condition on LLM Gateway spend-cap and rate-limit policies now worked with organization-, workspace-, and user-scoped policies too, not just API-key-scoped ones, allowing the splitting of a single subject's traffic into separate caps by header value regardless of policy scope.
* Added a reusable ChartCard component to the LangSmith design system, standardizing chart titles, move, expand, and overflow actions, responsive full-width layouts, and chart and legend spacing.
* Used three-dot diff for CI path gating.
* Made /langchain model catalog config-driven and used Kimi models.
* Stopped frontend unit path filter matching unrelated PRs.
* Self-hosted LangSmith bulk exports now defaulted to zstandard (zstd) compression instead of gzip for improved performance.
* Navigating to an agent chat with a selected agent no longer crashed while the agent details were still loading; the chat showed a loading state until the agent was ready, then rendered normally.
* Disabled keepalive on ace requests.
* Enabled annotation queues in Python and TypeScript SDKs.
* A resolved issue on an Engine Issue Board now returned to Open as soon as Engine linked a new matching trace to it; previously, the trace was filed as evidence but the issue stayed closed, so a recurring problem never resurfaced on the board. Dismissed issues stayed dismissed.
* On self-hosted installations authenticating with OAuth/SSO, the Remote MCP authorization endpoint returned a 400 because the SSO login route shadowed it; OAuth clients could now complete the authorize step and connect to the Remote MCP server.
* Gateway policies with a blank or whitespace-only name now fell back to showing the policy ID instead of rendering an empty name cell, and the policy update endpoint now rejected blank names the same way creation already did.
* Resolved duplicate Z import bug.
* The LangSmith home page now provided quick access to copy the current organization and workspace IDs.
* Used service keys instead of standing API keys and named the snapshot.
* The LLM Gateway now lived in a dedicated top-level sidebar section instead of under Settings, with a new Home tab listing your custom model configurations and a ready-to-run code snippet for the gateway; old Settings gateway links redirected automatically.
* Self-hosted deployments with an online license key (beacon access) now saw the monthly organization usage graph automatically, without needing the enable\_monthly\_usage\_charts org config, while offline deployments were now pointed to the Granular usage tab for locally-recorded billable usage.
* Sandboxes now shipped with the `langsmith` CLI on PATH, so agents could query traces, runs, and datasets without installing it first.
* Fleet now showed a warning when a Google Docs, Sheets, Drive, or Slides tool hit a 403 or 404, inline above the failing tool call in chat and as a message in Slack, explaining the agent could only access files it had created itself with its connected Google account.
* Switching workspaces or organizations kept you on the same page when the route had no workspace-specific resource IDs, and routes referencing a specific resource continued to open the destination workspace home page.
* Evaluator lists on a dataset or tracing project now showed an evaluator's current name instead of the name it had when it was attached; feedback keys were unchanged by a rename.
* Next self-hosted release preview and commit locator.
* Dataset example views restored clear spacing between the example details and tab navigation.
* The connect card now appeared above the Gateway Credits balance on the LLM Gateway Home page, and the generated code snippets listed the API key before the base URL to match common convention.
* Annotation queue item APIs used project\_id for the tracing project, and request bodies also accepted session\_id as an alias.
* Sandbox-backed Fleet agents could create or revise downloadable DOCX files without installing an authoring package during the task; a built-in skill guided document authoring and structural validation.
* Pointed Gateway Credits snippet at /langchain/v1.
* Pairwise annotation queue runs again included the tracing project ID needed to create feedback when ClickHouse query support was disabled.
* Fleet agents could send workspace files to Slack channels, threads, and direct messages using slack\_send\_file and slack\_send\_file\_to\_user.
* The Gateway Credits purchase dialog now showed the credit balance your purchase would land you on and stated the fee-inclusive total directly above a single purchase button; large amounts no longer pushed the credits readout and total outside the dialog.
* Negative feedback-key filters now returned matching traces correctly when ClickHouse used optimized runs tables.
* The annotation queue item endpoints were now documented at their served path under /api/v1/platform, so the generated SDK methods for listing, adding, updating, counting, deleting, and placing queue items reached the API instead of returning 404.
* Yielded lossy for `stream_options.include_usage` on fusion responses.
* Added Gateway Policies and Gateway Credits rows to plan matrix.
* Logged completed langchain provider credit purchases.
* The `langsmith` CLI in sandboxes was updated to v0.2.44, and its requests now resolved on self-hosted deployments that served the API under `/api`, where commands such as `trace messages` and the project issues commands previously failed.
* When a model provider rejected a playground run, such as a wrong API key or an exhausted quota, the playground now showed the provider's own error message instead of a generic server error, clarifying the cause from the error itself.
* Deleting a tracing project whose LangGraph deployment was still within its post-deletion retention window now scheduled the project to be removed along with the deployment, and explained that in the error message instead of asking you to delete a deployment you already deleted.
* The new agent creation experience was now enabled for everyone, with the assistant surfacing the Create agent button, and the new agent running its own setup conversation instead of being built inline.
* Forking an evaluator attached the copy to the project or dataset named in the fork dialog; previously, the copy could be created attached to nothing, leaving the original evaluator running the version you had just edited away from.
* The delete confirmation for a LangGraph deployment now stated that cleanup of the underlying database ran after you confirmed, and that a deleted deployment's name stayed reserved until that cleanup finished.
* When you selected Gateway Credits during onboarding, the prompt copied into your coding agent now included the correct Gateway URL for your deployment.
* Restored the dedup/lifecycle block removed in #30448.
* LLM Gateway Home now highlighted the selected model and allowed switching connect samples between Chat Completions, Messages, and Responses formats.
* PDFs and other documents attached to a message now rendered in a full-width preview frame with a header control that opened them nearly full screen, instead of collapsing to a thumbnail-sized box.
* Tracing project activity and sorting stayed up to date for self-hosted deployments using Redis versions before 6.2.
* Engine sandbox commands in self-hosted deployments now authenticated over WebSocket with the deployment service key, preventing 401 failures after successful sandbox creation.
* Run filters now supported total, prompt, and completion token counts and costs consistently across routed query backends.
* `POST /api/v1/runs/stats` now returned a 404 when the requested tracing project did not exist in your workspace, and reported other client errors, such as a `start_time` older than the supported lookback window, with their real status and message instead of a generic 500 internal server error.
* LangGraph approached with colocated UI and actions.
* A conversation whose stored state grew past the API's usual single-response size limit now loaded in full, up to 32 MiB, instead of failing; the response marked the conversation as oversized, and updates to it still failed until its state shrank.
* Sandboxes accepted a new streaming execute request that returned stdout and stderr as Server-Sent Events, for clients that could not hold a WebSocket; passing a command ID reused a running command, and a separate resume request continued an interrupted stream instead of running the command again.
* The Cost Controls and Model Fallbacks shortcuts on LLM Gateway Home now read "View cost controls"/"View model fallbacks" for members who couldn't manage the org, instead of "Manage"/"Configure".
* Gateway usage spend chart now showed the top 12 individual spenders per bucket, rolling the rest into an "Other" series, with its hover tooltip listing every contributor at once alongside the bucket total pinned beneath them.
* Used a non-colliding release branch name for langster-skills.
* The Gateway Usage tab no longer showed an in-page workspace dropdown, because the page was already scoped to your current workspace; its subtitle now named that workspace directly.
* Hid workspace picker on OIDC OAuth consent.
* Hotfixes page (stacked).
* The Configure Evaluator pane's header and templates navigation again painted the same background as the pane itself in dark mode.
* Deleted an entire trace from the run details actions menu after confirming the destructive action.
* On a tracing project, resetting a view now moved the Threads/Traces/Runs switcher back in step with the rows being shown; previously, the switcher could stay on Runs while the table had already returned to traces.
* Self-hosted deployments now caught up missing tracing project last-run timestamps so project sorting reflected recent historical activity.
* Homepage spacing and surface tinting now matched design review feedback, and several small copy fixes clarified credit limits, provider status, and organization-level purchase limits.
* When a project configured a custom output renderer, the trace Output section now offered it as a Custom option alongside Markdown, Plain, JSON, and YAML instead of replacing them; Custom remained the default, and your choice was remembered.
* Skipped backfill release-train check on fresh installs.
* Requests that set prompt\_cache\_options (or the deprecated prompt\_cache\_retention) now enabled Anthropic prompt caching when the LLM Gateway translated an OpenAI Chat Completions or Responses request to a Claude model, instead of ignoring the field; Anthropic's default cache lifetime applied, and prompt\_cache\_key, prompt\_cache\_retention, and prompt\_cache\_options were all preserved when translating between the Chat Completions and Responses formats.
* Fleet agents now correctly routed sandbox creation and org config requests to the Go platform-backend service on self-hosted deployments where the Go and Python services ran on separate addresses, eliminating the need for a reverse-proxy workaround.
* Correcting an evaluator score from the experiment results grid now updated the cell and its popover right away instead of requiring a page refresh.
* The prompts list no longer displayed a persistent LangChain Hub banner at the bottom of the page.
* Used live smith-frontend design system.
* Engine run webhooks and sandbox links now resolved the externally reachable API base from LANGSMITH\_PUBLIC\_API\_ENDPOINT, falling back to LANGCHAIN\_PLATFORM\_ENDPOINT and then LANGCHAIN\_ENDPOINT; installs whose chart set only LANGSMITH\_PUBLIC\_API\_ENDPOINT were building relative URLs, which made every non-shadow Engine run fail because the run webhook was rejected as a loopback address.
* llm-gateway: init metronome client from the gateway process.
* Dataset JSON schema descriptions were now safely rendered in editor tooltips.
* Showed gateway and credits widget in sidebar in all cases except for self-hosted and non-dataplane workspaces.
* Dataset and run attachments now resolved relative signed download URLs before previewing, opening, or downloading them in self-hosted deployments.
* Creating a dataset from the Datasets or Home empty state now opened the new dataset instead of briefly showing a Page not found screen.
* Playground batch and invoke endpoints now sanitized buffered run trees into JSON-safe payloads before responding, so online evaluations no longer failed with opaque 500s when a run graph could not be serialized.
* Listing or counting examples with an unsupported `filter` expression, such as an unfilterable attribute or a `has(...)` comparison whose value was not valid JSON, now returned a 422 naming the `filter` parameter instead of a 500.
* Feedback corrections could now reset a score to its original value, including zero.
* New connections to the hosted LangSmith MCP server failed to register when the client requested a confidential authentication method; dynamic client registration now issued a public client in that case instead of returning an error, so connecting from Claude and other MCP clients worked again.
* Requests to moonshotai/kimi-k3 and moonshotai/kimi-k2.6 through gateway credit models in the LLM gateway were now matched against a price map when sent in user-traced code.
* Self-hosted deployment forms now supported Redis CPU and memory requests and limits, and the configured values were applied to the Redis workload managed by the Kubernetes operator.
* Claude models on Gemini Enterprise Agent Platform now loaded successfully in the Playground when no credentials secret was configured, matching existing Gemini behavior under GCP Workload Identity or AWS IRSA.
* Set a resource tag key or value description to `null` to clear it through the PATCH API.
* Insights reports only analyzed traces, so the "Is Trace" condition in a report's filter was now fixed; setting it to false previously produced a report that ran successfully but never found any insights.
* Large PDF, JSON, and CSV previews on a message now rendered instead of showing an empty frame, and PDF and JSON previews gained an open-in-new-tab control next to the expand control.
* Sandbox-backed Fleet agents could build a new deck, revise an existing one, and answer questions about the contents of a .pptx file without installing presentation tooling first; a built-in skill guided authoring and validated the file before delivery.
* While an agent worked on a turn, the chat now showed a live elapsed-time count that appeared after a couple of seconds and picked up a rotating status label on longer waits, so a slow turn read as in progress rather than stalled; models that streamed reasoning still collapsed to the time they spent thinking once the answer arrived.
* Resuming a suspended sandbox now checked your organization's real sandbox quota, including plan-specific limits, instead of the default cap; requests that genuinely exceeded quota returned 429 with a quota message rather than 502 Bad Gateway.
* Chart headers on dashboards no longer overflowed or wrapped when the title or description was long: the description now truncated with a hover tooltip revealing the full text. The expand-chart action also picked up the standard icon-button hover treatment.
* The Create New Deployment form now showed a clear, per-field message when a submitted value failed validation (e.g. an invalid image path) instead of the raw backend error payload.
* The Engine tab was visible again on tracing projects before Engine was turned on, so admins could enable it, members could request access, and personal organizations could upgrade, all from the tab itself.
* Online self-hosted LangSmith installations now reported finalized sandbox uptime and resource usage for billing when phone-home usage reporting was enabled; offline and opted-out installations did not send sandbox usage.
* Self-hosted LangSmith now enabled sandbox API and UI access only when the deployment license included sandbox access.
* Waterfall filters in thread details now kept deeply nested matches visible and preserved filter controls while newly ingested traces were still appearing.
* Updated FE agent skill & lint based on feedback.
* Creating or validating an example with a `dataset_id` that was not a well-formed UUID now returned a 422 naming the field instead of a 500.
* Adding a provider API key now started from a provider picker that filled in the correct secret key name for you, with a Custom option for anything else; in the LLM Gateway, you could add a provider's required secret without leaving the connect screen.
* Allowed disabling specific dashboards via FF.
* Renamed the traces tile and named its estimate window.
* Sandbox-backed Fleet agents could create spreadsheets, revise existing workbooks, and answer questions about .xlsx and .xlsm files without installing spreadsheet tooling first; a built-in skill guided safe openpyxl usage and validated each workbook before delivery.
* Bedrock requests through the LLM gateway now used the Amazon Bedrock price map so their costs were calculated correctly.
* Auto-resolution verdicts for stale issues (log-only).
* Creating an experiment no longer converted an existing tracing project with the same name; you could rename the experiment or choose a new project name when a conflict existed.
* The section sidebar in the manual Insights configuration no longer collapsed when a panel's contents were wide, such as long model IDs on the General tab.
* Engine was now enabled by default for organizations on a self-serve plan, allowing you to open the Engine tab on any project and start analyzing traces without an admin turning it on first; organizations that explicitly disabled Engine remained disabled, and an admin could still turn it off under Settings → Engine.
* Access-policy endpoints now reported errors as RFC 7807 problem details; error messages moved from the `error` field to `detail`, and semantically invalid request bodies returned HTTP 422.
* LangSmith now rejected credential-bearing and non-GitHub remote URLs when rendering evaluation commit links.
* When an agent read a file its model couldn't accept as an attachment, Fleet now substituted a short explanation instead of failing the request. Conversations that previously became stuck recovered on their next message.
* Clarified the fields used to create a new Fleet agent.
* Group by metadata and metadata columns were selectable again in the experiment comparison view.
* Updated ABAC access policies and detached policies from roles through the public API.
* The Prompts page now supported filtering by prompt type, prompt tags, and commit tags, allowing you to quickly narrow the list down to the prompts you were looking for.
* Attachments stored on a run now appeared when you reviewed it in an annotation queue, including pairwise queues; previously, only media inlined in the run's inputs or outputs was shown.
* Scrolling through large experiment comparison results no longer re-fetched the first page of examples on every lazy-load, cutting redundant network traffic and reducing load time.
* Chat model runs sent through the gateway's unified endpoint with provider/model slugs now matched model pricing rules, producing accurate trace costs.
* Engine GitHub settings now linked to setup instructions for LangSmith Cloud and self-hosted deployments, with clearer guidance when a connection failed.
* Resolved PortalSlot import in TracingToolbarSlot.
* PDF attachment icons now aligned consistently with other file types in attachment lists.
* Rolling back a deployment that was created from an uploaded source archive now redeployed that revision's archive instead of the most recent one.
* Added Environment variables page.
* Engine spend controls now explained that new runs paused at the monthly limit while runs already in progress might finish and increase billed spend beyond it.
* LangSmith MCP's `fetch_runs` tool could now include invocation parameters, including the tool and function schemas sent to an LLM, for easier tool-calling diagnosis.
* Wrapped shell in TooltipProvider.
* Self-hosted deployments refreshed their license every 5 minutes instead of every 24 hours, so entitlement changes took effect shortly after they were made; a failed refresh no longer restarted the service; it kept using the last verified license until that license's own expiry. The tuning knob was now LICENSE\_REFRESH\_INTERVAL\_SECONDS (default 300), replacing LICENSE\_REFRESH\_INTERVAL\_HOURS.
* The credit balance now showed above the connect card, and the shortcut cards for cost controls, model fallbacks, and spend monitoring stayed visible (locked, with an "Upgrade plan" prompt) instead of disappearing for Developer-plan orgs.
* Role permission and access policy changes now invalidated cached authorization results reliably, including when an older transaction committed after a newer update.
* The evaluator spend table kept the All runs filter badge inactive when an evaluator had no filters.
* Attachment and object downloads now always declared how the browser should handle the response; files whose type was unrecognized, or that were stored without a type, were delivered as downloads instead of being rendered in the page.
* Engine scans on non-coding-agent boards applied the configured priority chips, user instructions, and a trace-scope filter instead of reviewing the whole project.

**Download the Helm chart:** [`langsmith-0.17.0-rc.7.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.0-rc.7/langsmith-0.17.0-rc.7.tgz)

**2026-08-19**

## langsmith-0.16.9

* GCP Redis IAM cluster discovery now used TLS when the Redis cluster TLS was enabled, allowing self-hosted deployments to combine IAM authentication with TLS-required Memorystore clusters.

**Download the Helm chart:** [`langsmith-0.16.9.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.16.9/langsmith-0.16.9.tgz)

**2026-08-18**

## langsmith-0.16.8

* Self-hosted v16 deployments could attach and detach ABAC access policies from roles through the canonical organization API.
* The Microsoft Teams reply-to-channel tool now asked for approval by default, matching the other Teams write tools; agents that already set the tool to run automatically kept their current behavior, and you could switch it back to Auto per agent.

**Download the Helm chart:** [`langsmith-0.16.8.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.16.8/langsmith-0.16.8.tgz)

**2026-08-16**

## langsmith-0.16.7

* LangSmith workers using Microsoft Entra ID authentication for standalone Redis started successfully and continued refreshing credentials after the event loop starts.

**Download the Helm chart:** [`langsmith-0.16.7.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.16.7/langsmith-0.16.7.tgz)

**2026-08-14**

## langsmith-0.16.6

* This release packages the same LangSmith application version as langsmith-0.16.5. Refer to the [langsmith-0.16.5](#langsmith-0-16-5) release notes below.

**Download the Helm chart:** [`langsmith-0.16.6.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.16.6/langsmith-0.16.6.tgz)

**2026-08-13**

## langsmith-0.16.5

* Internal improvements and maintenance updates

**Download the Helm chart:** [`langsmith-0.16.5.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.16.5/langsmith-0.16.5.tgz)

**2026-08-12**

## langsmith-0.16.4

* This release packages the same LangSmith application version as langsmith-0.16.2. Refer to the [langsmith-0.16.2](#langsmith-0-16-2) release notes below.

**Download the Helm chart:** [`langsmith-0.16.4.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.16.4/langsmith-0.16.4.tgz)

**2026-08-12**

## langsmith-0.17.0-rc.6

* This release packages the same LangSmith application version as langsmith-0.17.0-rc.1. Refer to the [langsmith-0.17.0-rc.1](#langsmith-0-17-0-rc-1) release notes below.

**Download the Helm chart:** [`langsmith-0.17.0-rc.6.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.0-rc.6/langsmith-0.17.0-rc.6.tgz)

**2026-08-11**

## langsmith-0.16.3

* This release packages the same LangSmith application version as langsmith-0.16.2. Refer to the [langsmith-0.16.2](#langsmith-0-16-2) release notes below.

**Download the Helm chart:** [`langsmith-0.16.3.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.16.3/langsmith-0.16.3.tgz)

**2026-08-11**

## langsmith-0.17.0-rc.5

* This release packages the same LangSmith application version as langsmith-0.17.0-rc.1. Refer to the [langsmith-0.17.0-rc.1](#langsmith-0-17-0-rc-1) release notes below.

**Download the Helm chart:** [`langsmith-0.17.0-rc.5.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.0-rc.5/langsmith-0.17.0-rc.5.tgz)

**2026-08-11**

## langsmith-0.16.2

* Self-hosted Fleet agents can use sandbox-backed computer access without requiring a cloud billing plan tier.

**Download the Helm chart:** [`langsmith-0.16.2.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.16.2/langsmith-0.16.2.tgz)

**2026-08-07**

## langsmith-0.17.0-rc.4

* This release packages the same LangSmith application version as langsmith-0.17.0-rc.1. Refer to the [langsmith-0.17.0-rc.1](#langsmith-0-17-0-rc-1) release notes below.

**Download the Helm chart:** [`langsmith-0.17.0-rc.4.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.0-rc.4/langsmith-0.17.0-rc.4.tgz)

**2026-08-07**

## langsmith-0.16.1

* Fixed issues with initial file uploads on Sandbox-backed Fleet agents.

**Download the Helm chart:** [`langsmith-0.16.1.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.16.1/langsmith-0.16.1.tgz)

**2026-08-05**

## langsmith-0.16.0

LangSmith Self-Hosted v0.16 is our recommended release for all self-hosted deployments. It brings three major capabilities to Self-hosted: **SmithDB**, **Engine**, and **Sandboxes**, alongside broad improvements across the rest of our platform.

Follow the upgrade instructions to get access to everything: [https://docs.langchain.com/langsmith/self-host-upgrades](../Manage%20an%20instance/Upgrade%20an%20installation.md).

If you want to book time for your upgrade, feel free to contact LangChain support at `support@langchain.dev`.

### Breaking changes

* The `agent-bootstrap` script is fully deprecated and deleted. If you used `agent-bootstrap` to deploy Fleet (formerly Agent Builder), migrate to a standalone deployment. For more information, see [Migrating LangSmith Deployments control plane Fleet to standalone Fleet](https://support.langchain.com/articles/8306585004-migrating-langsmith-deployments-control-plane-fleet-to-standalone-fleet).
* A new `backfillCheck` job prevents upgrading versions before required checks complete. If you rely on features such as IAM-based auth in other services, you may need to add matching annotations and labels.

### Infrastructure changes

* Several images are consolidated into the `smith-backend` image. You no longer need to mirror images such as `go-backend`, `playground`, and `host-backend`. If you previously overrode these, remove them from your `values.yaml`.
* Agent images such as `polly`, `fleet`, and `insightsEngine` are now at par with core observability images. They support IAM auth for dependencies as well as FIPS compatibility.
* Self-hosted images ship with Cosign signatures and signed SBOM attestations, so you can verify provenance and satisfy supply-chain requirements out of the box.

### New features

* **SmithDB** is available in public beta. LangChain does not support or recommend setting this up on your own. Express interest through the [SmithDB early access waitlist](https://www.langchain.com/smithdb-early-access-waitlist) and the team will reach out to set you up for success with SmithDB.
  * A columnar database purpose-built for LangSmith run and trace data, replacing ClickHouse as the query engine for runs.
  * Faster trace and run queries on large projects, and the backing store for the expanded custom dashboard metrics in this release.
  * Can run as the sole query path with ClickHouse disabled, or alongside ClickHouse during migration. Runs, threads, and stats are served from `/v2/*` endpoints.
* **Self-hosted Engine** is available in AWS/GCP US. For installation instructions, see [LangSmith Engine on self-hosted](../../../Engine/Self-hosted%20and%20BYOC/LangSmith%20Engine%20on%20Self-hosted%20and%20BYOC.md). You may need to contact your account representative to enable this feature on your license.
  * The agent for agent engineering: Engine works from your production traces to surface recurring issues, diagnose their root cause, and drive the fix.
  * Continuously scans enabled tracing projects, identifying failures and potential improvements and turning them into actionable issues ranked by severity.
  * Proposes fixes, opens PRs if source code is connected, creates evaluators and ground truth examples to catch regressions, and monitors issues automatically for recurrence.
  * Usage is charged in [LangChain Compute Units (LCUs)](https://docs.langchain.com/langsmith/pricing-plans.md) with an optional monthly spend limit at the organization and project level. On self-hosted, Engine emits no LangSmith traces.
  * Sends trace content to LangSmith Intelligence, a LangChain-managed zero-data-retention service. Requires egress to `beacon.langchain.com` on GCP or `beacon.aws.langchain.com` on AWS. Air-gapped installs cannot run Engine.
* **Self-hosted Sandboxes** are available in AWS and GCP. For installation instructions, see [Enable sandboxes](../Install%20an%20instance/Additional%20features/Enable%20Sandboxes/Enable%20Sandboxes%20on%20self-hosted%20LangSmith.md) and [LangSmith Sandboxes](../../../Deploy/Sandboxes/LangSmith%20Sandboxes.md). You may need to contact your account representative to enable this feature on your license.
  * Isolated environments where agents can safely execute arbitrary code and interact with a filesystem without touching your main infrastructure.
  * Boot from snapshots built off a Docker image, a local `Dockerfile`, or a captured running sandbox, and mount S3, GCS, and Git repositories without exposing credentials to the agent.
  * Auth proxy to keep credentials out of the runtime.
* **Platform and tooling**
  * **LangSmith MCP**: Point any MCP-capable client at your instance to read traces, projects, datasets, and prompts. For more information, see [LangSmith Remote MCP](../../../Monitor/Debug/Viewing%20%26%20managing%20traces/LangSmith%20Remote%20MCP.md). Remote MCP OAuth authorize now works on Self-hosted with SSO.
  * **LangSmith OAuth tokens**: Browser-based login via `langsmith auth login`, issuing short-lived access tokens and a refresh token, plus profiles for sharing endpoint, workspace, and auth config across the CLI and SDKs. For more information, see [LangSmith CLI](../../Govern/Tools/LangSmith%20CLI.md).
    * **Terraform provider**: Manage workspaces, custom roles, organization and workspace members, evaluators, run rules, and alert rules as code. For more information, see [Manage LangSmith with Terraform](../../Govern/Organization/Manage%20LangSmith%20with%20Terraform.md).
  * **Deployment**: Rename a deployment from Settings, create multiple cron schedules with the same expression on one agent, and see cron schedules in your local timezone.
* **Observability and evaluation**
  * **Run details panel**: Redesigned, with feedback submission directly in the panel.
  * **Threads view**: Shows the actual last output plus a new Last Error column.
  * **Scoped trace limits**: Manage per-project and per-user monthly trace limits, with banners and visibility on the Usage limits page.
  * **Monitoring hooks**: Run-rule webhook payloads include a `trace_url` deep link, and queue workers emit Prometheus metrics.
  * **OpenTelemetry**: Custom trace metadata from OTel resource attributes, and child spans arriving before their parent are now buffered and nested correctly instead of dropped.
  * **Reusable evaluators**: LLM-as-judge evaluators can include extended stats.
  * **Annotation queue permissions**: ABAC support.
  * **Experiment progress tracking**: Progress bar shows run and evaluator execution progress.
  * **Dataset splits**: Shown as chips and editable from the experiment and comparison tables.
  * **Bulk experiment exports**: A new `all_experiments` parameter exports every experiment in a workspace (250 per export, raisable on request).
  * **Context Hub webhooks**: Configure workspace-wide HTTPS webhooks that fire on every agent or skill commit, with HMAC-SHA256 signed payloads, custom request headers, and in-place secret rotation. For more information, see [Configure Context Hub commit webhooks](../../../Deploy/Prompt%20%26%20Context%20Hub/Context%20Hub/Configure%20Context%20Hub%20commit%20webhooks.md).
* **Model support**: Claude Sonnet 5, Claude Fable 5, Claude Opus 4.8, Gemini 3.6 Flash, Gemini 3.5 Flash Lite, and Databricks models. New Anthropic playground sessions default to Claude Sonnet 5. OAuth client credentials are supported for model configurations.
* Numerous bug fixes and smaller improvements.

### Admin changes

* Organization admins can update an existing [service key's](../../Govern/Organization/Overview.md#service-keys) role without rotating it.
* Rename your [organization](../../Govern/Organization/Workspace%20setup/Set%20up%20hierarchy.md#set-up-an-organization), and manage [SCIM tokens](../../Govern/Users%20%26%20access%20control/User%20management.md#set-up-scim-for-your-organization), from organization settings.
* [Disable model providers](../../Govern/Organization/Workspace%20setup/Manage%20model%20configurations.md#disable-a-provider-for-the-organization) for an entire organization.
* [Edit pending member invite roles](../../Govern/Users%20%26%20access%20control/User%20management.md#assign-a-role-to-a-user) from the UI.
* [Restrict roles](../../Govern/Users%20%26%20access%20control/Role-based%20access%20control.md#restrict-roles) from the Organizations tab.
* Workspace batch invite handles existing organization members instead of returning 409, and respects [disabled organization invites](../../Govern/Users%20%26%20access%20control/Manage%20user%20access%20in%20SSO%20organizations.md).
* Organization and workspace IDs are shown on the home page, and [workspace switching](../../Govern/Organization/Workspace%20setup/Set%20up%20hierarchy.md#manage-and-navigate-workspaces) preserves your current page.
* The monthly [usage graph](../../Account/Billing%20%26%20usage/View%20usage.md#aggregate-usage-on-self-hosted) shows automatically on online Self-hosted deployments.

**Download the Helm chart:** [`langsmith-0.16.0.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.16.0/langsmith-0.16.0.tgz)

**2026-08-04**

## langsmith-0.16.0-rc.29

* Dataset and run attachments resolved relative signed download URLs before previewing, opening, or downloading them in self-hosted deployments.
* Fixed dynamic client registration for the LangSmith MCP server so that clients requesting a confidential authentication method are issued a public client instead of an error.
* Online self-hosted installations reported finalized sandbox uptime and resource usage for billing when phone-home usage reporting is enabled. Offline and opted-out installations do not send sandbox usage.
* Self-hosted LangSmith enabled sandbox API and UI access only when the deployment license includes sandbox access.
* Added Redis CPU and memory requests and limits to self-hosted deployment forms, applied to the Redis workload managed by the Kubernetes operator.

**Download the Helm chart:** [`langsmith-0.16.0-rc.29.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.16.0-rc.29/langsmith-0.16.0-rc.29.tgz)

**2026-08-04**

## langsmith-0.16.0-rc.28

* Correcting an evaluator score from the experiment results grid updated the cell and its popover immediately, without requiring a page refresh.
* Engine run webhooks and sandbox links resolved the externally reachable API base from `LANGSMITH_PUBLIC_API_ENDPOINT`, falling back to `LANGCHAIN_PLATFORM_ENDPOINT` and then `LANGCHAIN_ENDPOINT`. Installations that set only `LANGSMITH_PUBLIC_API_ENDPOINT` previously built relative URLs, which caused every non-shadow Engine run to fail.
* Added a streaming sandbox execute request that returns stdout and stderr as Server-Sent Events, for clients that cannot hold a WebSocket. Passing a command ID reuses a running command, and a separate resume request continues an interrupted stream.
* Self-hosted deployments with an online license key showed the monthly organization usage graph automatically, without the `enable_monthly_usage_charts` organization config. Offline deployments now point to the Granular usage tab for locally recorded billable usage.

**Download the Helm chart:** [`langsmith-0.16.0-rc.28.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.16.0-rc.28/langsmith-0.16.0-rc.28.tgz)

**2026-08-01**

## langsmith-0.16.0-rc.27

* The Configure Evaluator pane header and templates navigation painted the same background as the pane itself in dark mode.
* Self-hosted deployments caught up missing tracing project last-run timestamps, so project sorting reflects recent historical activity.

**Download the Helm chart:** [`langsmith-0.16.0-rc.27.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.16.0-rc.27/langsmith-0.16.0-rc.27.tgz)

**2026-07-31**

## langsmith-0.16.0-rc.26

* This release packages the same LangSmith application version as langsmith-0.16.0-rc.25. Refer to the [langsmith-0.16.0-rc.25](#langsmith-0-16-0-rc-25) release notes below.

**Download the Helm chart:** [`langsmith-0.16.0-rc.26.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.16.0-rc.26/langsmith-0.16.0-rc.26.tgz)

**2026-07-31**

## langsmith-0.16.0-rc.25

* Internal improvements and maintenance updates

**Download the Helm chart:** [`langsmith-0.16.0-rc.25.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.16.0-rc.25/langsmith-0.16.0-rc.25.tgz)

**2026-07-31**

## langsmith-0.16.0-rc.24

* Tracing project activity and sorting stayed up to date for self-hosted deployments using Redis versions before 6.2.
* Dataset example views restored clear spacing between the example details and tab navigation.
* The evaluator onboarding navigation matched the background of the surrounding pane.
* The evaluator spend view listed only gateway-routed providers as tracked.
* Metadata columns in the experiment comparison grid, including `example.metadata.<key>`, rendered their values instead of staying empty.
* Uploading a `.csv` or `.jsonl` dataset worked regardless of the Content-Type reported by the browser. Windows browsers label `.csv` files as an Excel type, which previously caused valid uploads to fail. Uppercase filenames such as `DATASET.CSV` are also accepted.

**Download the Helm chart:** [`langsmith-0.16.0-rc.24.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.16.0-rc.24/langsmith-0.16.0-rc.24.tgz)

**2026-07-31**

## langsmith-0.16.0-rc.23

* Updated the `langsmith` CLI in sandboxes to v0.2.44. Its requests now resolve on self-hosted deployments that serve the API under `/api`, where commands such as `trace messages` and the project issues commands previously failed.
* Negative feedback-key filters returned matching traces correctly when ClickHouse uses optimized runs tables.

**Download the Helm chart:** [`langsmith-0.16.0-rc.23.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.16.0-rc.23/langsmith-0.16.0-rc.23.tgz)

**2026-07-29**

## langsmith-0.16.0-rc.22

* The Granular usage page showed a notice that long-lived trace usage is not tracked in self-hosted deployments, so the Long-lived only filter is expected to return zero results.

**Download the Helm chart:** [`langsmith-0.16.0-rc.22.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.16.0-rc.22/langsmith-0.16.0-rc.22.tgz)

**2026-07-28**

## langsmith-0.17.0-rc.3

* This release packages the same LangSmith application version as langsmith-0.17.0-rc.1. Refer to the [langsmith-0.17.0-rc.1](#langsmith-0-17-0-rc-1) release notes below.

**Download the Helm chart:** [`langsmith-0.17.0-rc.3.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.0-rc.3/langsmith-0.17.0-rc.3.tgz)

**2026-07-28**

## langsmith-0.16.0-rc.21

* This release packages the same LangSmith application version as langsmith-0.16.0-rc.20. Refer to the [langsmith-0.16.0-rc.20](#langsmith-0-16-0-rc-20) release notes below.

**Download the Helm chart:** [`langsmith-0.16.0-rc.21.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.16.0-rc.21/langsmith-0.16.0-rc.21.tgz)

**2026-07-28**

## langsmith-0.16.0-rc.20

* Internal improvements and maintenance updates

**Download the Helm chart:** [`langsmith-0.16.0-rc.20.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.16.0-rc.20/langsmith-0.16.0-rc.20.tgz)

**2026-07-27**

## langsmith-0.17.0-rc.2

* This release packages the same LangSmith application version as langsmith-0.17.0-rc.1. Refer to the [langsmith-0.17.0-rc.1](#langsmith-0-17-0-rc-1) release notes below.

**Download the Helm chart:** [`langsmith-0.17.0-rc.2.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.0-rc.2/langsmith-0.17.0-rc.2.tgz)

**2026-07-27**

## langsmith-0.17.0-rc.1

* Engine worked in supported self-hosted deployments without Eppo rollout configuration, while organization enablement and existing permissions remain enforced.

**Download the Helm chart:** [`langsmith-0.17.0-rc.1.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.17.0-rc.1/langsmith-0.17.0-rc.1.tgz)

**2026-07-27**

## langsmith-0.16.0-rc.19

* This release packages the same LangSmith application version as langsmith-0.16.0-rc.18. Refer to the [langsmith-0.16.0-rc.18](#langsmith-0-16-0-rc-18) release notes below.

**Download the Helm chart:** [`langsmith-0.16.0-rc.19.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.16.0-rc.19/langsmith-0.16.0-rc.19.tgz)

**2026-07-27**

## langsmith-0.16.0-rc.18

* Internal improvements and maintenance updates

**Download the Helm chart:** [`langsmith-0.16.0-rc.18.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.16.0-rc.18/langsmith-0.16.0-rc.18.tgz)

**2026-07-27**

## langsmith-0.15.17

* Internal improvements and maintenance updates

**Download the Helm chart:** [`langsmith-0.15.17.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.15.17/langsmith-0.15.17.tgz)

**2026-07-26**

## langsmith-0.16.0-rc.17

* This release packages the same LangSmith application version as langsmith-0.16.0-rc.16. Refer to the [langsmith-0.16.0-rc.16](#langsmith-0-16-0-rc-16) release notes below.

**Download the Helm chart:** [`langsmith-0.16.0-rc.17.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.16.0-rc.17/langsmith-0.16.0-rc.17.tgz)

**2026-07-25**

## langsmith-0.16.0-rc.16

* Giving feedback on a thread annotation queue item recorded the last reviewed time using the queue membership ID, so review progress is saved for both runs and threads.
* The LLM Gateway spend chart and table labeled spend from service keys as "Unaffiliated with any user" instead of showing a blank name, with a tooltip explaining that the spend came from a workspace-scoped or organization-scoped key.
* Hybrid deployments remained compatible with older listeners during control plane upgrades, preventing new deployments from staying queued.
* The Spend share column on the LLM Gateway monitoring spend dashboard no longer cut off its header text.
* Stat card and table headers in the Spend tab of the LLM Gateway monitoring page capitalized every word, matching the header style used elsewhere.
* Selecting a specific start and end date in the LLM Gateway monitoring date range picker showed the dates in UTC and appended "(UTC)" to the button. Relative ranges such as Last 7 days are unaffected.
* Fresh deployments tolerated an unmigrated billing configuration.
* Custom output renderer URLs were restricted to HTTPS.
* Fixed routing for `/api/v1/info` in single-origin deployments.
* Bulk-adding runs from a tracing project listed the default dataset of that project first in the dataset picker.

**Download the Helm chart:** [`langsmith-0.16.0-rc.16.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.16.0-rc.16/langsmith-0.16.0-rc.16.tgz)

**2026-07-24**

## langsmith-0.15.16

* Internal improvements and maintenance updates

**Download the Helm chart:** [`langsmith-0.15.16.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.15.16/langsmith-0.15.16.tgz)

**2026-07-24**

## langsmith-0.16.0-rc.15

* None (internal engine triage behavior, behind the `ISSUES_AGENT_MAIN_AGENT_SEMANTIC` flag).

**Download the Helm chart:** [`langsmith-0.16.0-rc.15.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.16.0-rc.15/langsmith-0.16.0-rc.15.tgz)

**2026-07-21**

## langsmith-0.16.0-rc.14

* Fixed incorrect dashboard tooltip time ranges when the first aggregation bucket was partial.
* Fixed engine issue-detection evaluators that failed on large agent traces by trimming the run payload sent to the evaluator sandbox to only what the evaluators actually read.

**Download the Helm chart:** [`langsmith-0.16.0-rc.14.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.16.0-rc.14/langsmith-0.16.0-rc.14.tgz)

**2026-07-16**

## langsmith-0.16.0-rc.13

* This release packages the same LangSmith application version as langsmith-0.16.0-rc.12. Refer to the [langsmith-0.16.0-rc.12](#langsmith-0-16-0-rc-12) release notes below.

**Download the Helm chart:** [`langsmith-0.16.0-rc.13.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.16.0-rc.13/langsmith-0.16.0-rc.13.tgz)

**2026-07-09**

## langsmith-0.16.0-rc.12

* Evaluator detach confirmation dialog showed a "Detach" button instead of "Delete".

* Include extended stats was made available to all organizations for code evaluators.

* Added two dedicated permissions `bulk-exports:read` and `bulk-exports:manage` for fetching and creating/updating bulk exports.

* Fixed the Engine "Connect GitHub" flow when the GitHub App was already installed via another workspace in the same organization.

* Bumped `@langchain/langgraph-sdk` to 1.9.4 in `smith-frontend`.

* Added an opt-in Smith-ACE v2 sandbox implementation behind `SMITH_ACE_SANDBOX_IMPLEMENTATION=v2`.

* Threads table showed the actual last output in the *Last Output* column and surfaced thread-level errors in a new *Last Error* column.

* Hid the \$0.00 cost badge for tool calls in the trace tree view.

* Users could now create multiple cron schedules with the same expression on the same agent.

* Agent Builder "View agent traces" and "View trace" links always opened in the fleet tracing project.

* Added LangSmith model pricing entry for `gemini-3.1-flash-lite`.

* LLM-as-judge evaluators could now opt into including extended stats and mapping prompt variables from `run.*` fields.

* Default sandbox rootfs images included Docker Compose and automatically started the Docker daemon.

* Added cost tracking for `gemini-3.6-flash`.

* Gateway spend cap policies could now be configured with a weekly period.

* Added Centralize as an MCP marketplace integration.

* Sandbox-enabled agents saw configured proxy profiles (hosts, injected header keys, network rules, OAuth providers) in their system prompt, replacing the older hosts-only auth-proxy section.

* Hid the Sandboxes nav entry and `/sandboxes` page in regions where `SANDBOX_FEATURE_ENABLED` was off.

* Self-hosted DockerHub images included Cosign signatures and signed SPDX SBOM attestations.

* Fixed a bug where special characters in thread ids caused the UI to be unable to query these threads.

* Fixed "Query timeout exceeded" errors when opening large traces.

* Self-hosted OIDC fixed SSO Groups Sync silently no-op'ing during login.

* Managed Deep Agents private preview supported MCP server registration with header-based auth.

* Emitted Prometheus metrics from `queue` workers.

* Clarified the stats unavailable message when text filters were applied.

* Context repos supported metadata updates and deletion from the Hub overflow menu.

* Typed responses and standard error envelope for Fleet `/v1/fleet/agents/{agent_id}/connections` (List / Create / Delete).

* Sandbox snapshots could now export a Docker image built inside a sandbox.

* Fixed ACE subprocess handling so early child-process exits returned request failures instead of crashing the service.

* Fixed large integer preservation in native run ingest payloads.

* Waterfall turn view now took full height if available.

* Organization admins could now disable Engine even when their plan auto-enabled it; their explicit choice persisted across the UI and backend gates.

* Workspace admins could now override the workspace-default weekly spend cap on a per-evaluator-rule basis from the evaluator side panel; non-admins saw the resolved cap as read-only text.

* Fixed incorrect metadata facet suggestions and improved group stats latency for projects with rich run metadata.

* Alert rules for Run Count, Errors, Latency, and Cost now supported `<`, `<=`, `>`, and `>=` comparison operators (previously the UI only allowed `>=`).

* Fleet `/v1/fleet/auth-agents/{agent_id}/connections` endpoints moved to `/v1/fleet/agents/{agent_id}/connections` with typed responses, request validation, and the standard Fleet error envelope. The old URL returned 404.

* Fixed Fleet redirect after deleting the active agent.

* Removed the Type column from the LangSmith datasets table.

* Encrypted/redacted "reasoning" content blocks no longer appeared as empty or garbled cards in the trace messages view. Meaningful extended-thinking content continued to render normally.

* Fleet agent APIs required `thread_scoped_sandbox` or `agent_scoped_sandbox` for sandbox-backed agents.

* Allowed exporting all experiments in a workspace via the new `all_experiments` parameter for bulk exports. Limited to 250 experiments per export, could be increased at request.

* No user-facing changes—internal OpenAPI spec update only.

* Fleet used langchain-fireworks 1.4.2 for Fireworks model calls.

* This enabled a redesign of the run details panel with improved readability and more robust message parsing.

* Fleet/Agent Builder included Gemini 3.5 Flash as a selectable built-in model.

* Computer use had an in-chat callout for eligible general chat users.

* Fixed a bug where the blob storage banner incorrectly flashed on page load.

* This enabled a new way to leave feedback on a run, directly within the run details panel.

* Added token pricing support for Claude Opus 4.8.

* Agent Builder offered Claude Opus 4.8 as a built-in Anthropic model.

* Organization admins could now update an existing API key's role via the service-keys API without rotating the key.

* Managed Deep Agents MCP server setup supported OAuth under the `/v1/deepagents` API namespace.

* Extra Parameters entered for Bedrock Nova 2 (and any other provider requiring camelCase API fields) now preserved their original key casing when the model configuration was saved and reloaded in the Playground.

* Self-hosted OIDC users now got a display name resolved from the `name` / `given_name`+`family_name` id\_token claims.

* Fixed an LLM gateway data-protection bug that could corrupt Anthropic images or documents when PII redaction was enabled.

* Hid sandbox file explorer controls while allowing explicit sandbox summary downloads.

* Engine supported an optional monthly LCU spend limit (set by finance, plan, or org admins) that paused new Engine runs once reached.

* Chat-input file uploads in agent builder/fleet reached the sandbox filesystem at `/tmp/uploads/` when sandboxes were enabled.

* Fleet Default appeared first in the model picker for eligible plans.

* Fixed the project stats sidebar trace count label and header layout.

* Run rules webhook payloads now included a `trace_url` deep link for each run.

* Experiment loading progress bars displayed the number of runs completed and evaluated within the experiments table.

* Sandboxes allowed password-based SSH for non-root users while keeping root SSH login key-only.

* Workspace switcher on the data-plane no-access screen only listed current organization workspaces.

* Restored cron execution for enterprise Fleet agents that had silently failed to fire since early March 2026.

* Run rules webhook payloads now included a `trace_url` deep link for each run.

* Fixed security vulnerabilities. See CVE-2026-45736, CVE-2026-44664, CVE-2025-71176 for details.

**Download the Helm chart:** [`langsmith-0.16.0-rc.12.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.16.0-rc.12/langsmith-0.16.0-rc.12.tgz)

**2026-07-09**

## langsmith-0.16.0-rc.11

* Evaluator detach confirmation dialog showed a "Detach" button instead of "Delete."

* Included extended stats became available to all organizations for code evaluators.

* Added two dedicated permissions, `bulk-exports:read` and `bulk-exports:manage`, for fetching and creating/updating bulk exports.

* Fixed the Engine "Connect GitHub" flow when the GitHub App was already installed via another workspace in the same organization.

* Bumped `@langchain/langgraph-sdk` to 1.9.4 in `smith-frontend`.

* Added an opt-in Smith-ACE v2 sandbox implementation behind `SMITH_ACE_SANDBOX_IMPLEMENTATION=v2`.

* The Threads table now showed the actual last output in the *Last Output* column and surfaced thread-level errors in a new *Last Error* column.

* Hid the \$0.00 cost badge for tool calls in the trace tree view.

* Users could now create multiple cron schedules with the same expression on the same agent.

* Agent Builder "View agent traces" and "View trace" links always opened in the fleet tracing project.

* Added LangSmith model pricing entry for `gemini-3.1-flash-lite`.

* LLM-as-judge evaluators could now opt into Include extended stats and map prompt variables from `run.*` fields.

* Default sandbox rootfs images now included Docker Compose and started the Docker daemon automatically.

* Added cost tracking for `gemini-3.6-flash`.

* Gateway spend cap policies could now be configured with a weekly period.

* Added Centralize as an MCP marketplace integration.

* Sandbox-enabled agents now saw configured proxy profiles (hosts, injected header keys, network rule, OAuth providers) in their system prompt, replacing the older hosts-only auth-proxy section.

* Hid the Sandboxes nav entry and `/sandboxes` page in regions where `SANDBOX_FEATURE_ENABLED` was off.

* Self-hosted DockerHub images now included Cosign signatures and signed SPDX SBOM attestations.

* Fixed a bug where special characters in thread IDs were not encoded, causing UI to fail to query these threads.

* Fixed "Query timeout exceeded" errors when opening large traces.

* Self-hosted OIDC fixed SSO Groups Sync silently no-op'ing during login.

* Managed Deep Agents private preview now supported MCP server registration with header-based auth.

* Emitted Prometheus metrics from `queue` workers.

* Clarified the stats unavailable message when text filters were applied.

* Context repos now supported metadata updates and deletion from the Hub overflow menu.

* Typed responses and standard error envelope for Fleet `/v1/fleet/agents/{agent_id}/connections` (List / Create / Delete).

* Sandbox snapshots could now export a Docker image built inside a sandbox.

* Fixed ACE subprocess handling so early child-process exits returned request failures instead of crashing the service.

* Fixed large integer preservation in native run ingest payloads.

* Waterfall turn view now took full height if available.

* Organization admins could now disable Engine even when their plan auto-enabled it; their explicit choice persisted across the UI and the backend gates.

* Workspace admins could now override the workspace-default weekly spend cap on a per-evaluator-rule basis from the evaluator side panel; non-admins saw the resolved cap as read-only text.

* Fixed incorrect metadata facet suggestions and improved group stats latency for projects with rich run metadata.

* Alert rules for Run Count, Errors, Latency, and Cost now supported `<`, `<=`, `>`, and `>=` comparison operators (previously the UI only allowed `>=`).

* Fleet `/v1/fleet/auth-agents/{agent_id}/connections` endpoints moved to `/v1/fleet/agents/{agent_id}/connections` with typed responses, request validation, and the standard Fleet error envelope. The old URL returned 404.

* Fixed Fleet redirect after deleting the active agent.

* Removed the Type column from the LangSmith datasets table.

* Encrypted/redacted "reasoning" content blocks no longer appeared as empty or garbled cards in the trace messages view. Meaningful extended-thinking content continued to render normally.

* Fleet agent APIs now required `thread_scoped_sandbox` or `agent_scoped_sandbox` for sandbox-backed agents.

* Allowed exporting all experiments in a workspace via the new `all_experiments` parameter for bulk exports, limited to 250 experiments per export, which could be increased upon request.

* Fleet used langchain-fireworks 1.4.2 for Fireworks model calls.

* This enabled a redesign of the run details panel with improved readability and more robust message parsing.

* Fleet/Agent Builder now included Gemini 3.5 Flash as a selectable built-in model.

* Computer use now had an in-chat callout for eligible general chat users.

* Fixed a bug where the blob storage banner incorrectly flashed on page load.

* Enabled a new way to leave feedback on a run, directly within the run details panel.

* Added token pricing support for Claude Opus 4.8.

* Agent Builder now offered Claude Opus 4.8 as a built-in Anthropic model.

* Org admins could now update an existing API key's role via the service-keys API without rotating the key.

* Managed Deep Agents MCP server setup now supported OAuth under the `/v1/deepagents` API namespace.

* Extra Parameters entered for Bedrock Nova 2 (and any other provider requiring camelCase API fields) now preserved their original key casing when the model configuration was saved and reloaded in the Playground.

* Self-hosted OIDC users now got a display name resolved from the `name` / `given_name` + `family_name` id\_token claims.

* Fixed SSRF policy for the `playground` service such that it respected `SSRF_ALLOW_K8S_INTERNAL`.

* Fixed an LLM gateway data-protection bug that could corrupt Anthropic images or documents when PII redaction was enabled.

* Hid sandbox file explorer controls while allowing explicit sandbox summary downloads.

* Engine now supported an optional monthly LCU spend limit (set by finance, plan, or org admins) that paused new Engine runs once reached.

* Chat-input file uploads in agent builder/fleet now reached the sandbox filesystem at `/tmp/uploads/` when sandboxes were enabled.

* Fleet Default now appeared first in the model picker for eligible plans.

* Fixes the project stats sidebar trace count label and header layout.

* Restored cron execution for enterprise Fleet agents that had been silently failing to fire.

* Run rules webhook payloads now included a `trace_url` deep link for each run.

* Experiment loading progress bars displayed the number of runs completed and evaluated within the experiments table.

* Sandboxes now allowed password-based SSH for non-root users while keeping root SSH login key-only.

* Fixed security vulnerabilities. See CVE-2026-45736, CVE-2026-44664, CVE-2025-71176 for details.

**Download the Helm chart:** [`langsmith-0.16.0-rc.11.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.16.0-rc.11/langsmith-0.16.0-rc.11.tgz)

**2026-07-09**

## langsmith-0.15.13

* Added support for new model integrations to enhance AI deployments in self-hosted environments.
* Improved the UI experience with streamlined features for the tracing tool, offering better insight into model performance.
* Fixed several bugs affecting user experience and UI responsiveness, leading to smoother operation.
* Enhanced performance with optimizations for faster loading speeds across various interfaces.
* Implemented new API capabilities to support extended functionality and integration options for developers.
* Incorporated security improvements with updated authentication and authorization features to better protect self-hosted instances.

**Download the Helm chart:** [`langsmith-0.15.13.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.15.13/langsmith-0.15.13.tgz)

**2026-07-08**

## langsmith-0.16.0-rc.10

* Evaluator detach confirmation dialog showed a "Detach" button instead of "Delete."

* Included extended stats were made available to all organizations for code evaluators.

* Added two dedicated permissions `bulk-exports:read` and `bulk-exports:manage` for fetching and creating/updating bulk exports.

* Fixed the Engine "Connect GitHub" flow when the GitHub App was already installed via another workspace in the same organization.

* Bumped `@langchain/langgraph-sdk` to 1.9.4 in `smith-frontend`.

* Added an opt-in Smith-ACE v2 sandbox implementation behind `SMITH_ACE_SANDBOX_IMPLEMENTATION=v2`.

* Threads table now showed the actual last output in the *Last Output* column and surfaced thread-level errors in a new *Last Error* column.

* Hid the \$0.00 cost badge for tool calls in the trace tree view.

* Users could create multiple cron schedules with the same expression on the same agent.

* Agent Builder "View agent traces" and "View trace" links always opened in the fleet tracing project.

* Added LangSmith model pricing entry for `gemini-3.1-flash-lite`.

* LLM-as-judge evaluators could opt into Include extended stats and map prompt variables from `run.*` fields.

* Default sandbox rootfs images included Docker Compose and started the Docker daemon automatically.

* Added cost tracking for `gemini-3.6-flash`.

* Gateway spend cap policies could be configured with a weekly period.

* Added Centralize as an MCP marketplace integration.

* Sandbox-enabled agents now saw configured proxy profiles (hosts, injected header keys, network rule, OAuth providers) in their system prompt, replacing the older hosts-only auth-proxy section.

* Hid the Sandboxes nav entry and `/sandboxes` page in regions where `SANDBOX_FEATURE_ENABLED` was off.

* Self-hosted DockerHub images included Cosign signatures and signed SPDX SBOM attestations.

* Fixed a bug where special characters in thread IDs were not encoding, causing the UI to be unable to query these threads.

* Fixed "Query timeout exceeded" errors when opening large traces.

* Self-hosted OIDC fixed SSO Groups Sync silently no-op'ing during login.

* Managed Deep Agents private preview supported MCP server registration with header-based auth.

* Emitted Prometheus metrics from `queue` workers.

* Clarified the stats unavailable message when text filters were applied.

* Context repos supported metadata updates and deletion from the Hub overflow menu.

* Typed responses and standard error envelope were added for Fleet `/v1/fleet/agents/{agent_id}/connections` (List / Create / Delete).

* Sandbox snapshots now could export a Docker image built inside a sandbox.

* Fixed ACE subprocess handling so early child-process exits returned request failures instead of crashing the service.

* Fixed large integer preservation in native run ingest payloads.

* Waterfall turn view took full height if available.

* Organization admins could disable Engine even when their plan auto-enabled it; their explicit choice persisted across the UI and the backend gates.

* Workspace admins could override the workspace-default weekly spend cap on a per-evaluator-rule basis from the evaluator side panel; non-admins saw the resolved cap as read-only text.

* Fixed incorrect metadata facet suggestions and improved group stats latency for projects with rich run metadata.

* Alert rules for Run Count, Errors, Latency, and Cost supported `<`, `<=`, `>`, and `>=` comparison operators (previously the UI only allowed `>=`).

* Fleet `/v1/fleet/auth-agents/{agent_id}/connections` endpoints moved to `/v1/fleet/agents/{agent_id}/connections` with typed responses, request validation, and the standard Fleet error envelope. The old URL returned 404.

* Fixed Fleet redirect after deleting the active agent.

* Removed the Type column from the LangSmith datasets table.

* Encrypted/redacted "reasoning" content blocks no longer appeared as empty or garbled cards in the trace messages view. Meaningful extended-thinking content continued to render normally.

* Fleet agent APIs required `thread_scoped_sandbox` or `agent_scoped_sandbox` for sandbox-backed agents.

* Allowed exporting all experiments in a workspace via the new `all_experiments` parameter for bulk exports. Limited to 250 experiments per export, could be increased at request.

* Fleet used langchain-fireworks 1.4.2 for Fireworks model calls.

* This enabled a redesign of the run details panel with improved readability and more robust message parsing.

* Fleet/Agent Builder included Gemini 3.5 Flash as a selectable built-in model.

* Computer use had an in-chat callout for eligible general chat users.

* Fixed a bug where the blob storage banner incorrectly flashed on page load.

* Enabled a new way to leave feedback on a run, directly within the run details panel.

* Added token pricing support for Claude Opus 4.8.

* Agent Builder offered Claude Opus 4.8 as a built-in Anthropic model.

* Org admins could update an existing API key's role via the service-keys API without rotating the key.

* Managed Deep Agents MCP server setup supported OAuth under the `/v1/deepagents` API namespace.

* Extra Parameters entered for Bedrock Nova 2 (and any other provider requiring camelCase API fields) preserved their original key casing when the model configuration was saved and reloaded in the Playground.

* Self-hosted OIDC users got a display name resolved from the `name` / `given_name`+`family_name` id\_token claims.

* Fixed SSRF policy for `playground` service such that it respected `SSRF_ALLOW_K8S_INTERNAL`.

* Fixed an LLM gateway data-protection bug that could corrupt Anthropic images or documents when PII redaction was enabled.

* Hid sandbox file explorer controls while allowing explicit sandbox summary downloads.

* Engine supported an optional monthly LCU spend limit (set by finance, plan, or org admins) that paused new Engine runs once reached.

* Chat-input file uploads in agent builder/fleet reached the sandbox filesystem at `/tmp/uploads/` when sandboxes were enabled.

* Fleet Default appeared first in the model picker for eligible plans.

* Fixed the project stats sidebar trace count label and header layout.

* Run rules webhook payloads included a `trace_url` deep link for each run.

* Experiment loading progress bars displayed the number of runs completed and evaluated within the experiments table.

* Sandboxes allowed password-based SSH for non-root users while keeping root SSH login key-only.

* Fixed security vulnerabilities. See CVE-2026-45736, CVE-2026-44664, CVE-2025-71176 for details.

**Download the Helm chart:** [`langsmith-0.16.0-rc.10.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.16.0-rc.10/langsmith-0.16.0-rc.10.tgz)

**2026-07-07**

## langsmith-0.16.0-rc.9

* This release packages the same LangSmith application version as langsmith-0.16.0-rc.8. Refer to the [langsmith-0.16.0-rc.8](#langsmith-0-16-0-rc-8) release notes below.

**Download the Helm chart:** [`langsmith-0.16.0-rc.9.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.16.0-rc.9/langsmith-0.16.0-rc.9.tgz)

**2026-07-02**

## langsmith-0.16.0-rc.8

* Evaluator detach confirmation dialog showed a "Detach" button instead of "Delete."

* Included extended stats became available to all organizations for code evaluators.

* Added two dedicated permissions `bulk-exports:read` and `bulk-exports:manage` for fetching and creating/updating bulk exports.

* Fixed the Engine "Connect GitHub" flow when the GitHub App was already installed via another workspace in the same organization.

* Bumped `@langchain/langgraph-sdk` to 1.9.4 in `smith-frontend`.

* Added an opt-in Smith-ACE v2 sandbox implementation behind `SMITH_ACE_SANDBOX_IMPLEMENTATION=v2`.

* Threads table now showed the actual last output in the *Last Output* column and surfaced thread-level errors in a new *Last Error* column.

* Hid the \$0.00 cost badge for tool calls in the trace tree view.

* Users could now create multiple cron schedules with the same expression on the same agent.

* Agent Builder "View agent traces" and "View trace" links always opened in the fleet tracing project.

* Added LangSmith model pricing entry for `gemini-3.1-flash-lite`.

* LLM-as-judge evaluators could now opt into Include extended stats and map prompt variables from `run.*` fields.

* Default sandbox rootfs images now included Docker Compose and started the Docker daemon automatically.

* Added cost tracking for `gemini-3.6-flash`.

* Gateway spend cap policies could now be configured with a weekly period.

* Added Centralize as an MCP marketplace integration.

* Sandbox-enabled agents now saw configured proxy profiles (hosts, injected header keys, network rule, OAuth providers) in their system prompt, replacing the older hosts-only auth-proxy section.

* Hid the Sandboxes nav entry and `/sandboxes` page in regions where `SANDBOX_FEATURE_ENABLED` was off.

* Self-hosted DockerHub images now included Cosign signatures and signed SPDX SBOM attestations.

* Fixed a bug where special characters in thread IDs were not encoded, causing the UI to not be able to query these threads.

* Fixed "Query timeout exceeded" errors when opening large traces.

* Self-hosted OIDC: fixed SSO Groups Sync silently no-op'ing during login.

* Managed Deep Agents private preview now supported MCP server registration with header-based auth.

* Emitted Prometheus metrics from `queue` workers.

* Clarified the stats unavailable message when text filters were applied.

* Context repos now supported metadata updates and deletion from the Hub overflow menu.

* Sandbox snapshots could now export a Docker image built inside a sandbox.

* Fixed ACE subprocess handling so early child-process exits returned request failures instead of crashing the service.

* Fixed large integer preservation in native run ingest payloads.

* Waterfall turn view now took full height if available.

* Organization admins could now disable Engine even when their plan auto-enabled it; their explicit choice persisted across the UI and the backend gates.

* Workspace admins could now override the workspace-default weekly spend cap on a per-evaluator-rule basis from the evaluator side panel; non-admins saw the resolved cap as read-only text.

* Fixed incorrect metadata facet suggestions and improved group stats latency for projects with rich run metadata.

* Alert rules for Run Count, Errors, Latency, and Cost now supported `<`, `<=`, `>`, and `>=` comparison operators (previously the UI only allowed `>=`).

* Fleet `/v1/fleet/auth-agents/{agent_id}/connections` endpoints moved to `/v1/fleet/agents/{agent_id}/connections` with typed responses, request validation, and the standard Fleet error envelope. The old URL returned 404.

* Fixed Fleet redirect after deleting the active agent.

* Removed the Type column from the LangSmith datasets table.

* Encrypted/redacted "reasoning" content blocks no longer appeared as empty or garbled cards in the trace messages view. Meaningful extended-thinking content continued to render normally.

* Fleet agent APIs now required `thread_scoped_sandbox` or `agent_scoped_sandbox` for sandbox-backed agents.

* Allowed exporting all experiments in a workspace via the new `all_experiments` parameter for bulk exports. Limited to 250 experiments per export, can be increased at request.

* No user-facing changes—internal OpenAPI spec update only.

* Fleet used langchain-fireworks 1.4.2 for Fireworks model calls.

* This enabled a redesign of the run details panel with improved readability and more robust message parsing.

* Fleet/Agent Builder now included Gemini 3.5 Flash as a selectable built-in model.

* Computer use now had an in-chat callout for eligible general chat users.

* Fixed a bug where the blob storage banner incorrectly flashed on page load.

* This enabled a new way to leave feedback on a run, directly within the run details panel.

* Added token pricing support for Claude Opus 4.8.

* Agent Builder now offered Claude Opus 4.8 as a built-in Anthropic model.

* Org admins could now update an existing API key's role via the service-keys API without rotating the key.

* Managed Deep Agents MCP server setup now supported OAuth under the `/v1/deepagents` API namespace.

* Extra Parameters entered for Bedrock Nova 2 (and any other provider requiring camelCase API fields) now preserved their original key casing when the model configuration was saved and reloaded in the Playground.

* Self-hosted OIDC users now got a display name resolved from the `name` / `given_name`+`family_name` id\_token claims.

* Fixed SSRF policy for `playground` service such that it respected `SSRF_ALLOW_K8S_INTERNAL`.

* Fixed an LLM gateway data-protection bug that could corrupt Anthropic images or documents when PII redaction was enabled.

* Hid sandbox file explorer controls while allowing explicit sandbox summary downloads.

* Engine now supported an optional monthly LCU spend limit (set by finance, plan, or org admins) that paused new Engine runs once reached.

* Chat-input file uploads in agent builder/fleet now reached the sandbox filesystem at `/tmp/uploads/` when sandboxes were enabled.

* Fleet Default now appeared first in the model picker for eligible plans.

* Fixed the project stats sidebar trace count label and header layout.

* Workspace switcher on the data-plane no-access screen only listed current organization workspaces.

* Restored cron execution for enterprise Fleet agents that had been silently failing to fire since early March 2026.

* Run rules webhook payloads now included a `trace_url` deep link for each run.

* Experiment loading progress bars displayed the number of runs completed and evaluated within the experiments table.

* Sandboxes now allowed password-based SSH for non-root users while keeping root SSH login key-only.

* Fixed security vulnerabilities. See CVE-2026-45736, CVE-2026-44664, CVE-2025-71176 for details.

**Download the Helm chart:** [`langsmith-0.16.0-rc.8.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.16.0-rc.8/langsmith-0.16.0-rc.8.tgz)

**2026-07-01**

## langsmith-0.16.0-rc.7

* Patched dependencies.

* Confirmed CI green :pray:.

* Evaluator detach confirmation dialog showed a "Detach" button instead of "Delete."

* Included extended stats were made available to all organizations for code evaluators.

* Added two dedicated permissions `bulk-exports:read` and `bulk-exports:manage` for fetching and creating/updating bulk exports.

* Fixed the Engine "Connect GitHub" flow when the GitHub App was already installed via another workspace in the same organization.

* Bumped `@langchain/langgraph-sdk` to 1.9.4 in the `smith-frontend`.

* Added an opt-in Smith-ACE v2 sandbox implementation behind `SMITH_ACE_SANDBOX_IMPLEMENTATION=v2`.

* Threads table showed the actual last output in the *Last Output* column and surfaced thread-level errors in a new *Last Error* column.

* Hid the \$0.00 cost badge for tool calls in the trace tree view.

* Users could now create multiple cron schedules with the same expression on the same agent.

* Agent Builder "View agent traces" and "View trace" links always opened in the fleet tracing project.

* Added LangSmith model pricing entry for `gemini-3.1-flash-lite`.

* LLM-as-judge evaluators could now opt into Include extended stats and map prompt variables from `run.*` fields.

* Default sandbox rootfs images included Docker Compose and started the Docker daemon automatically.

* Added cost tracking for `gemini-3.6-flash`.

* Gateway spend cap policies could now be configured with a weekly period.

* Added Centralize as an MCP marketplace integration.

* Sandbox-enabled agents now saw configured proxy profiles (hosts, injected header keys, network rule, OAuth providers) in their system prompt, replacing the older hosts-only auth-proxy section.

* Hid the Sandboxes nav entry and `/sandboxes` page in regions where `SANDBOX_FEATURE_ENABLED` was off.

* Self-hosted DockerHub images included Cosign signatures and signed SPDX SBOM attestations.

* Fixed a bug where special characters were not encoded in thread IDs, causing the UI to be unable to query these threads.

* Fixed "Query timeout exceeded" errors when opening large traces.

* Self-hosted OIDC: fixed SSO Groups Sync that silently no-op'ed during login.

* Managed Deep Agents private preview supported MCP server registration with header-based auth.

* Emitted Prometheus metrics from `queue` workers.

* Clarified the stats unavailable message when text filters are applied.

* Context repos now supported metadata updates and deletion from the Hub overflow menu.

* Typed responses and standard error envelope for Fleet `/v1/fleet/agents/{agent_id}/connections` (List/Create/Delete).

* Sandbox snapshots could now export a Docker image built inside a sandbox.

* Fixed ACE subprocess handling so early child-process exits returned request failures instead of crashing the service.

* Fixed large integer preservation in native run ingest payloads.

* Waterfall turn view took full height if available.

* Organization admins could now disable Engine even when their plan auto-enables it; their explicit choice persisted across the UI and the backend gates.

* Workspace admins could now override the workspace-default weekly spend cap on a per-evaluator-rule basis from the evaluator side panel; non-admins saw the resolved cap as read-only text.

* Fixed incorrect metadata facet suggestions and improved group stats latency for projects with rich run metadata.

* Alert rules for Run Count, Errors, Latency, and Cost now supported `<`, `<=`, `>`, and `>=` comparison operators (previously the UI only allowed `>=`).

* Fleet agent APIs required `thread_scoped_sandbox` or `agent_scoped_sandbox` for sandbox-backed agents.

* Allowed exporting all experiments in a workspace via the new `all_experiments` parameter for bulk exports; limited to 250 experiments per export, can be increased at request.

* Fleet used `langchain-fireworks 1.4.2` for Fireworks model calls.

* Enabled a redesign of the run details panel with improved readability and more robust message parsing.

* Fleet/Agent Builder included Gemini 3.5 Flash as a selectable built-in model.

* Computer use had an in-chat callout for eligible general chat users.

* Fixed a bug where the blob storage banner incorrectly flashed on page load.

* Enabled a new way to leave feedback on a run, directly within the run details panel.

* Added token pricing support for Claude Opus 4.8.

* Agent Builder offered Claude Opus 4.8 as a built-in Anthropic model.

* Organization admins could now update an existing API key's role via the service-keys API without rotating the key.

* Managed Deep Agents MCP server setup supported OAuth under the `/v1/deepagents` API namespace.

* Extra Parameters entered for Bedrock Nova 2 and other providers requiring camelCase API fields preserved their original key casing when the model configuration was saved and reloaded in the Playground.

* Self-hosted OIDC users received a display name resolved from the `name` / `given_name`+`family_name` id\_token claims.

* Fixed SSRF policy for `playground` service to respect `SSRF_ALLOW_K8S_INTERNAL`.

* Fixed an LLM gateway data-protection bug that could corrupt Anthropic images or documents when PII redaction was enabled.

* Hid sandbox file explorer controls while allowing explicit sandbox summary downloads.

* Engine supported an optional monthly LCU spend limit (set by finance, plan, or org admins) that paused new Engine runs once reached.

* Chat-input file uploads in agent builder/fleet reached the sandbox filesystem at `/tmp/uploads/` when sandboxes were enabled.

* Fleet Default appeared first in the model picker for eligible plans.

* Fixed the project stats sidebar trace count label and header layout.

* Workspace switcher on the data-plane no-access screen only listed current organization workspaces.

* Restored cron execution for enterprise Fleet agents that had been silently failing to fire since early March 2026.

* Run rules webhook payloads included a `trace_url` deep link for each run.

* Experiment loading progress bars showed the number of runs completed and evaluated within the experiments table.

* Sandboxes allowed password-based SSH for non-root users while keeping root SSH login key-only.

* Fixed security vulnerabilities. See CVE-2026-45736, CVE-2026-44664, CVE-2025-71176 for details.

**Download the Helm chart:** [`langsmith-0.16.0-rc.7.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.16.0-rc.7/langsmith-0.16.0-rc.7.tgz)

**2026-06-26**

## langsmith-0.16.0-rc.6

* Evaluator detach confirmation dialog showed a "Detach" button instead of "Delete."

* "Include extended stats" was made available to all organizations for code evaluators.

* Added two dedicated permissions, `bulk-exports:read` and `bulk-exports:manage`, for fetching and creating/updating bulk exports.

* Fixed the Engine "Connect GitHub" flow when the GitHub App was already installed via another workspace in the same organization.

* Added an opt-in Smith-ACE v2 sandbox implementation behind `SMITH_ACE_SANDBOX_IMPLEMENTATION=v2`.

* Threads table now showed the actual last output in the *Last Output* column and surfaced thread-level errors in the new *Last Error* column.

* Hid the \$0.00 cost badge for tool calls in the trace tree view.

* Users could now create multiple cron schedules with the same expression on the same agent.

* Agent Builder's "View agent traces" and "View trace" links always opened in the fleet tracing project.

* Added LangSmith model pricing entry for `gemini-3.1-flash-lite`.

* LLM-as-judge evaluators could now opt into "Include extended stats" and map prompt variables from `run.*` fields.

* Default sandbox rootfs images now included Docker Compose and started the Docker daemon automatically.

* Added cost tracking for `gemini-3.6-flash`.

* Gateway spend cap policies could now be configured with a weekly period.

* Added Centralize as an MCP marketplace integration.

* Sandbox-enabled agents now saw configured proxy profiles (hosts, injected header keys, network rules, OAuth providers) in their system prompt, replacing the older hosts-only auth-proxy section.

* Hid the Sandboxes nav entry and `/sandboxes` page in regions where `SANDBOX_FEATURE_ENABLED` was off.

* Self-hosted DockerHub images now included Cosign signatures and signed SPDX SBOM attestations.

* Fixed a bug where special characters in thread IDs were not encoded, causing the UI to fail to query these threads.

* Fixed "Query timeout exceeded" errors when opening large traces.

* Self-hosted OIDC: fixed SSO Groups Sync silently no-op'ing during login.

* Managed Deep Agents private preview now supported MCP server registration with header-based auth.

* Emitted Prometheus metrics from `queue` workers.

* Clarified the stats unavailable message when text filters were applied.

* Typed responses and standard error envelope were added for Fleet `/v1/fleet/agents/{agent_id}/connections` (List / Create / Delete).

* Sandbox snapshots could now export a Docker image built inside a sandbox.

* Fixed ACE subprocess handling so early child-process exits returned request failures instead of crashing the service.

* Fixed large integer preservation in native run ingest payloads.

* Waterfall turn view now took full height if available.

* Organization admins could now disable Engine even when their plan auto-enabled it; their explicit choice persisted across the UI and the backend gates.

* Workspace admins could now override the workspace-default weekly spend cap on a per-evaluator-rule basis from the evaluator side panel; non-admins saw the resolved cap as read-only text.

* Fixed incorrect metadata facet suggestions and improved group stats latency for projects with rich run metadata.

* Alert rules for Run Count, Errors, Latency, and Cost now supported `<`, `<=`, `>`, and `>=` comparison operators (previously the UI only allowed `>=`).

* Fleet agent APIs now required `thread_scoped_sandbox` or `agent_scoped_sandbox` for sandbox-backed agents.

* Allowed exporting all experiments in a workspace via the new `all_experiments` parameter for bulk exports (limited to 250 experiments per export, with an option to increase upon request).

* Redesigned the run details panel with improved readability and more robust message parsing.

* Fleet/Agent Builder now included Gemini 3.5 Flash as a selectable built-in model.

* Computer use now had an in-chat callout for eligible general chat users.

* Fixed a bug where the blob storage banner incorrectly flashed on page load.

* Added a way to leave feedback on a run directly within the run details panel.

* Added token pricing support for Claude Opus 4.8.

* Agent Builder now offered Claude Opus 4.8 as a built-in Anthropic model.

* Org admins could now update an existing API key's role via the service-keys API without rotating the key.

* Managed Deep Agents MCP server setup now supported OAuth under the `/v1/deepagents` API namespace.

* Extra parameters entered for Bedrock Nova 2 (and any other provider requiring camelCase API fields) now preserved their original key casing when the model configuration was saved and reloaded in the Playground.

* Self-hosted OIDC users now got a display name resolved from the `name` / `given_name` + `family_name` id\_token claims.

* Fixed SSRF policy for `playground` service such that it respected `SSRF_ALLOW_K8S_INTERNAL`.

* Fixed an LLM gateway data-protection bug that could corrupt Anthropic images or documents when PII redaction was enabled.

* Hid sandbox file explorer controls while allowing explicit sandbox summary downloads.

* Engine now supported an optional monthly LCU spend limit (set by finance, plan, or org admins) that paused new Engine runs once reached.

* Chat-input file uploads in agent builder/fleet now reached the sandbox filesystem at `/tmp/uploads/` when sandboxes were enabled.

* Fleet Default now appeared first in the model picker for eligible plans.

* Fixed the project stats sidebar trace count label and header layout.

* Run rules webhook payloads now included a `trace_url` deep link for each run.

* Experiment loading progress bars displayed the number of runs completed and evaluated within the experiments table.

* Sandboxes now allowed password-based SSH for non-root users while keeping root SSH login key-only.

* Fixed security vulnerabilities. See CVE-2026-45736, CVE-2026-44664, CVE-2025-71176 for details.

**Download the Helm chart:** [`langsmith-0.16.0-rc.6.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.16.0-rc.6/langsmith-0.16.0-rc.6.tgz)

**2026-06-24**

## langsmith-0.15.12

* Patched dependencies.

**Download the Helm chart:** [`langsmith-0.15.12.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.15.12/langsmith-0.15.12.tgz)

**2026-06-24**

## langsmith-0.16.0-rc.5

* This release packages the same LangSmith application version as langsmith-0.16.0-rc.4. Refer to the [langsmith-0.16.0-rc.4](#langsmith-0-16-0-rc-4) release notes below.

**Download the Helm chart:** [`langsmith-0.16.0-rc.5.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.16.0-rc.5/langsmith-0.16.0-rc.5.tgz)

**2026-06-18**

## langsmith-0.16.0-rc.4

* Evaluator detach confirmation dialog showed a "Detach" button instead of "Delete".

* "Include extended stats" was made available to all organizations for code evaluators.

* Added two dedicated permissions `bulk-exports:read` and `bulk-exports:manage` for fetching and creating/updating bulk exports.

* Fixed the Engine "Connect GitHub" flow when the GitHub App was already installed via another workspace in the same organization.

* Bumped `@langchain/langgraph-sdk` to 1.9.4 in `smith-frontend`.

* Added an opt-in Smith-ACE v2 sandbox implementation behind `SMITH_ACE_SANDBOX_IMPLEMENTATION=v2`.

* Threads table now showed the actual last output in the *Last Output* column and surfaced thread-level errors in a new *Last Error* column.

* Hid the \$0.00 cost badge for tool calls in the trace tree view.

* Users could now create multiple cron schedules with the same expression on the same agent.

* Agent Builder's "View agent traces" and "View trace" links always opened in the fleet tracing project.

* Added LangSmith model pricing entry for `gemini-3.1-flash-lite`.

* LLM-as-judge evaluators could now opt into "Include extended stats" and map prompt variables from `run.*` fields.

* Default sandbox rootfs images now included Docker Compose and started the Docker daemon automatically.

* Added cost tracking for `gemini-3.6-flash`.

* Gateway spend cap policies could now be configured with a weekly period.

* Added Centralize as an MCP marketplace integration.

* Sandbox-enabled agents now saw configured proxy profiles (hosts, injected header keys, network rules, OAuth providers) in their system prompt, replacing the older hosts-only auth-proxy section.

* Hid the Sandboxes nav entry and `/sandboxes` page in regions where `SANDBOX_FEATURE_ENABLED` was off.

* Self-hosted DockerHub images now included Cosign signatures and signed SPDX SBOM attestations.

* Fixed a bug where special characters in thread IDs were not encoded, causing the UI to be unable to query these threads.

* Fixed "Query timeout exceeded" errors when opening large traces.

* Self-hosted OIDC: fixed SSO Groups Sync silently no-op'ing during login.

* Managed Deep Agents private preview now supported MCP server registration with header-based auth.

* Emitted Prometheus metrics from `queue` workers.

* Clarified the stats unavailable message when text filters were applied.

* Context repos now supported metadata updates and deletion from the Hub overflow menu.

* Added token pricing support for Claude Opus 4.8.

* Agent Builder now offered Claude Opus 4.8 as a built-in Anthropic model.

* Org admins could now update an existing API key's role via the service-keys API without rotating the key.

* Managed Deep Agents MCP server setup now supported OAuth under the `/v1/deepagents` API namespace.

* Extra Parameters entered for Bedrock Nova 2 (and any other provider requiring camelCase API fields) now preserved their original key casing when the model configuration was saved and reloaded in the Playground.

* Self-hosted OIDC users now got a display name resolved from the `name` / `given_name`+`family_name` id\_token claims.

* Fixed SSRF policy for `playground` service such that it respected `SSRF_ALLOW_K8S_INTERNAL`.

* Fixed an LLM gateway data-protection bug that could corrupt Anthropic images or documents when PII redaction was enabled.

* Hid sandbox file explorer controls while allowing explicit sandbox summary downloads.

* Engine now supported an optional monthly LCU spend limit (set by finance, plan, or org admins) that paused new Engine runs once reached.

* Chat-input file uploads in agent builder/fleet now reached the sandbox filesystem at `/tmp/uploads/` when sandboxes were enabled.

* Fleet Default now appeared first in the model picker for eligible plans.

* Fixed the project stats sidebar trace count label and header layout.

* Workspace switcher on the data-plane no-access screen only listed current organization workspaces.

* Restored cron execution for enterprise Fleet agents that had been silently failing to fire since early March 2026.

* Run rules webhook payloads now included a `trace_url` deep link for each run.

* Experiment loading progress bars displayed the number of runs completed and evaluated within the experiments table.

* Sandboxes now allowed password-based SSH for non-root users while keeping root SSH login key-only.

* Fixed security vulnerabilities. See CVE-2026-45736, CVE-2026-44664, CVE-2025-71176 for details.

**Download the Helm chart:** [`langsmith-0.16.0-rc.4.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.16.0-rc.4/langsmith-0.16.0-rc.4.tgz)

**2026-06-18**

## langsmith-0.15.11

* Improved the UI for tracing to enhance the user experience.
* Fixed a bug that affected playground performance.
* Added support for mTLS in self-hosted infrastructure.
* Added Redis Cluster compatibility for better scalability.
* Implemented PostgreSQL IAM support to enhance database security.
* Enhanced streaming performance to reduce load times.
* Added new API endpoints to expand developer capabilities.
* Improved the Agent Builder interface for more intuitive usage.
* Updated authentication features to increase security in self-hosted deployments.

**Download the Helm chart:** [`langsmith-0.15.11.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.15.11/langsmith-0.15.11.tgz)

**2026-06-15**

## langsmith-0.16.0-rc.3

* Evaluator detach confirmation dialog showed a "Detach" button instead of "Delete."

* Included extended stats were made available to all organizations for code evaluators.

* Added two dedicated permissions `bulk-exports:read` and `bulk-exports:manage` for fetching and creating/updating bulk exports.

* Fixed the Engine "Connect GitHub" flow when the GitHub App was already installed via another workspace in the same organization.

* Bumped `@langchain/langgraph-sdk` to 1.9.4 in `smith-frontend`.

* Added an opt-in Smith-ACE v2 sandbox implementation behind `SMITH_ACE_SANDBOX_IMPLEMENTATION=v2`.

* Threads table now showed the actual last output in the *Last Output* column and surfaced thread-level errors in a new *Last Error* column.

* Hid the \$0.00 cost badge for tool calls in the trace tree view.

* Users can now create multiple cron schedules with the same expression on the same agent.

* Agent Builder "View agent traces" and "View trace" links now always open in the fleet tracing project.

* Added LangSmith model pricing entry for `gemini-3.1-flash-lite`.

* LLM-as-judge evaluators could now opt into Include extended stats and map prompt variables from `run.*` fields.

* Default sandbox rootfs images now included Docker Compose and started the Docker daemon automatically.

* Added cost tracking for `gemini-3.6-flash`.

* Gateway spend cap policies could now be configured with a weekly period.

* Added Centralize as an MCP marketplace integration.

* Sandbox-enabled agents now see configured proxy profiles (hosts, injected header keys, network rule, OAuth providers) in their system prompt, replacing the older hosts-only auth-proxy section.

* Hid the Sandboxes nav entry and `/sandboxes` page in regions where `SANDBOX_FEATURE_ENABLED` is off.

* Self-hosted DockerHub images now included Cosign signatures and signed SPDX SBOM attestations.

* Fixed a bug where special characters in thread IDs were not encoded, causing the UI to not be able to query these threads.

* Fixed "Query timeout exceeded" errors when opening large traces.

* Self-hosted OIDC: fixed SSO Groups Sync silently no-op'ing during login.

* Managed Deep Agents private preview now supports MCP server registration with header-based authentication.

* Emitted Prometheus metrics from `queue` workers.

* Clarified the stats unavailable message when text filters are applied.

* Context repos now supported metadata updates and deletion from the Hub overflow menu.

* Typed responses and standard error envelope for Fleet `/v1/fleet/agents/{agent_id}/connections` (List / Create / Delete) endpoints.

* Sandbox snapshots could now export a Docker image built inside a sandbox.

* Fixed ACE subprocess handling so early child-process exits returned request failures instead of crashing the service.

* Fixed large integer preservation in native run ingest payloads.

* Waterfall turn view now takes full height if available.

* Organization admins could now disable Engine even when their plan auto-enables it; their explicit choice persisted across the UI and backend gates.

* Workspace admins could override the workspace-default weekly spend cap on a per-evaluator-rule basis from the evaluator side panel, while non-admins saw the resolved cap as read-only text.

* Fixed incorrect metadata facet suggestions and improved group stats latency for projects with rich run metadata.

* Alert rules for Run Count, Errors, Latency, and Cost now supported `<`, `<=`, `>`, and `>=` comparison operators (previously the UI only allowed `>=`).

* Fleet `/v1/fleet/auth-agents/{agent_id}/connections` endpoints moved to `/v1/fleet/agents/{agent_id}/connections` with typed responses, request validation, and the standard Fleet error envelope; the old URL returned 404.

* Fixed Fleet redirect after deleting the active agent.

* Removed the Type column from the LangSmith datasets table.

* Encrypted/redacted "reasoning" content blocks no longer appeared as empty or garbled cards in the trace messages view; meaningful extended-thinking content continued to render normally.

* Fleet agent APIs now required `thread_scoped_sandbox` or `agent_scoped_sandbox` for sandbox-backed agents.

* Allowed exporting all experiments in a workspace via the new `all_experiments` parameter for bulk exports, limited to 250 experiments per export, with potential for increase upon request.

* Fleet used langchain-fireworks 1.4.2 for Fireworks model calls.

* This enabled a redesign of the run details panel with improved readability and more robust message parsing.

* Fleet/Agent Builder now included Gemini 3.5 Flash as a selectable built-in model.

* Computer use now had an in-chat callout for eligible general chat users.

* Fixed a bug where the blob storage banner incorrectly flashed on page load.

* This enabled a new way to leave feedback on a run, directly within the run details panel.

* Added token pricing support for Claude Opus 4.8.

* Agent Builder now offered Claude Opus 4.8 as a built-in Anthropic model.

* Org admins could now update an existing API key's role via the service-keys API without rotating the key.

* Managed Deep Agents MCP server setup now supported OAuth under the `/v1/deepagents` API namespace.

* Extra Parameters entered for Bedrock Nova 2 (and any other provider requiring camelCase API fields) now preserved their original key casing when the model configuration was saved and reloaded in the Playground.

* Self-hosted OIDC users now got a display name resolved from the `name` / `given_name`+`family_name` id\_token claims.

* Fixed the SSRF policy for the `playground` service so that it respected `SSRF_ALLOW_K8S_INTERNAL`.

* Fixed an LLM gateway data-protection bug that could corrupt Anthropic images or documents when PII redaction was enabled.

* Hid sandbox file explorer controls while allowing explicit sandbox summary downloads.

* Engine now supported an optional monthly LCU spend limit (set by finance, plan, or org admins) that paused new Engine runs once reached.

* Chat input file uploads in agent builder/fleet now reached the sandbox filesystem at `/tmp/uploads/` when sandboxes were enabled.

* Fleet Default now appeared first in the model picker for eligible plans.

* Fixed the project stats sidebar trace count label and header layout.

* Workspace switcher on the data-plane no-access screen only listed current organization workspaces.

* Restored cron execution for enterprise Fleet agents that had been silently failing to fire since early March 2026.

* Run rules webhook payloads now included a `trace_url` deep link for each run.

* Experiment loading progress bars now displayed the number of runs completed and evaluated within the experiments table.

* Sandboxes now allowed password-based SSH for non-root users while keeping root SSH login key-only.

* Fixed security vulnerabilities. See CVE-2026-45736, CVE-2026-44664, CVE-2025-71176 for details.

**Download the Helm chart:** [`langsmith-0.16.0-rc.3.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.16.0-rc.3/langsmith-0.16.0-rc.3.tgz)

**2026-06-11**

## langsmith-0.16.0-rc.2

* For the full list of changes in the 0.16.0 release candidate, refer to the [langsmith-0.16.0-rc.1](#langsmith-0-16-0-rc-1) release notes below.

**Download the Helm chart:** [`langsmith-0.16.0-rc.2.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.16.0-rc.2/langsmith-0.16.0-rc.2.tgz)

**2026-06-11**

## langsmith-0.15.10

* Patched dependencies.

* Fixed security vulnerabilities. See CVE-2026-25087, CVE-2026-45134, CVE-2026-9256 for details.

**Download the Helm chart:** [`langsmith-0.15.10.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.15.10/langsmith-0.15.10.tgz)

**2026-06-09**

## langsmith-0.16.0-rc.1

* Evaluator detach confirmation dialog showed a "Detach" button instead of "Delete."

* Included extended stats became available to all organizations for code evaluators.

* Added two dedicated permissions `bulk-exports:read` and `bulk-exports:manage` for fetching and creating/updating bulk exports.

* Fixed the Engine "Connect GitHub" flow when the GitHub app was already installed via another workspace in the same organization.

* Bumped `@langchain/langgraph-sdk` to 1.9.4 in `smith-frontend`.

* Added an opt-in Smith-ACE v2 sandbox implementation behind `SMITH_ACE_SANDBOX_IMPLEMENTATION=v2`.

* Threads table now showed the actual last output in the *Last Output* column and surfaced thread-level errors in a new *Last Error* column.

* Hid the \$0.00 cost badge for tool calls in the trace tree view.

* Similar cron schedules on the same agent could now be created multiple times with the same expression.

* Agent Builder "View agent traces" and "View trace" links always opened in the fleet tracing project.

* Added LangSmith model pricing entry for `gemini-3.1-flash-lite`.

* LLM-as-judge evaluators could now opt into include extended stats and map prompt variables from `run.*` fields.

* Default sandbox rootfs images now included Docker Compose and started the Docker daemon automatically.

* Added cost tracking for `gemini-3.6-flash`.

* Gateway spend cap policies could now be configured with a weekly period.

* Added Centralize as an MCP marketplace integration.

* Sandbox-enabled agents now saw configured proxy profiles (hosts, injected header keys, network rule, OAuth providers) in their system prompt, replacing the older hosts-only auth-proxy section.

* Hid the Sandboxes nav entry and `/sandboxes` page in regions where `SANDBOX_FEATURE_ENABLED` was off.

* Self-hosted DockerHub images now included Cosign signatures and signed SPDX SBOM attestations.

* Fixed a bug where special characters in thread IDs were not encoded, causing the UI to not be able to query these threads.

* Fixed "Query timeout exceeded" errors when opening large traces.

* Self-hosted OIDC: fixed SSO groups sync silently no-op'ing during login.

* Managed Deep Agents private preview now supported MCP server registration with header-based auth.

* Emitted Prometheus metrics from `queue` workers.

* Clarified the "Stats unavailable" message when text filters were applied.

* Context repos now supported metadata updates and deletion from the Hub overflow menu.

* Typed responses and standard error envelope for Fleet `/v1/fleet/agents/{agent_id}/connections` (List / Create / Delete).

* Sandbox snapshots could now export a Docker image built inside a sandbox.

* Fixed ACE subprocess handling so early child-process exits returned request failures instead of crashing the service.

* Fixed large integer preservation in native run ingest payloads.

* Waterfall turn view now took full height if available.

* Organization admins could now disable Engine even when their plan auto-enabled it; their explicit choice persisted across the UI and the backend gates.

* Workspace admins could now override the workspace-default weekly spend cap on a per-evaluator-rule basis from the evaluator side panel; non-admins saw the resolved cap as read-only text.

* Fixed incorrect metadata facet suggestions and improved group stats latency for projects with rich run metadata.

* Alert rules for Run Count, Errors, Latency, and Cost now supported `<`, `<=`, `>`, and `>=` comparison operators (previously the UI only allowed `>=`).

* Fleet `/v1/fleet/auth-agents/{agent_id}/connections` endpoints moved to `/v1/fleet/agents/{agent_id}/connections` with typed responses, request validation, and the standard Fleet error envelope. The old URL returned 404.

* Fixed Fleet redirect after deleting the active agent.

* Removed the Type column from the LangSmith datasets table.

* Encrypted/redacted "reasoning" content blocks no longer appeared as empty or garbled cards in the trace messages view. Meaningful extended-thinking content continued to render normally.

* Fleet agent APIs now required `thread_scoped_sandbox` or `agent_scoped_sandbox` for sandbox-backed agents.

* Allowed exporting all experiments in a workspace via the new `all_experiments` parameter for bulk exports. Limited to 250 experiments per export, could be increased at request.

* Fleet uses langchain-fireworks 1.4.2 for Fireworks model calls.

* This enabled a redesign of the run details panel with improved readability and more robust message parsing.

* Fleet/Agent Builder now included Gemini 3.5 Flash as a selectable built-in model.

* Computer use now had an in-chat callout for eligible general chat users.

* Fixed a bug where the blob storage banner incorrectly flashed on page load.

* This enabled a new way to leave feedback on a run, directly within the run details panel.

* Added token pricing support for Claude Opus 4.8.

* Agent Builder now offered Claude Opus 4.8 as a built-in Anthropic model.

* Org admins could now update an existing API key's role via the service-keys API without rotating the key.

* Managed Deep Agents MCP server setup now supported OAuth under the `/v1/deepagents` API namespace.

* Extra Parameters entered for Bedrock Nova 2 (and any other provider requiring camelCase API fields) now preserved their original key casing when the model configuration was saved and reloaded in the Playground.

* Self-hosted OIDC users now got a display name resolved from the `name` / `given_name`+`family_name` id\_token claims.

* Fixed SSRF policy for `playground` service such that it respected `SSRF_ALLOW_K8S_INTERNAL`.

* Fixed an LLM gateway data-protection bug that could corrupt Anthropic images or documents when PII redaction was enabled.

* Hid sandbox file explorer controls while allowing explicit sandbox summary downloads.

* Engine now supported an optional monthly LCU spend limit (set by finance, plan, or org admins) that paused new Engine runs once reached.

* Chat-input file uploads in agent builder/fleet now reached the sandbox filesystem at `/tmp/uploads/` when sandboxes were enabled.

* Fleet Default now appeared first in the model picker for eligible plans.

* Fixes the project stats sidebar trace count label and header layout.

* Run rules webhook payloads now included a `trace_url` deep link for each run.

* Experiment loading progress bars displayed the number of runs completed and evaluated within the experiments table.

* Sandboxes now allowed password-based SSH for non-root users while keeping root SSH login key-only.

* Workspace switcher on the data-plane no-access screen only listed current organization workspaces.

* Restored cron execution for enterprise Fleet agents that had been silently failing to fire since early March 2026.

* Fixed security vulnerabilities. See CVE-2026-45736, CVE-2026-44664, CVE-2025-71176 for details.

**Download the Helm chart:** [`langsmith-0.16.0-rc.1.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.16.0-rc.1/langsmith-0.16.0-rc.1.tgz)

**2026-06-09**

## langsmith-0.15.9

* This release packages the same LangSmith application version as langsmith-0.15.7. Refer to the [langsmith-0.15.7](#langsmith-0-15-7) release notes below.

**Download the Helm chart:** [`langsmith-0.15.9.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.15.9/langsmith-0.15.9.tgz)

**2026-06-08**

## langsmith-0.15.8

* This release packages the same LangSmith application version as langsmith-0.15.7. Refer to the [langsmith-0.15.7](#langsmith-0-15-7) release notes below.

**Download the Helm chart:** [`langsmith-0.15.8.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.15.8/langsmith-0.15.8.tgz)

**2026-06-06**

## langsmith-0.15.7

* Added support for API key authentication with Amazon Bedrock in the Playground. Bedrock API keys let you authenticate requests with a bearer token instead of AWS credentials.
* Fixed the LLM auth proxy for two cases: evaluator batch requests and Bedrock model configurations.

**Download the Helm chart:** [`langsmith-0.15.7.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.15.7/langsmith-0.15.7.tgz)

**2026-06-03**

## langsmith-0.15.6

* Fixed a bug in SSO Groups Sync where the group-name separator was ignored and did not behave like SCIM sync.
* Added structured server logs identifying which workspace group claims resolved and which did not, simplifying SSO Groups Sync diagnosis.
* Patched dependencies.

**Download the Helm chart:** [`langsmith-0.15.6.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.15.6/langsmith-0.15.6.tgz)

**2026-06-02**

## langsmith-0.15.5

* Fixed the SSRF policy for the `playground` service so that it respected `SSRF_ALLOW_K8S_INTERNAL`.
* Patched dependencies.
* Fixed security vulnerabilities. See CVE-2026-45736, CVE-2026-44664 for details.

**Download the Helm chart:** [`langsmith-0.15.5.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.15.5/langsmith-0.15.5.tgz)

**2026-06-01**

## langsmith-0.15.4

* This release packages the same LangSmith application version as langsmith-0.15.2. Refer to the [langsmith-0.15.2](#langsmith-0-15-2) release notes below.

**Download the Helm chart:** [`langsmith-0.15.4.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.15.4/langsmith-0.15.4.tgz)

**2026-05-29**

## langsmith-0.15.3

* This release packages the same LangSmith application version as langsmith-0.15.2. Refer to the [langsmith-0.15.2](#langsmith-0-15-2) release notes below.

**Download the Helm chart:** [`langsmith-0.15.3.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.15.3/langsmith-0.15.3.tgz)

**2026-05-29**

## langsmith-0.15.2

* Fixed an OIDC login redirect loop (`ERR_TOO_MANY_REDIRECTS`) for identity providers that use the hybrid flow with a `form_post` callback.

**Download the Helm chart:** [`langsmith-0.15.2.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.15.2/langsmith-0.15.2.tgz)

**2026-05-29**

## langsmith-0.15.1

* Fixed a bug where the blob storage banner incorrectly flashed on page load.
* Fixed an issue in self-hosted OIDC (v15) where the SSO Groups Sync silently no-op'ed during login.

**Download the Helm chart:** [`langsmith-0.15.1.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.15.1/langsmith-0.15.1.tgz)

**2026-05-26**

## langsmith-0.15.0

LangSmith Self-Hosted v0.15 brings **reusable evaluators and a library of 30+ evaluator templates** that centralize evaluation across your workspace, ships **per-example assertions** alongside reference outputs in annotation queues, lets you download **Insights reports** as PDFs for offline analysis, and introduces the **Context Hub** for version-controlled, environment-aware management of agent instructions and tools. Several breaking changes are worth reviewing before upgrade: the `agent-bootstrap` script is deprecated, the Agent Builder rename to [Fleet](../../../Additional%20documentation/No-code%20agents%20with%20LangSmith%20Fleet.md) may require workload-identity service-account updates, and the `projects:update-retention` permission splits into `projects:increase-trace-tier` and `projects:decrease-trace-tier`.

Follow the [upgrade instructions](../Manage%20an%20instance/Upgrade%20an%20installation.md) to get access to everything. To book time with LangChain support for your upgrade, contact the team via the [Support Portal](https://support.langchain.com).

### Breaking changes

* Deprecated the `agent-bootstrap` script. LangSmith agents are now standalone services that deploy with the Helm chart instead of through the LangSmith Deployment control plane. If you were using [Fleet](../../../Additional%20documentation/No-code%20agents%20with%20LangSmith%20Fleet.md) through this script previously, this may require a migration. See the [Fleet rename and migration guide](https://kb.langchain.com/articles/9482666900-upgrading-self-hosted-langsmith-to-v0-15-fleet-rename-and-migration-guide) or contact support to walk through migration.
* Renamed Agent Builder to [Fleet](../../../Additional%20documentation/No-code%20agents%20with%20LangSmith%20Fleet.md). If you use workload identity, you may need to update any service accounts.
* `POST /workspaces/current/members` now requires `role_id` for [RBAC](../../Govern/Users%20%26%20access%20control/Role-based%20access%20control.md)-enabled organizations. Requests without it return `400` instead of defaulting to `WORKSPACE_ADMIN`.
* Deprecated the `USAGE_EXPORT_ADMIN_EMAILS` environment variable. Use `INSTANCE_ADMIN_EMAILS` instead.
* Replaced the `projects:update-retention` permission with `projects:increase-trace-tier` and `projects:decrease-trace-tier` for separate control over raising and lowering trace retention. Permissions were backfilled to existing roles, so no changes are needed for existing roles. New roles should use the new permissions. See [RBAC permissions](../../Govern/Users%20%26%20access%20control/Role-based%20access%20control.md).
* Added a `fleet-admin:read` permission that gates the new Fleet Admin section. Admins of existing tenants need to grant it. Permissions were backfilled to existing roles, so no changes are needed for existing roles. New roles should use the new permissions. See [RBAC permissions](../../Govern/Users%20%26%20access%20control/Role-based%20access%20control.md).

### Infrastructure changes

* **Section renames from the Fleet rename**—several sections were renamed as part of the Agent Builder to [Fleet](../../../Additional%20documentation/No-code%20agents%20with%20LangSmith%20Fleet.md) rename (see [Breaking changes](#breaking-changes)). You may need to update service accounts or shift values in your configuration.
* **LLM Auth Proxy without a public ingress**—if the LLM Auth Proxy is deployed without a public ingress and is only reachable through internal Kubernetes networking, you must add `SSRF_ALLOW_K8S_INTERNAL` to all services that make LLM calls and `SSRF_ALLOW_PRIVATE_IPS_PLAYGROUND` to the `playground` service. Without these settings, the built-in SSRF protection blocks requests to private IPs. See [Deploy without a public ingress](../Configure%20an%20instance/Set%20up%20the%20LLM%20auth%20proxy.md#deploy-without-a-public-ingress) for full configuration details.

### New features

* **Context Hub**—version-controlled, environment-aware management of agent instructions and tools. Create and manage versioned [skill and agent repos](../../../Deploy/Prompt%20%26%20Context%20Hub/Context%20Hub/Context%20engineering%20concepts.md), promote commits to `staging` or `production` environments, and resolve context by environment tag at runtime. See [Use the Context Hub](../../../Deploy/Prompt%20%26%20Context%20Hub/Context%20Hub/Use%20the%20Context%20Hub.md) and [Manage contexts with the SDK](../../../Deploy/Prompt%20%26%20Context%20Hub/Context%20Hub/Manage%20contexts%20with%20the%20SDK.md) to get started.
* **Reusable evaluators and evaluator templates**—a new [Evaluators](../../../Test/Evaluators/Manage%20evaluators.md) tab centralizes every evaluator in your workspace, with 30+ templates covering safety, response quality, trajectory, user behavior, and multimodal evaluation. Attach an existing evaluator to a new tracing project in seconds without maintaining duplicate copies.
* **Per-example assertions**—write [assertions](../../../Test/Annotation%20Queues/Use%20assertions.md) instead of or alongside reference outputs when editing examples in an [annotation queue](../../../Test/Annotation%20Queues/Use%20annotation%20queues.md).
* **Downloadable Insights reports**—download an [Insights](../../../Monitor/Observe/Monitoring%20%26%20alerting/Discover%20errors%20and%20usage%20patterns%20with%20Insights.md) report as a PDF from the report details page for offline analysis.

### Admin changes

* **Expanded ABAC coverage**—[ABAC](../../Govern/Users%20%26%20access%20control/Attribute-based%20access%20control.md) now applies to `runs:create` on `POST /runs` and `POST /runs/batch`, plus the remaining `/sessions/{session_id}/` endpoints.
* **SCIM email-case-mismatch fix**—identity providers that send a different email casing are no longer rejected as email-change attempts.

**Download the Helm chart:** [`langsmith-0.15.0.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.15.0/langsmith-0.15.0.tgz)

**2026-05-26**

## langsmith-0.15.0-rc.17

* This release packages the same LangSmith application version as langsmith-0.15.0-rc.14. Refer to the [langsmith-0.15.0-rc.14](#langsmith-0-15-0-rc-14) release notes below.

**Download the Helm chart:** [`langsmith-0.15.0-rc.17.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.15.0-rc.17/langsmith-0.15.0-rc.17.tgz)

**2026-05-21**

## langsmith-0.15.0-rc.16

* This release packages the same LangSmith application version as langsmith-0.15.0-rc.14. Refer to the [langsmith-0.15.0-rc.14](#langsmith-0-15-0-rc-14) release notes below.

**Download the Helm chart:** [`langsmith-0.15.0-rc.16.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.15.0-rc.16/langsmith-0.15.0-rc.16.tgz)

**2026-05-20**

## langsmith-0.15.0-rc.15

* This release packages the same LangSmith application version as langsmith-0.15.0-rc.14. Refer to the [langsmith-0.15.0-rc.14](#langsmith-0-15-0-rc-14) release notes below.

**Download the Helm chart:** [`langsmith-0.15.0-rc.15.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.15.0-rc.15/langsmith-0.15.0-rc.15.tgz)

**2026-05-20**

## langsmith-0.8.31

* This release packages the same LangSmith application version as langsmith-0.8.30. Refer to the [langsmith-0.8.30](#langsmith-0-8-30) release notes below.

**Download the Helm chart:** [`langsmith-0.8.31.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.8.31/langsmith-0.8.31.tgz)

**2026-05-18**

## langsmith-0.15.0-rc.14

* Fixed the truncation issue of the 'Enabled' column in the automations table.
* Improved handling of click events in the UI with the polly button icon fix.
* Implemented multiple UI enhancements such as the addition of solid icons, icon xs variants, and updated details view headers.
* Improved performance by removing unused join operations from session stats and optimizing query handling.
* Added new event hooks for model invocation and updated the fleet-admin permissions to include read access.
* Expanded model support with new tools for GLM5 and Minimax 2.5.
* Added new features to the evaluator UI, including filters by created\_by, feedback key, and resource.
* Recognized external type definitions in evaluators, enabling more sophisticated feedback and sorting options.
* Introduced loading improvements for better data handling in various Fleet UI components.
* Enhanced fleet management with tool usage breakdowns, spend limit enforcement, and improved usage dashboards.
* Added support for auditing logs across Go write endpoints and audit logging for sensitive data access.
* Implemented new security features such as SSRF protection, transparent HTTP/HTTPS proxying, and enhanced authorization for self-hosted environments.
* Supported service identification with GitHub OAuth installation synchronization and CRUD operations.
* Introduced mobile-friendly login and a Progressive Web App (PWA) capability.
* Added the capability to invite users to organizations via a new endpoint.
* Enhanced message processing with SubAgentDetails, facilitating better context capture and management.

**Download the Helm chart:** [`langsmith-0.15.0-rc.14.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.15.0-rc.14/langsmith-0.15.0-rc.14.tgz)

**2026-05-14**

## langsmith-0.15.0-rc.13

* This release packages the same LangSmith application version as langsmith-0.15.0-rc.12. Refer to the [langsmith-0.15.0-rc.12](#langsmith-0-15-0-rc-12) release notes below.

**Download the Helm chart:** [`langsmith-0.15.0-rc.13.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.15.0-rc.13/langsmith-0.15.0-rc.13.tgz)

**2026-05-14**

## langsmith-0.14.6

* Fixed storage issue by backporting S3 CopyObject KMS headers to v14, improving data transfer security for S3 integrations.
* Fixed security vulnerabilities: CVE-2026-40192, CVE-2026-40347, CVE-2026-41205, CVE-2026-42561

**Download the Helm chart:** [`langsmith-0.14.6.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.14.6/langsmith-0.14.6.tgz)

**2026-05-13**

## langsmith-0.15.0-rc.12

* Fixed the truncation issue in the 'Enabled' column of the automations table to improve UI usability.
* Improved the evaluator details page and added sorting capabilities for created and updated timestamps.
* Enhanced evaluator tables by adding a type filter and click-to-filter functionality for type, feedback key, and resource cells.
* Added a new evaluator reuse feature to streamline the use of existing evaluators.
* Improved frontend evaluators to include feedback key and resource filters, enhancing usability.
* Added support for tracing tool usage and displaying agent names in the usage dashboard, enhancing performance insights.
* Enhanced mobile friendliness and PWA support for login interfaces.
* Improved performance by optimizing session synchronization and indexing strategies.
* Added mTLS support for ClickHouse migrations.
* Added parallel tool calls rendering in the messages view for better visual representation of concurrent processes.
* Introduced a new endpoint to update licenses for self-hosted instances via JWT.
* Added a new UI section for displaying evaluator actions required when creating an issue board.
* Implemented mobile-friendly login and an installable PWA to enhance accessibility for mobile users.
* Enhanced DataGrid components for better UI performance in tracing views.

These updates focus on improving user experience, performance, security, and feature set for self-hosted deployments.

**Download the Helm chart:** [`langsmith-0.15.0-rc.12.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.15.0-rc.12/langsmith-0.15.0-rc.12.tgz)

**2026-05-11**

## langsmith-0.15.0-rc.10

* This release packages the same LangSmith application version as langsmith-0.15.0-rc.4. Refer to the [langsmith-0.15.0-rc.4](#langsmith-0-15-0-rc-4) release notes below.

**Download the Helm chart:** [`langsmith-0.15.0-rc.10.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.15.0-rc.10/langsmith-0.15.0-rc.10.tgz)

**2026-05-09**

## langsmith-0.15.0-rc.9

* This release packages the same LangSmith application version as langsmith-0.15.0-rc.4. Refer to the [langsmith-0.15.0-rc.4](#langsmith-0-15-0-rc-4) release notes below.

**Download the Helm chart:** [`langsmith-0.15.0-rc.9.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.15.0-rc.9/langsmith-0.15.0-rc.9.tgz)

**2026-05-08**

## langsmith-0.15.0-rc.8

* This release packages the same LangSmith application version as langsmith-0.15.0-rc.4. Refer to the [langsmith-0.15.0-rc.4](#langsmith-0-15-0-rc-4) release notes below.

**Download the Helm chart:** [`langsmith-0.15.0-rc.8.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.15.0-rc.8/langsmith-0.15.0-rc.8.tgz)

**2026-05-08**

## langsmith-0.15.0-rc.7

* This release packages the same LangSmith application version as langsmith-0.15.0-rc.4. Refer to the [langsmith-0.15.0-rc.4](#langsmith-0-15-0-rc-4) release notes below.

**Download the Helm chart:** [`langsmith-0.15.0-rc.7.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.15.0-rc.7/langsmith-0.15.0-rc.7.tgz)

**2026-05-06**

## langsmith-0.15.0-rc.6

* This release packages the same LangSmith application version as langsmith-0.15.0-rc.4. Refer to the [langsmith-0.15.0-rc.4](#langsmith-0-15-0-rc-4) release notes below.

**Download the Helm chart:** [`langsmith-0.15.0-rc.6.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.15.0-rc.6/langsmith-0.15.0-rc.6.tgz)

**2026-05-05**

## langsmith-0.15.0-rc.5

* This release packages the same LangSmith application version as langsmith-0.15.0-rc.4. Refer to the [langsmith-0.15.0-rc.4](#langsmith-0-15-0-rc-4) release notes below.

**Download the Helm chart:** [`langsmith-0.15.0-rc.5.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.15.0-rc.5/langsmith-0.15.0-rc.5.tgz)

**2026-05-04**

## langsmith-0.15.0-rc.4

* Enhanced the Messages View with auto-scroll navigation, parallel tool calls rendering, and improved styling
* Improved Messages View performance with better memory utilization and processing times
* Added thread ID display in run details with copy-to-clipboard functionality
* Added the ability to open threads in new tabs
* Fixed dark mode gradient styling
* Fixed OAuth refresh race condition in Fleet
* Fixed run rules not marking matched runs as completed in Redis at max attempts
* Fixed dataset evaluators incorrectly created with group\_by thread\_id
* Added new run rules logic for workspaces with no existing rules
* Removed self-hosted gate for Fleet usage page
* Hidden minimal reasoning effort option for GPT-5.x models in the playground

**Download the Helm chart:** [`langsmith-0.15.0-rc.4.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.15.0-rc.4/langsmith-0.15.0-rc.4.tgz)

**2026-05-01**

## langsmith-0.14.5

* Fixed the agent-builder failure to start on v14 self-hosted 0.14.6 due to the `langgraph-api 0.8.3` base image bundling `LangSmith 0.7.37`, which removed `SandboxTemplate`, by pinning `LangSmith<0.7.34` to downgrade to a compatible version.

**Download the Helm chart:** [`langsmith-0.14.5.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.14.5/langsmith-0.14.5.tgz)

**2026-04-30**

## langsmith-0.15.0-rc.3

* This release packages the same LangSmith application version as langsmith-0.15.0-rc.1. Refer to the [langsmith-0.15.0-rc.1](#langsmith-0-15-0-rc-1) release notes below.

**Download the Helm chart:** [`langsmith-0.15.0-rc.3.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.15.0-rc.3/langsmith-0.15.0-rc.3.tgz)

**2026-04-29**

## langsmith-0.14.3

* Fixed silent corruption of `traceId`, `spanId`, and `parentSpanId` for OTLP/JSON (`Content-Type: application/json`) trace ingestion.
* Reduced Microsoft Graph permission requirements for Microsoft 365 docs and Teams private-message tools.

**Download the Helm chart:** [`langsmith-0.14.3.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.14.3/langsmith-0.14.3.tgz)

**2026-04-24**

## langsmith-0.15.0-rc.2

* This release packages the same LangSmith application version as langsmith-0.15.0-rc.1. Refer to the [langsmith-0.15.0-rc.1](#langsmith-0-15-0-rc-1) release notes below.

**Download the Helm chart:** [`langsmith-0.15.0-rc.2.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.15.0-rc.2/langsmith-0.15.0-rc.2.tgz)

**2026-04-24**

## langsmith-0.15.0-rc.1

* Fixed truncation issue by widening the 'Enabled' column in the automations table for better header visibility.
* Updated details view header for improved user experience.
* Improved performance by removing dead run\_stats\_facets join from session stats queries.
* Fixed MCP server filter dropdown to make it scrollable.
* Added 'user cost' table and toggle for agent/user view in the fleet.
* Enhanced security by adding URL allowlist enforcement for JWT injection.
* Added ability to sort evaluators by creation and update time in the backend.
* Added 'Feedback Key' filtering in the evaluators table for more precise searches.
* Showed back button on the full-page trace view to enhance navigation.
* Fixed audit-logs and various performance improvements for lower latency.
* Enhanced UI by showing 'Feedback Key' in evaluator column dropdown.
* Added session insights, views, metadata, and dashboard endpoints to improve data accessibility.
* Fixed file creation issues to prevent active interrupt state clearance.
* Provided async support for agents in the fleet to improve reliability.
* Fixed issues with agent cloning that previously caused flow issues.
* Added spend limit enforcement and the ability to track usage, enhancing cost management features.
* Made more efficient use of resources with new skill memory-store mirror updates in fleets.
* Improved evaluator reuse UX for users with better management of evaluator actions on issue generation.
* Enhanced security features by preventing sub-agents from triggering unauthorized actions.
* Optimized memory and resource management in the agent builder chat.
* Improved evaluator trace detail navigation by preserving search model in URLs.
* Upgraded per-environment favicon colors for clarity in staging and dev environments.
* Performance improvements in session sync reducing resource usage.
* Added default agent name support in usage dashboard for clarity in report generation.
* Made UI improvements to evaluator details for a smoother experience.
* Enabled auto-wake and auto-stop for Sandbox environments to save resources.
* Integrated tracing tool functionality in issue creation for better context and reliability.
* Added "create agent manually" button to navigation for easier agent management.
* Enhanced memory management tools UI for better approval process visualization.
* Fixed tool usage table and improved its performance for a better UX.
* Enabled auditing for sensitive data access endpoints for enhanced security compliance.
* Improved tracing project name display in usage dashboard for better project clarity.
* Introduced keyboard shortcuts in the editor page for rapid interaction.
* Set default MSP cron schedule as standard to reduce manual setup effort.
* Added integration user flow with prompt messages for smooth operation and understanding.
* Fixed default tracing project selection to Fleet to prevent inconsistencies.

**Download the Helm chart:** [`langsmith-0.15.0-rc.1.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.15.0-rc.1/langsmith-0.15.0-rc.1.tgz)

**2026-04-20**

## langsmith-0.14.2

* This release packages the same LangSmith application version as langsmith-0.14.0. Refer to the [langsmith-0.14.0](#langsmith-0-14-0) release notes below.

**Download the Helm chart:** [`langsmith-0.14.2.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.14.2/langsmith-0.14.2.tgz)

**2026-04-20**

## langsmith-0.14.1

* This release packages the same LangSmith application version as langsmith-0.14.0. Refer to the [langsmith-0.14.0](#langsmith-0-14-0) release notes below.

**Download the Helm chart:** [`langsmith-0.14.1.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.14.1/langsmith-0.14.1.tgz)

**2026-04-20**

## langsmith-0.14.0

LangSmith Self-Hosted v0.14 brings **Chat** (our in-product chat for traces and runs) to self-hosted, takes **ABAC and audit logs** GA (on by default), and enables the **LLM Auth Proxy** by default with URL allowlisting and richer JWT claims. Admins get **unified model configurations** shared across Agent Builder, Chat, Insights, Playground, and Evaluators, and fine-grained **Prompt Owners** for locking down who can promote or delete individual prompts. Evaluators gain **multi-modal support** and workspaces can now set **cost alerts** on tracing projects. Playground model support expands (Anthropic via Gemini Enterprise Agent Platform, custom Azure models, Bedrock inference profiles, Gemini 3.1 Pro, GPT-5.3 / 5.4, Baseten + GLM-5), and new agent tools and triggers land for Google Sheets & Docs, Outlook, Teams, and Salesforce SOQL. On the infrastructure side, v0.14 adds **GCS Workload Identity** support for blob storage, **Valkey** as a drop-in Redis replacement, and a pre-upgrade migration hook for safer rollouts.

Follow the [upgrade instructions](../Manage%20an%20instance/Upgrade%20an%20installation.md) to get access to everything. To book time with LangChain support for your upgrade, contact the team via the [Support Portal](https://support.langchain.com).

### Breaking changes

* Fixed an issue where `host-backend` wasn't picking up `commonEnv`. This may result in duplicate environment variables that need to be removed.

### Infrastructure changes

* Migrations now run as a `Pre-upgrade` hook prior to image versions rolling out. This will prevent issues when migrations fail.
* **GCS Workload Identity support**—authenticate to GCS blob storage using cloud-native workload identity instead of long-lived credentials.
* **Valkey support**—Valkey can now be used as a drop-in replacement for Redis.

### New features

* **Chat on self-hosted**—in-product Chat for understanding traces, runs, and evaluator feedback is now available in self-hosted.
* **ABAC and audit logs GA**—Attribute-Based Access Control and audit logs are enabled by default for self-hosted deployments.
* **LLM Auth Proxy on by default**—URL allowlist prevents credential forwarding to unintended hosts, and JWTs now carry `organization_name` and `workspace_name` claims.
* **Unified model configurations**—Agent Builder, Chat, Insights, Playground, and Evaluators now share a single set of model configs, with workspace-admin controls over model access across all AI features.
* **Prompt Owners**—designate a specific group of users with fine-grained permission to promote or delete individual prompts, without granting broader org access.
* **Multi-modal evaluators**—pass attachments and base64 content (images, audio, PDFs) directly into evaluators.
* **Cost alerts on tracing projects**—set alerts on tracing project-level costs alongside existing LangSmith alerts.
* **Expanded playground model support**—Anthropic via Gemini Enterprise Agent Platform, custom Azure models, Bedrock inference profiles and configurable base URLs, Gemini 3.1 Pro, GPT-5.3 / 5.4 (now default), and Baseten + GLM-5.
* **New agent tools and triggers**—Google Sheets and Docs, Outlook mail and calendar, Microsoft Teams, Salesforce SOQL, Gmail OAuth v2 with refresh tokens, and an Outlook Trigger.
* **Insights enhancements**—scheduled Insights reports, categories trending over time, full feedback comments in analysis, and a lower minimum job interval (6h → 1h).
* **Annotation and review upgrades**—required reviewers per queue, pairwise queues that honor `reviewer_access_mode`, an "Assigned to me" filter, per-annotator CSV export, and bulk table actions.
* **Prompt Hub and tool registry**—commit tag search, model select in template creation, a workspace-scoped tool registry API, and a private registry UI.
* **Evaluator workflow improvements**—prebuilt LLM evaluators use strict structured outputs by default, evaluators support tagging and reuse, retries no longer lose scores, and a new API runs playground experiments programmatically.
* **Custom iframe output renderer**—drag-to-resize HTML chart outputs in experiments and trace views.
* **Thread and inbox UX**—auto-generated thread titles, redesigned run details in threads, session-level feedback stats, keyboard shortcuts, and filtering out internal helper threads.

### Admin changes

* **Granular usage reporting**—granular billable usage APIs that allow you to retrieve detailed trace usage data broken down by workspace, project, user, or API key.

**Download the Helm chart:** [`langsmith-0.14.0.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.14.0/langsmith-0.14.0.tgz)

**2026-04-17**

## langsmith-0.13.43

* This release packages the same LangSmith application version as langsmith-0.13.42. Refer to the [langsmith-0.13.42](#langsmith-0-13-42) release notes below.

**Download the Helm chart:** [`langsmith-0.13.43.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.13.43/langsmith-0.13.43.tgz)

**2026-04-14**

## langsmith-0.13.42

* Fixed issue in metadata filtering to recognize json.Number as a primitive type, improving data ingestion accuracy.

**Download the Helm chart:** [`langsmith-0.13.42.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.13.42/langsmith-0.13.42.tgz)

**2026-04-14**

## langsmith-0.13.41

* Internal improvements and maintenance updates

**Download the Helm chart:** [`langsmith-0.13.41.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.13.41/langsmith-0.13.41.tgz)

**2026-04-09**

## langsmith-0.13.40

* Added support for mTLS configuration to enhance self-hosted security.
* Improved the loading speed of the Fleet interface.
* Fixed a bug in the tracing UI that caused intermittent display issues.
* Added support for Redis Cluster, improving scalability for self-hosted deployments.
* Improved PostgreSQL IAM integration for better database management in self-hosted instances.

**Download the Helm chart:** [`langsmith-0.13.40.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.13.40/langsmith-0.13.40.tgz)

**2026-04-07**

## langsmith-0.13.39

* Users can now run experiments without `projects:create`, decoupling experiment execution from project governance controls.
* Added skeleton loading state when switching between agent chat threads instead of a blank chat input.
* Improved the Fleet Arcade integrations page to display correct actions and clearer backend states.
* Arcade gateway installs now automatically sanitize invalid MCP server names before adding them to a workspace.
* Users can now see assigned reviewers as name chips in the annotation queue list and filter to queues they are assigned to via an "Assigned to me" button.
* Improved run details hover on the trace tree for less flicker when clicking or moving quickly between rows.
* Fixed a timeout when generating Insights reports with feedback enabled on high-volume workspaces.
* Arcade integrations now show a permission error instead of a generic upstream failure when a connected user lacks access to the configured Arcade project.
* Added a clickable ID badge to the experiment detail page header for easy copying of the experiment ID.
* LLM auth proxy JWTs now include `organization_name` and `workspace_name` claims.
* Added dataset split selection to the evaluator playground, allowing users to run evaluator experiments on specific dataset splits.
* Fixed experiment comparison view showing contradictory improvement arrows and regression cell colors for composite scores.
* Fixed a bug where deleting traces from pre-compression multipart blob storage objects could corrupt byte ranges for other traces in the same object, causing 416 errors when reading their payloads.
* Fixed crash when viewing a tool run in an in-progress trace.
* Lowered Insights job schedule minimum interval from 6 hours to 1 hour, configurable via `CLIO_SCHEDULE_MIN_INTERVAL_SECONDS` environment variable.
* LLM auth proxy now supports Insights (CLIO) service identity for JWT-based LLM authentication.
* Fixed subagent files not being deleted from hub repo memory when subagents are removed in the agent editor.
* Simplified Arcade workspace connection status to show "Workspace configured" instead of the confusing "Connected account" label with a redundant badge.
* Fixed a bug where expanding a tool call in the run detail view and scrolling away caused it to collapse back when scrolled into view again.
* Agent file reads (clone, inspect, startup) now correctly use the hub as the source of truth when hub memory is enabled.
* Fixed custom output rendering (HTML charts via iframe) not working in the redesigned experiment detail panes.
* Allowed usage of LLM Auth Proxy in self-hosted by default.
* Sessions facets raw path now returns input/output KV facets when `RUNS_LITE_STATS_TENANTS` is enabled, matching the Python backend behavior.
* Click-to-copy tooltips (e.g. project ID) now respond to clicks on the tooltip content itself, not just the trigger badge.
* Improved MCP server authorization enforcement in the platform backend.
* Added Baseten as a model provider with GLM-5 support.
* Improved LLM inference efficiency by reducing date precision in system prompts from minute-level to date-only.
* Fixed Polly losing trace context when a trace page is expanded to full page view.
* Added a unified files sidebar to Fleet chat, accessible via a "Files" button in the header, to browse, search, create, rename, move, and preview all agent-generated files in one panel.
* Added `SSRF_ALLOW_PRIVATE_IPS_WEBHOOKS`, `SSRF_ALLOW_PRIVATE_IPS_MCP_SERVERS`, and `SSRF_ALLOW_PRIVATE_IPS_TOOLS` environment variables to allow self-hosted deployments to connect to services on private IP ranges.
* Added `get_current_time` tool to Polly so relative time expressions in filter queries resolve correctly.
* Reference outputs are now always visible in the experiment trace detail view, fixing an issue where they were hidden for some organizations.
* Fixed agent OAuth connections failing with "Unknown provider" errors for non-personal agents.
* Added Base URL configuration support for Bedrock models in the playground and model configurations, enabling custom endpoint URLs for proxy or gateway deployments.
* Added sign out button back to the settings page sidebar.
* The run rules list endpoint now returns `backfill_id` when backfill progress is requested.
* SSO users can no longer see or accept pending invites to organizations other than their own SSO organization.
* Fleet webhook execution now uses a dedicated endpoint instead of the MCP proxy.
* Added session-level feedback stats to the sessions API for parity with the Python backend.
* Improved MCP proxy authorization and URL safety checks for agent runtime requests.

**Download the Helm chart:** [`langsmith-0.13.39.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.13.39/langsmith-0.13.39.tgz)

**2026-04-03**

## langsmith-0.13.38

* Fixed MCP OAuth tools (e.g., Hex, Notion) failing on self-hosted deployments when `HOST_BACKEND_ENDPOINT_PUBLIC` lacked an `https://` scheme.
* Insights agent now includes full feedback comments when analyzing traces.
* Removed the legacy Feed page in Fleet; Inbox is now the default thread view for all tenants.
* Fixed a permission error that blocked users from creating evaluators when using the evaluator reuse feature.
* Org admins can now grant Model Configuration management to workspace editors and custom roles via Settings > Roles.
* Pairwise annotation queues now respect `reviewer_access_mode`: completion/archive logic gates on assigned reviewers only, and GET responses include `assigned_reviewers`.
* Agent chat messages are no longer grouped into a collapsible "Completed N steps" container. A single copy dropdown on the last AI message of each turn lets you copy just the response or all steps including tool outputs.
* Fixed pagination in the waterfall view for thread traces, where threads with more than 20 turns now load additional traces when scrolling.
* Fixed "Empty Message" text appearing in the agent editor chat when AI invokes tools without accompanying text.
* Added Salesforce SOQL query tool to Fleet, enabling agents to query Salesforce data via OAuth.
* Annotation queue run list items now show reviewer names and avatars when hovering over the review stats badge.
* Go session stats now return `feedback_key`, `feedback_key_score`, `feedback_value`, and `feedback_source` facets in `run_facets`, matching the Python backend.
* Fixed `/info` endpoint returning 401 when `infoEndpointAuthRequired` is enabled with SSO authentication.
* Added a documentation link button to the "Trigger Webhook" section in the Save prompt dialog for easier access to webhook docs.
* Fixed layout shift in agent chat caused by the copy button unmounting during streaming.

**Download the Helm chart:** [`langsmith-0.13.38.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.13.38/langsmith-0.13.38.tgz)

**2026-04-01**

## langsmith-0.13.37

* Added URL allowlist for the LLM Auth Proxy to prevent credential forwarding to unintended hosts.
* Enabled audit logs by default for self-hosted deployments.
* MCP servers now respect granular RBAC permissions in the UI; users only see actions their role allows.
* Enabled ABAC by default for self-hosted deployments.
* Fixed a bug with OpenAI tools rendering.

**Download the Helm chart:** [`langsmith-0.13.37.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.13.37/langsmith-0.13.37.tgz)

**2026-03-30**

## langsmith-0.13.36

* This release packages the same LangSmith application version as langsmith-0.13.32. Refer to the [langsmith-0.13.32](#langsmith-0-13-32) release notes below.

**Download the Helm chart:** [`langsmith-0.13.36.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.13.36/langsmith-0.13.36.tgz)

**2026-03-27**

## langsmith-0.13.35

* This release packages the same LangSmith application version as langsmith-0.13.32. Refer to the [langsmith-0.13.32](#langsmith-0-13-32) release notes below.

**Download the Helm chart:** [`langsmith-0.13.35.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.13.35/langsmith-0.13.35.tgz)

**2026-03-27**

## langsmith-0.13.34

* This release packages the same LangSmith application version as langsmith-0.13.32. Refer to the [langsmith-0.13.32](#langsmith-0-13-32) release notes below.

**Download the Helm chart:** [`langsmith-0.13.34.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.13.34/langsmith-0.13.34.tgz)

**2026-03-27**

## langsmith-0.13.33

* This release packages the same LangSmith application version as langsmith-0.13.32. Refer to the [langsmith-0.13.32](#langsmith-0-13-32) release notes below.

**Download the Helm chart:** [`langsmith-0.13.33.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.13.33/langsmith-0.13.33.tgz)

**2026-03-27**

## langsmith-0.13.32

* Added ability for users to find account labels for first-class providers.
* Fixed issue where switching alerts did not switch charts accordingly.
* Fixed key error for experiments with attachments.
* Added dismiss button functionality to the agentify banner.
* Improved responsiveness in run details header and compare traces.
* Added truncate property to feedback chips list to respond to container width.
* Fixed subpixel bleed on body rows in the repetition summary table.
* Fixed race condition in AQ run archive check.
* Patched 9 medium security alerts and 4 high security alerts.
* Renamed Metadata to Attributes in the comparison detail pane.
* Enabled toggle panel size button in RepetitionDetailPane.
* Updated model cards in the frontend.
* Fixed issue to load prompt picker when opening playground from experiments table.
* Properly disabled environment promotion buttons for users without tag permissions.
* Enabled granular usage rollup cron for self-hosted instances.
* Onboarded more CUD operations for audit logs.
* Added Ashby integration migration to Agent Builder.
* Improved performance by parallelizing graph loading and eliminating redundant MCP fetches in Agent Builder.
* Automatically expanded/collapsed keys for improved UI.
* Fixed blue hover state for trace comparison divider.
* Avoided MITM races during sandbox startup with Smithbox proxy.
* Fixed bar height calculation in the granular usage chart.
* Added Dynatrace webhook integration for alerts.
* Displayed toast notification on "run now" button click in Forge.
* Handled non-string resource fields in MCP OAuth discovery.
* Added feedback banner for experiment sidebar redesign.
* Added example attachments to experiment detail panes.
* Wired Arcade integration to real OAuth flow in Agent Builder.
* Fixed loading flash in host revisions table during revalidation.
* Fixed imports in host backend for truststore.
* Added request context to authentication middleware error log in Agent Builder.
* Fixed editing prompt feature in evaluator.
* Fetched full run data in new experiment detail pane.

**Download the Helm chart:** [`langsmith-0.13.32.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.13.32/langsmith-0.13.32.tgz)

**2026-03-23**

## langsmith-0.13.31

* This release packages the same LangSmith application version as langsmith-0.13.28. Refer to the [langsmith-0.13.28](#langsmith-0-13-28) release notes below.

**Download the Helm chart:** [`langsmith-0.13.31.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.13.31/langsmith-0.13.31.tgz)

**2026-03-23**

## langsmith-0.13.30

* This release packages the same LangSmith application version as langsmith-0.13.28. Refer to the [langsmith-0.13.28](#langsmith-0-13-28) release notes below.

**Download the Helm chart:** [`langsmith-0.13.30.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.13.30/langsmith-0.13.30.tgz)

**2026-03-21**

## langsmith-0.13.29

* This release packages the same LangSmith application version as langsmith-0.13.28. Refer to the [langsmith-0.13.28](#langsmith-0-13-28) release notes below.

**Download the Helm chart:** [`langsmith-0.13.29.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.13.29/langsmith-0.13.29.tgz)

**2026-03-21**

## langsmith-0.13.28

* Fixed ABAC permission checks to improve self-hosted instance functionality.
* Enhanced agent builder by handling DotDict in decrypting passthrough headers.
* Improved fleet logo for better dark mode support.
* Updated Slack reauthorization required message with link to integrations page in Agent Builder.
* Added network allow-deny list feature.
* Introduced new access control UI for the sandbox proxy.
* Fixed GCS workload identity in storage and added copy health check.
* Reduced concurrency and added timeout for scheduled insights jobs.
* Enhanced frontend performance by reducing the number of preload chunks during initial load.
* Added caching for `/info` and `/auth/v1/user` responses in localStorage to improve frontend performance.
* Enabled JWT generation for auth-proxy in playground service for enhanced security.
* Recreated feedbacks index in the backend for storage optimization.
* Implemented gating for workspace skill editing by repo ownership in the Agent Builder.
* Added static TTL expiry for sandbox claims for improved management.
* Enabled Slack channels for personal agents in Agent Builder.
* Adjusted frontend contrast for run status icons in light mode for better visibility.
* Implemented JWT generation for LLM-as-judge evals to enhance evaluation security.
* Always display creator name on agent workspace cards for better transparency.
* Reordered inbox tabs to improve navigation.
* Supported Google IAP session refresh in self-hosted environments.
* Replaced MUI checkboxes in various sections to improve UI consistency.
* Improved experimental evaluator SAQ timeouts matching online eval paths for better performance.
* Supported RDS DB instance on k8s platform for enhanced infrastructure flexibility.
* Loaded LLM auth proxy JWT signing key from `LANGSMITH_SIGNING_JWKS` to align with security standards.
* Improved run detail dropdown design for a better user experience.
* Added service key authentication to runs, sessions, and sandbox endpoints for enhanced security.
* Added LangChain vendor extractor to enhance message processing capabilities.
* Fixed parsing errors related to cache reads impacting costs for better performance metrics.
* Introduced support for specifying environment variables from secret references for improved configuration management.

**Download the Helm chart:** [`langsmith-0.13.28.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.13.28/langsmith-0.13.28.tgz)

**2026-03-18**

## langsmith-0.13.27

* Organization admins can now edit member display names inline from the members table in Settings.
* Multipart ingestion requests no longer accept Inputs, Outputs, or Events as inline fields. These must be sent as dedicated out-of-band parts.
* Tracing support email on the Home page error banner is now a clickable mailto link.
* Improved run details tab highlighting so selected sections stay correctly highlighted near scroll boundaries.
* Improved keyboard shortcut rendering in the chat assistant tooltip.
* Fixed connect/disconnect button on Slack integrations.
* Added prompt environments support.

**Download the Helm chart:** [`langsmith-0.13.27.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.13.27/langsmith-0.13.27.tgz)

**2026-03-13**

## langsmith-0.13.26

* Sub-agents spawned during Fleet conversations now display real-time status cards inline in the chat, with a detail sidebar showing the sub-agent's live timeline, tool calls, and results.
* Prebuilt LLM evaluators now use strict structured output mode by default. Strict mode automatically toggles when switching between OpenAI and non-OpenAI model providers.
* Fixed a bug where online evaluator scores were lost when the evaluation succeeded on a retry but the total job time exceeded the queue timeout.
* Deleting a run from an annotation queue now fully removes it instead of incorrectly marking it as completed.
* Included per-annotator feedback in experiments CSV export.
* Uploading dataset examples with invalid UTF-8 in inputs or outputs now returns a 422 error instead of a 500.
* Reduced CPU and memory requirements for dev and dev\_free self-hosted deployments.
* Reject insecure default JWT secret at startup for improved security.
* Updated brand colors for neutral backgrounds and surfaces.
* Renamed prompt usage example label from "Use object in LangChain" to "Use Programmatically".
* Fixed agent zip upload to correctly place cron schedules in the Schedule section.
* Inbox now sorts the All tab by recency and properly wraps long messages in preview.
* Fixed chat assistant tooltips rendering behind the chatbox.
* Added ABAC authorization middleware.

**Download the Helm chart:** [`langsmith-0.13.26.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.13.26/langsmith-0.13.26.tgz)

**2026-03-12**

## langsmith-0.13.25

* This release packages the same LangSmith application version as langsmith-0.13.24. Refer to the [langsmith-0.13.24](#langsmith-0-13-24) release notes below.

**Download the Helm chart:** [`langsmith-0.13.25.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.13.25/langsmith-0.13.25.tgz)

**2026-03-10**

## langsmith-0.13.24

* Added rich markdown editor with toolbar and slash commands in Fleet.
* Added skill creation flow with page entry and navigation in Fleet.
* Annotation queue CSV exports now include per-annotator feedback scores and a reviewer notes column.
* Fixed dataset metadata filters not matching number fields across pages.
* Fixed datasets table only showing first page of results on tall screens.
* Alert like/notlike filters on error, inputs, and outputs now correctly match individual tokens instead of the full phrase.
* Fixed `list_runs` tool crashing when the LangSmith API returns an error.
* Fixed stray artifact in system prompt for Gemini models.
* Accepting an organization invite now navigates to the newly joined organization.
* Improved Playground auto-scroll during streaming output.
* Added workspace scope display for personal API keys.
* Bumped Python to 3.13 and pinned OpenSSL to resolve security vulnerabilities.
* Blocked shell injection characters in build/install commands.
* Improved Polly assistant understanding of traces and runs.
* Fixed baseline experiment stats not showing on initial page load.
* Fixed duplicated x-axis date labels on the insights time series chart.
* Re-enabled ABAC for listing datasets.
* Added ABAC runs delete endpoint.

**Download the Helm chart:** [`langsmith-0.13.24.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.13.24/langsmith-0.13.24.tgz)

**2026-03-07**

## langsmith-0.13.23

* Patched security vulnerabilities in smith-frontend.
* Patched security vulnerabilities in smith-polly.
* Fixed a code injection vulnerability.
* Restricted `--allow-run` to only the deno binary in smith-ace.
* Fixed XSS vulnerability by escaping URLs in the RichTextEditor.
* Fixed Playground functionality in self-hosted environments.

**Download the Helm chart:** [`langsmith-0.13.23.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.13.23/langsmith-0.13.23.tgz)

**2026-03-06**

## langsmith-0.13.21

* This release packages the same LangSmith application version as langsmith-0.13.20. Refer to the [langsmith-0.13.20](#langsmith-0-13-20) release notes below.

**Download the Helm chart:** [`langsmith-0.13.21.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.13.21/langsmith-0.13.21.tgz)

**2026-03-06**

## langsmith-0.13.20

* Added JSON/YAML syntax highlighting to experiment comparison for better readability.
* Improved thread trace opening behavior in the frontend, removing the need for an expand button.
* Eliminated n+1 query issue in the backend for listing personal access tokens, improving performance.
* Fixed support for OpenAI compatible endpoints with smith-polly integration.
* Timed out bulk exports stuck in `CREATED` status to avoid indefinite processing.
* Addressed issue where service identity access was blocked from creating repository endpoints.
* Recorded hub prompt commit in experiment session metadata for better session tracking.
* Improved authentication for /sessions shadow queries.
* Updated backend deployments with ABAC (Attribute-Based Access Control).
* Enhanced UI with projects and runs write permissions support.
* Added support for new models: GPT-5.4 and GPT-5.4 pro.
* Fixed large attachment image preview issue for better UI experience.
* Made GPT-5.4 the default OpenAI playground model, simplifying model selection.
* Increased maximum tags displayed in `RunTags` component for better visibility.
* Added models and prompts columns to experiments table, enhancing data insights.
* Resolved agent builder runs rejection issue when limit settings were changed.
* Fixed float errors in /sessions go endpoint for improved data handling.
* Returned fetched value when Redis cache `SET` fails, improving reliability.
* Enabled AWS IAM role support for agent builder, Polly, and Insights features.
* Redesigned custom chart CRUD in the frontend, enhancing user satisfaction.
* Introduced prompt filtering in the experiments table for targeted data analysis.
* Updated inbox counts and thread fetching logic in Agent Builder for real-time information.
* Added a feature to group experiments by prompt for streamlined data management.

**Download the Helm chart:** [`langsmith-0.13.20.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.13.20/langsmith-0.13.20.tgz)

**2026-03-06**

## langsmith-0.13.19

* This release packages the same LangSmith application version as langsmith-0.13.18. Refer to the [langsmith-0.13.18](#langsmith-0-13-18) release notes below.

**Download the Helm chart:** [`langsmith-0.13.19.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.13.19/langsmith-0.13.19.tgz)

**2026-03-05**

## langsmith-0.13.18

* Introduced a redesigned run details view in threads for improved user experience.
* Fixed an issue where popovers were covering other content in the UI.
* Added Microsoft Outlook Calendar Tools to the Agent Builder for integration.
* Addressed bugs related to agent chat popups and placeholders in the Agent Builder.
* Improved support for disabling feedback comment filtering in self-hosted instances.
* Enhanced performance with improved code splitting in the frontend.
* Added model support for GPT 5.3 instant and GPT-5.3-chat-latest.
* Introduced a new single\_run filter type for more refined querying.
* Added ability to read insights reports and show insights categories over time.
* Added drag-to-resize functionality with persistence in custom iframe output renderer.
* Enhanced security with more robust user migration processes.
* Enabled tagging support for evaluators and enhanced their reuse functionality.
* Fixed issues with session expired warnings after logout.
* Enhanced UI components for better user interaction in the playground and feedback tagging.
* Improved metadata handling in datasets and fixed overflow issues.
* Introduced support for Microsoft Teams Tools in the Agent Builder.
* Implemented better handling for OAuth provider updates.
* Added new /orgs/current/info endpoint to the platform-backend for more robust organizational information retrieval.
* Introduced compatibility testing for session API with added safety checks for PostgreSQL and Redis connections.
* Added functionality to bind Slack agents dynamically, enhancing the integration experience.

**Download the Helm chart:** [`langsmith-0.13.18.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.13.18/langsmith-0.13.18.tgz)

**2026-03-03**

## langsmith-0.13.17

* Fixed a bug in the executor deployment handling for new operator versions.
* Added a setting to filter out internal helper threads from the inbox.
* Improved the evaluator's page by providing context to Polly's feedback.
* Forced trace filtering for dataset code evaluators to enhance stability.
* Updated OAuth mode management, restricting changes during updates.
* Fixed an issue with experiment cell colors to enhance user clarity.
* Improved the usage configuration modal to utilize a new TTL endpoint for trace retention.
* Addressed a bug where workspace invites were not displaying correctly in the UI.
* Applied brand color adjustments in dark mode and various UI elements.
* Enhanced OAuth callback security by preventing potential reflected XSS vulnerabilities.
* Added a dynamic OAuth feature for user management.
* Fixed a bug preventing filter updates when certain conditions were met.
* Implemented rebranding updates for the auth screen.
* Added a feature to collapse sidebar automatically on small viewports.
* Fixed issues with variable handling in playground evaluate mode.
* Enhanced the Agent Builder with infinite scroll and improved inbox fetching.
* Added a new Outlook Trigger feature in the Agent Builder.
* Upgraded agent-builder to use websockets and new OpenAI model API (gpt-5.3-codex).
* Fixed auto-save on API key during onboarding process.
* Resolved issues causing errors in the playground due to empty placeholders.
* Updated frontend with a new logo for favicon.
* Fixed authorization bugs in cron deployment for Gmail/Outlook.
* Updated styling in various UI components, including studio button and index column behavior.
* Enhanced onboarding snippets for better integration with Langchain Python.
* Added support for [custom separators in SCIM group names](../../Govern/Users%20%26%20access%20control/User%20management.md#configure-custom-separator).

**Download the Helm chart:** [`langsmith-0.13.17.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.13.17/langsmith-0.13.17.tgz)

**2026-02-26**

## langsmith-0.13.16

* This release packages the same LangSmith application version as langsmith-0.13.15. Refer to the [langsmith-0.13.15](#langsmith-0-13-15) release notes below.

**Download the Helm chart:** [`langsmith-0.13.16.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.13.16/langsmith-0.13.16.tgz)

**2026-02-26**

## langsmith-0.13.15

* Added rebranded primary colors to button under feature flag in the frontend UI.
* Replaced dataset autocomplete with tag input to improve user experience.
* Auto-hide and position Models column in the frontend based on data.
* Fixed revalidation conflict in the Smith frontend.
* Improved workspace model configurations to prevent text overflow with tooltips.
* Surfaced Models option in Group By popover under a feature flag.
* Supported loading ChatAnthropicVertex model configs in Smith-Polly.
* Added "No matching filters" message for empty search results in Filter Component Select V2.
* Enabled navigating automatically to insights with global scroll support.
* Resolved issues with playground and evaluators provider selector not filtering out disabled providers.
* Improved messaging mode user experience and styling.
* Implemented Raw Query Mode for Inline Filters.
* Allow `secret_key_ref` to be `None` in `K8sEnvVarSource` for backend improvements.
* Fixed agent builder UI to wrap question text on narrow viewports and dismiss "Add API Key to Get Started" dialog.
* Updated UX to match evaluator button height with tool button pattern.
* Persisted selected model in local storage for a consistent UI experience.
* Auto-generated thread titles for improved thread management.
* Enhanced backend by gating secrets access with granular RBAC permissions.
* Implemented Outlook Email Tools in the Agent Builder.
* Improved keyboard shortcuts in the inbox feature of the Agent Builder UI.

**Download the Helm chart:** [`langsmith-0.13.15.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.13.15/langsmith-0.13.15.tgz)

**2026-02-24**

## langsmith-0.13.14

* Fixed agent generation interruptions and handling, improving stability in the user experience.
* Fixed long feedback header text overflow when dragged to the last column.
* Added OAuth connections for built-in tools and providers on the tool page.
* Fixed crashes occurring on the run details page.
* Fixed onboarding dialog not fetching tools unnecessarily.
* Updated agent builder frontend to show real-time run count.
* Added private registry UI to the frontend.
* Enhanced support for SerializedConstructor model configs in playground and insights.
* Added Gemini 3.1 Pro model to playground and backend model lists.
* Fixed tool registry crash in the playground.
* Added support for Gmail authentication improvements, including refresh token capability.
* Added new API endpoints for running playground experiments using a new service.
* Improved UI for trace filters with version 2 UX using Filterbar.
* Enhanced syntax highlighting to match Figma design for standardization.
* Supported Gmail OAuth v2 with cron logic for higher reliability.
* Added new models column in the experiment view with updated filtering options.
* Supported multiple paths for query shadowing log improvements.
* Added UIs for managing and editing model API key names in the playground.

**Download the Helm chart:** [`langsmith-0.13.14.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.13.14/langsmith-0.13.14.tgz)

**2026-02-14**

## langsmith-0.13.13

* Reverted the PostgreSQL version to v14.7 and the Redis version to v7. This fixes breaking changes introduced in langsmith-0.13.10.
* Fixed internal error details being leaked in 5xx responses to enhance security.
* Improved View UI by moving SaveViewButton from ViewDropdown and changing SaveForm to a modal for better usability.
* Added model select dropdown to the template creation flow for enhanced user experience.
* Added warning for duplicate URLs when creating MCP server to prevent configuration errors.
* Added user context to agents and sub-agents for better feature functionality.
* Added support for SerializedConstructor model configs in the playground for improved flexibility.
* Enhanced UI by showing categorical feedback in experiment view config and hiding the sort icon.
* Improved playground and experiment views by fixing cell alignment.
* Added image upload support to facilitate better asset management.
* Added onboarding dialog to general-purpose agent for improved user guidance.
* Added spinner to loading triggers skeleton for better loading indication.

**Download the Helm chart:** [`langsmith-0.13.13.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.13.13/langsmith-0.13.13.tgz)

**2026-02-12**

## langsmith-0.13.12

* Improved button sizes and filter chip alignment in the InlineFilters UX.
* Added commit tags search and display to the Prompt Hub.
* Fixed issue with viewing experiments having objects for feedback scores.
* Enhanced tracing for the deploy\_image task.
* Added a search bar for the new consolidated filter dropdown.
* Added environment variable for globally disabling personal access token creation.
* Added cost charts feature.
* Improved homepage styling and fixed related design issues.
* Fixed issues with rerendering in General Purpose API (GPA).
* Improved system to count PENDING, RETRY, and FAILED transactions in self-hosted offline usage reporting.
* Enhanced the agent builder to localize the current date to the user's timezone.
* Added Bedrock inference profile dropdown to the playground.
* Improved error detection and messaging for server issues in agent-chat.
* Fixed styling issues including email count in invite modal and load state display in the agent editor.
* Implemented initial design for a tools page with feature flags.
* Added icon-only filter popover mode to the frontend filter UI.
* Added beacon endpoint for Self Hosted Agent Builder Runs Limiting.
* Enable new Granular Usage tab for reporting billable usage by workspace, project, user, and API key (enable with `DEFAULT_ORG_FEATURE_ENABLE_GRANULAR_USAGE_REPORTING=true` and `GRANULAR_USAGE_TABLE_ENABLED=true` environment variables in `commonEnv`)

**Download the Helm chart:** [`langsmith-0.13.12.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.13.12/langsmith-0.13.12.tgz)

**2026-02-12**

## langsmith-0.13.11

* Improved Agent Builder by using persisted simple model config.
* Fixed UI for Playground with better message block and tool button consistency.
* Added a search bar for the new consolidated filter dropdown.
* Fixed agent builder model selector for users without 'workspaces:manage' permission.
* Added file upload feature for General Purpose Agent.
* Added button to create General Purpose Agent.
* Enhanced the Playground by preserving baseline setting in URL on page reload.
* Improved Playground experiment table UI and alignment.
* Fixed bulk deletion of datasets to update the table correctly.
* Added new API: workspace-scoped tool registry API.
* Improved support for multifield runFields.
* Enhanced insights scheduler with backend changes.
* Added ability to navigate pages in Polly and an initial set of base evaluations.
* Added tracing enhancements to Agent Builder, including tool call tracing.
* Integrated changes to support custom model configs temporarily.

**Download the Helm chart:** [`langsmith-0.13.11.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.13.11/langsmith-0.13.11.tgz)

**2026-02-10**

## langsmith-0.13.10

* This release packages the same LangSmith application version as langsmith-0.13.9. Refer to the [langsmith-0.13.9](#langsmith-0-13-9) release notes below.

**Download the Helm chart:** [`langsmith-0.13.10.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.13.10/langsmith-0.13.10.tgz)

**2026-02-09**

## langsmith-0.13.9

* Fixed sorting of workspaces alphabetically in the new switcher to improve user experience.
* Improved playground with new tool modal design and model config popup windows for enhanced usability.
* Fixed issue with creating tags being idempotent.
* Modified Agent Builder to cache MCP tools list, session ID, and OAuth tokens for better performance.
* Fixed updated error message for exhausted agent builder runs.
* Fixed routing configuration for the agent builder /allow-run API endpoint.
* Fixed spacing of home page tables for improved UI.
* Fixed issue with datasets repeatedly fetching if empty.
* Fixed edit access for API keys for non-admin users.
* Added cost and token columns in the experiment view for better data insights.
* Fixed an issue where the Slack trigger was dropping messages due to authentication errors.
* Fixed boolean feedback values handling in comparison table cells.
* Updated service key subject for API calls to /allow-run for accurate authentication.
* Improved agent builder to use persisted simple model config.
* Fixed error state handling for OAuth login failures.
* Enhanced agent builder by ensuring threads display errors on reconnect in agent chat.
* Fixed UI to ensure the footer menu closes on organization switch.
* Improved tagging authentication by using specific resource auth.
* Enhanced UI to prevent closing the pane from within the app selector dropdown.
* Fixed potential SQL injection risks in feedback and annotation queue listing.
* Added a 15-second timeout to the OAuth HTTP client for improved connection reliability.

**Download the Helm chart:** [`langsmith-0.13.9.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.13.9/langsmith-0.13.9.tgz)

**2026-02-06**

## langsmith-0.13.7

* This release packages the same LangSmith application version as langsmith-0.13.6. Refer to the [langsmith-0.13.6](#langsmith-0-13-6) release notes below.

**Download the Helm chart:** [`langsmith-0.13.7.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.13.7/langsmith-0.13.7.tgz)

**2026-02-05**

## langsmith-0.13.6

* Fixed an issue with truncated large numbers affecting the user interface.
* Improved error string conversion from S3 to enhance error handling.
* Updated Filters UX to save DateTimeRange, improving user experience.
* Fixed UUID conversion to ensure consistent general agent identification.
* Fixed agent ID conversion to always use a string instead of UUID for stability.
* Enhanced the experiment comparison view by showing custom computed columns.
* Fixed chat preview for langchain-shaped output for better user experience.
* Improved caching mechanisms and authentication control planes' RetryableHTTP.
* Fixed the issue of incorrect tenant usage when bootstrapping agents.
* Improved user interface by adjusting page padding to remove visual obstructions.
* Updated wording for trace-related inquiries to improve clarity.
* Enhanced large field uploads to S3 for single run POST/PATCH endpoints.

**Download the Helm chart:** [`langsmith-0.13.6.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.13.6/langsmith-0.13.6.tgz)

**2026-02-05**

## langsmith-0.13.5

* Fixed regression on cloning prebuilt dashboards to enhance user experience.
* Updated Filters UX to match new mocks and improved the view dropdown.
* Fixed Agent Builder by converting `UUID` to `str` before JSON encoding to prevent errors.
* Added an updated insights sidebar for a more informative UI.
* Implemented bulk actions for tables to improve data management efficiency.
* Added a redesigned feedback banner for annotation queue in the frontend.
* Provided option to require feedback in the Smith frontend to enhance user communication.
* Limited Agent Builder template list to 2 rows for better usability.
* Fixed cursor jumping issue when editing agent builder skill name and description.
* Solved SSO+SCIM issue, always provisioning users to workspaces.
* Fixed Slack Auth disconnecting issue for workspace users.
* Enhanced missing tool experience in the Agent Builder by adjusting prompts.
* Prevented session fixation in self-hosted OAuth for enhanced security.
* Fixed the 'view run' regression in the annotation queue redesign in Smith frontend.
* Reduced gRPC streaming chunk size from 1MB to 64KB for improved performance.
* Added download zip button inside the Agent Builder Explorer.
* Enhanced tracing URLs allowed by adding them to the Datadog RUM config.

**Download the Helm chart:** [`langsmith-0.13.5.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.13.5/langsmith-0.13.5.tgz)

**2026-02-04**

## langsmith-0.13.4

* Fixed the toggle functionality for all column sections when clicking the Columns header.
* Fixed failure to edit SSO settings
* Improved frontend performance by using BarSeries instead of AnimatedBarSeries for granular usage tabs.
* Added a Cmd + Enter hotkey to the new annotation queue for enhanced user interaction.
* Added an option in the playground UI to mitigate loading errors by defaulting to `use_responses_api=true`.
* Added support for custom Azure models.
* Updated the playground UI for improved user experience.
* Improved studio chat UX with auto-resize textarea and keyboard shortcuts.
* Fixed prompt saving issue with incorrect naming.
* Improved visibility and user experience by making search icons larger and tracking navigation of AQ, prompts, and deployments.
* Enhanced UI for the Agent Builder with the introduction of a new Diff UI with context lines.
* Enabled accurate Y-axis margins using d3 nice ticks for better frontend visualization.
* Allowed the 'recently added to' section to pop over in the 'add to dataset' UI.
* Added pagination to the dashboard select view for better usability.
* Added support to limit long-lived TTL options and expose them in the org TTL settings endpoint.
* Fixed a bug with streaming flicker using the responses API in the playground.
* Enhanced the annotation queue user experience with custom output rendering in new queues.
* Optimized dataset session comparison using example\_ids filtering for better performance.
* Provided a download ZIP file button in the Agent Builder for user convenience.
* Added a streamlined loading state for the Agent Builder's agent generator graph.
* Allowed updating and creating SSO settings specifically in self-hosted environments.
* Added support for displaying SCIM user's `displayName` attribute.

These changes improve user interaction, enhance system performance, and expand support for custom models and infrastructure, benefiting self-hosted deployments.

**Download the Helm chart:** [`langsmith-0.13.4.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.13.4/langsmith-0.13.4.tgz)

**2026-01-26**

## langsmith-0.13.3

* Improved streaming to accumulate streamed delta data without loss.
* Added Google Sheets/Docs tools integration.
* Enhanced UX for OAuth servers in settings.
* Made view trace links more obvious in the UI.
* Resolved multiple bugs and performance issues in Agent Builder, including writing self-hosted Agent Builder runs to a single project and collapsing subagent tool cards by default.
* Improved experiment UI, now showing experiment descriptions on the single experiment page and fixing a blank page issue when accessing experiments via public URL.
* Enhanced UX by solving bulk export flakiness and allowing updating of bulk export destination credentials.
* Improved inline filter UX with multiple bug fixes and added edit functionality.
* Added support for configurable run input/output preview paths on the backend.
* Introduced new workspace management permissions for managing members' access.
* Optimized Agent Builder to reduce network calls.
* Added Action Menu to MyAgents Navlink in Agent Builder.
* Improved frontend performance, including solving slowness when loading authentication status.
* Enhanced Agent Builder with the API Key Needed Label/Button and collapsed action cluster features.
* Resolved playground tool modal overflow issue.
* Improved security by fixing frontend vulnerability in remix run router and clearing URLs on logout to prevent workspace misdirection.
* Updated API to use invoices for monthly burndown tracking and added support for V2 API.
* Improved frontend to handle malformed LLM outputs gracefully.
* Improved date/time selection UI by allowing bold "Last time" values for DateTimeRangePicker component.

**Download the Helm chart:** [`langsmith-0.13.3.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.13.3/langsmith-0.13.3.tgz)

**2026-01-21**

## langsmith-0.13.2

* Fixed content-type validation for dataset uploads to improve data handling.
* Improved the new annotation queue page with a pretty JSON editor and message list editor.
* Enabled better handling of retriable ingest errors on QueueRunPayloads.
* Fixed Cron Trigger updates in the Agent Builder UI.
* Added support for Redis Cluster, enhancing scalability for self-hosted setups.
* Fixed OAuth account takeover vulnerability to enhance security.
* Improved rendering of raw output in the playground.
* Added new inline UX filters and a View Dropdown component for enhanced user interaction.
* Increased line-height on XS Text variant to prevent clipping issues in the frontend.

**Download the Helm chart:** [`langsmith-0.13.2.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.13.2/langsmith-0.13.2.tgz)

**2026-01-16**

## langsmith-0.13.1

* This release packages the same LangSmith application version as langsmith-0.13.0. Refer to the [langsmith-0.13.0](#langsmith-0-13-0) release notes below.

**Download the Helm chart:** [`langsmith-0.13.1.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.13.1/langsmith-0.13.1.tgz)

**2026-01-16**

## langsmith-0.13.0

* Added support for [Agent Builder](../../../No-code%20agents/Fleet/No-code%20agents%20with%20LangSmith%20Fleet.md) in self-hosted deployments
* Added configurable trace TTL for long-lived traces
* Added ability to conditionally enable OAuth tools and triggers
* Added sample application creation during onboarding
* Fixed feedback pagination and auto-pagination bugs
* Fixed trace drawer skeleton not appearing immediately

**Download the Helm chart:** [`langsmith-0.13.0.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.13.0/langsmith-0.13.0.tgz)

**2026-01-12**

## langsmith-0.12.37

* This release packages the same LangSmith application version as langsmith-0.12.36. Refer to the [langsmith-0.12.36](#langsmith-0-12-36) release notes below.

**Download the Helm chart:** [`langsmith-0.12.37.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.12.37/langsmith-0.12.37.tgz)

**2026-01-09**

## langsmith-0.12.36

* Added support for custom MCP servers with OAuth in Agent Builder
* Added ability to view and edit memory files in Agent Builder
* Added support for attachments in the frontend
* Improved streaming tree performance in trace viewer
* Fixed scroll behavior in trace tree
* Fixed unicode truncation issues in trace display
* Fixed onboarding screen showing incorrectly when runs exist
* Increased maximum automation rules per workspace to 200

**Download the Helm chart:** [`langsmith-0.12.36.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.12.36/langsmith-0.12.36.tgz)

**2026-01-08**

## langsmith-0.12.35

* Added per-bar highlighting for feedback charts in experiments
* Added Agent Builder activity feed
* Changed experiment chip to hover card for better usability
* Fixed agents appearing in random sidebar positions
* Fixed tool modal nesting issue in playground
* Fixed diff mode fallback on comparison page
* Fixed race condition in OAuth authentication requests

**Download the Helm chart:** [`langsmith-0.12.35.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.12.35/langsmith-0.12.35.tgz)

**2025-12-26**

## langsmith-0.12.34

* Added Redis IAM authentication support for GCP and Azure
* Added self-serve audit logs in OCSF format
* Added hide column option to experiment outputs header
* Added message\_user tool to the tool server
* Improved trace tree loading speed
* Allowed basic auth installations to disable invites via API
* Fixed tenant ID handling in navigation
* Fixed scrolling in Agent Builder templates view
* Fixed Gmail account connection limit tooltip
* Fixed user view preference persistence on page load
* Fixed tab wrapping in UI
* Made feedback charts visible by default
* Made SCIM group name matching case-insensitive

**Download the Helm chart:** [`langsmith-0.12.34.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.12.34/langsmith-0.12.34.tgz)

**2025-12-20**

## langsmith-0.12.33

* Security fix: fixed Studio vulnerability to malicious `baseUrl` param by requiring user-defined allowed origins
* Allow enabling invites alongside JIT provisioning for SSO (OAuth with Client Secret mode only)
* Added self-serve audit logs for administrative actions (Private Preview)

**Download the Helm chart:** [`langsmith-0.12.33.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.12.33/langsmith-0.12.33.tgz)

**2025-12-12**

## langsmith-0.12.32

* Added IAM connection support for PostgreSQL (AWS only).
* Added GPT-5.2 model support to the playground.
* Added support for setting memory limits on executor pods.

**Download the Helm chart:** [`langsmith-0.12.32.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.12.32/langsmith-0.12.32.tgz)

**2025-12-11**

## langsmith-0.12.31

* Improved error messages for basic authentication misconfiguration.
* Added organization operator role support.
* Fixed issues with streaming datasets endpoint.

**Download the Helm chart:** [`langsmith-0.12.31.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.12.31/langsmith-0.12.31.tgz)

**2025-12-09**

## langsmith-0.12.30

* This release packages the same LangSmith application version as langsmith-0.12.29. Refer to the [langsmith-0.12.29](#langsmith-0-12-29) release notes below.

**Download the Helm chart:** [`langsmith-0.12.30.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.12.30/langsmith-0.12.30.tgz)

**2025-12-08**

## langsmith-0.12.29

* Added mTLS (mutual TLS) support for ClickHouse connections to enhance security for database communication.

**Download the Helm chart:** [`langsmith-0.12.29.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.12.29/langsmith-0.12.29.tgz)

**2025-12-05**

## langsmith-0.12.28

* Added mTLS (mutual TLS) support for PostgreSQL connections to enhance security for database communication.
* Added mTLS support for ClickHouse clients.
* Fixed Agent Builder onboarding and side navigation visibility when disabled in self-hosted deployments.

**Download the Helm chart:** [`langsmith-0.12.28.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.12.28/langsmith-0.12.28.tgz)

**2025-12-04**

## langsmith-0.12.27

* Added mTLS (mutual TLS) support for Redis connections to enhance security.
* Added support for empty trigger server configuration in self-hosted deployments.
* Improved incident banner styling and content.

**Download the Helm chart:** [`langsmith-0.12.27.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.12.27/langsmith-0.12.27.tgz)

**2025-12-02**

## langsmith-0.8.30

* Internal improvements and maintenance updates

**Download the Helm chart:** [`langsmith-0.8.30.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.8.30/langsmith-0.8.30.tgz)

**2025-12-01**

## langsmith-0.12.25

* Enabled Agent Builder UI feature flag for self-hosted deployments.
* Added Redis Cluster support for improved scalability and high availability.

**Download the Helm chart:** [`langsmith-0.12.25.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.12.25/langsmith-0.12.25.tgz)

**2025-11-27**

## langsmith-0.12.24

* Added dequeue timeouts to all SAQ (Simple Async Queue) queues to improve reliability.
* Performance improvements and bug fixes.

**Download the Helm chart:** [`langsmith-0.12.24.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.12.24/langsmith-0.12.24.tgz)

**2025-11-26**

## langsmith-0.12.23

* Internal improvements and maintenance updates

**Download the Helm chart:** [`langsmith-0.12.23.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.12.23/langsmith-0.12.23.tgz)

**2025-11-26**

## langsmith-0.12.22

* This release packages the same LangSmith application version as langsmith-0.12.21. Refer to the [langsmith-0.12.21](#langsmith-0-12-21) release notes below.

**Download the Helm chart:** [`langsmith-0.12.22.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.12.22/langsmith-0.12.22.tgz)

**2025-11-26**

## langsmith-0.12.21

* Added explicit `revisionHistoryLimit` configuration for operator deployment template.

**Download the Helm chart:** [`langsmith-0.12.21.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.12.21/langsmith-0.12.21.tgz)

**2025-11-24**

## langsmith-0.12.20

* This release packages the same LangSmith application version as langsmith-0.12.18. Refer to the [langsmith-0.12.18](#langsmith-0-12-18) release notes below.

**Download the Helm chart:** [`langsmith-0.12.20.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.12.20/langsmith-0.12.20.tgz)

**2025-11-24**

## langsmith-0.12.19

* This release packages the same LangSmith application version as langsmith-0.12.18. Refer to the [langsmith-0.12.18](#langsmith-0-12-18) release notes below.

**Download the Helm chart:** [`langsmith-0.12.19.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.12.19/langsmith-0.12.19.tgz)

**2025-11-20**

## langsmith-0.12.18

* Internal improvements and maintenance updates

**Download the Helm chart:** [`langsmith-0.12.18.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.12.18/langsmith-0.12.18.tgz)

**2025-11-19**

## langsmith-0.12.17

* Internal improvements and maintenance updates

**Download the Helm chart:** [`langsmith-0.12.17.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.12.17/langsmith-0.12.17.tgz)

**2025-11-19**

## langsmith-0.12.16

* Internal improvements and maintenance updates

**Download the Helm chart:** [`langsmith-0.12.16.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.12.16/langsmith-0.12.16.tgz)

**2025-11-17**

## langsmith-0.12.15

* Internal improvements and maintenance updates

**Download the Helm chart:** [`langsmith-0.12.15.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.12.15/langsmith-0.12.15.tgz)

**2025-11-17**

## langsmith-0.12.14

* Internal improvements and maintenance updates

**Download the Helm chart:** [`langsmith-0.12.14.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.12.14/langsmith-0.12.14.tgz)

**2025-11-13**

## langsmith-0.12.13

* This release packages the same LangSmith application version as langsmith-0.12.12. Refer to the [langsmith-0.12.12](#langsmith-0-12-12) release notes below.

**Download the Helm chart:** [`langsmith-0.12.13.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.12.13/langsmith-0.12.13.tgz)

**2025-11-13**

## langsmith-0.12.12

* Internal improvements and maintenance updates

**Download the Helm chart:** [`langsmith-0.12.12.tgz`](https://github.com/langchain-ai/helm/releases/download/langsmith-0.12.12/langsmith-0.12.12.tgz)

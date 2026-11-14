# LangSmith Cloud changelog

> Weekly updates to LangSmith Cloud

Weekly updates to [LangSmith Cloud](../../../Monitor/Overview/LangSmith%20Observability.md). For LangSmith Fleet, see the [Fleet changelog](../../../No-code%20agents/Fleet/Additional%20resources/LangSmith%20Fleet%20changelog.md).

**Subscribe**: This changelog includes an [RSS feed](https://docs.langchain.com/langsmith/changelog/rss.xml) that can integrate with [Slack](https://slack.com/help/articles/218688467-Add-RSS-feeds-to-Slack), [email](https://zapier.com/apps/email/integrations/rss/1441/send-new-rss-feed-entries-via-email), Discord bots like [Readybot](https://readybot.io/) or [RSS Feeds to Discord Bot](https://rss.app/en/bots/rssfeeds-discord-bot), and other subscription tools.

> [!NOTE]
>
> If you use self-hosted LangSmith, see the [self-hosted changelog](../../Self-hosted/Reference/Self-hosted%20LangSmith%20changelog.md) for updates.

**November 2-9, 2026**

## Highlights

* **Coding agents track GitHub pull request outcomes**: Coding agents now show GitHub pull request outcomes and spend on the agent overview. You can set an agent's type to Coding when you create it or from the agent actions menu, then open the GitHub connections dialog from the overview header to connect GitHub accounts, add another account, choose repository access, or reuse an installation already linked to another agent in your workspace. Usage appears directly on the overview, with a **No traces yet** state until production has a trace in the last 30 days. [Learn more](../../../Monitor/Trace/Tracing%20setup/Integrations/Developer%20tools/Coding%20agent%20metadata%20contract.md).
* **Online Insights with continuous analysis**: Insights now analyzes your traces continuously and keeps its categories current, so you no longer wait for a scheduled batch report. Ask a question to create an insight, adjust its settings with **Configure** before it runs, then view top categories, category trends over a 7, 14, or 30 day range, and an expandable breakdown with subcategories, feedback, latency, and cost metrics. New insights sample about 1,000 traces per week, and classifications that return arrays are now saved correctly. [Learn more](../../../Monitor/Observe/Monitoring%20%26%20alerting/Discover%20errors%20and%20usage%20patterns%20with%20Insights.md).
* **Full AI search for tracing projects**: You can describe what you want to find in plain language in a tracing project, and AI search turns it into structured filters, a semantic filter, and time bounds. It picks whether to search runs, traces, or threads, applies the result to your view, and shows the applied filters. When a request is ambiguous, AI search offers two or three interpretations under **Did you mean?** so you can pick one without running another search. [Learn more](../../../Monitor/Debug/Viewing%20%26%20managing%20traces/Filter%20traces%20%28ClickHouse%29.md).
* **Coding agent Usage dashboard with PR spend**: The Coding agent Usage tab now has a card for each of outcome, user, and model. Each card can be grouped, and a **Cost by conversation length** card and a **Top PRs by cost** card list your costliest pull requests with links to GitHub. You choose the time range with the shared date range picker, which accepts presets, typed durations, and specific dates. Pull request spend is attributed to the commit and branch that produced it, so you can see what each coding agent change costs. [Learn more](../../../Monitor/Trace/Tracing%20setup/Integrations/Developer%20tools/Coding%20agent%20metadata%20contract.md).
* **Scoped tool policies with call approvals**: Tool policies now let you block tool calls or require the caller to approve them first, and a blocking policy wins when both match the same call. You can scope each policy to every workspace, one workspace, or specific agent environments, and calls made with an agent's API key are also checked against that agent's policies. Workspace admins can create, edit, and delete policies for their own workspace from the **Policies** tab, while organization admins manage all policies.
* **Gateway requests appear as one trace**: Each LLM Gateway request now appears as a single trace with one run per attempt, so a request that falls back to another model shows both attempts in one place instead of two separate traces. Runs record the outcome, provider, model, and upstream status for each attempt, and requests refused before any provider call still get a trace. Policy checks that deny or throttle a request and data policy scans that modify or block content appear as their own runs under the attempt. [Learn more](../../../LLM%20Gateway/Observability/View%20LLM%20Gateway%20traces.md).

## Tracing

* Your workspace now has an hourly limit on persisted bytes, the full size of ingested runs including large fields and attachments. Ingestion is rejected once a workspace exceeds its `max_hourly_persisted_bytes` value, which defaults to 100 GB.
* OTEL ingest now enforces per-project monthly trace limits. Requests containing spans from a project over its limit receive a 429 response, while spans from other projects in the same workspace continue to be accepted.
* Session endpoints now include `GET /api/v2/sessions`, which lists projects with cursor paging and a `type` filter for `PROJECT`, `AGENT`, and `EXPERIMENT`, plus `GET /api/v2/sessions/{session_id}`, which returns one project with RFC 7807 error responses. The Python and TypeScript SDKs now include `sessions.delete` and `sessions.retrieve`.
* `POST /v1/trajectories/query` now returns conversation keys, message keys, message types, dotted orders, anchor IDs, agent types, insertion times, and available tools for messages you select in `message_select`. Send `Accept: text/event-stream` to stream results from `POST /v1/trajectories/query` or `GET /v1/trajectory/{scope_id}/stats` as JSON Patch events, and the stats response now includes a `tools` list with call counts and latencies for each tool.
* Every LangSmith CLI command that prints JSON now accepts `--jq` to filter the output with a jq expression, so you can trim results without installing `jq`. Strings, numbers, and booleans print bare, and objects and arrays print as compact JSON.
* You can now page through `langsmith runs list`, `traces list`, `prompt list`, `prompt commits`, and `hub list` with `--cursor`, so you no longer need to guess offsets. Pass `--cursor ""` on the first call to get `cursors.next` in JSON output, then pass that value back to resume right after the last item.
* You can now run `langsmith traces get` on a trace ID without `--project` on LangSmith Cloud. The CLI finds the trace in your workspace, and it asks for `--project` or `--project-id` on deployments that cannot run that lookup.
* `langsmith self-update` now detects when the CLI was installed with pip, pipx, or uv and prints the upgrade command for that install instead of replacing the binary. Use `--force` to update in place anyway.
* You can now call `instrumentation.WithoutContent(ctx)` in the Go SDK to trace LLM calls without recording prompts or completions, so spans keep model, usage, timing, and status and use less memory under high concurrency.
* Dashboard chart filters can now use v2 filter syntax for run, root-run, and any-run scopes. Chart saves reject a ratio metric whose run filter and operand filters mix legacy and v2 syntax, or whose combined filter is invalid.
* You can now download full traces of up to 2,000 runs as a single JSON file, up from 1,000. Traces with more than 2,000 runs show an error and must be downloaded run by run.
* `POST /runs` and `PATCH /runs/{id}` now reject request bodies over 200 MB with a 413 error, matching the limit on batch and multipart uploads.
* Project responses now return `total_cost`, `prompt_cost`, and `completion_cost` as numbers instead of text, so you can read them directly without parsing. This is a breaking change for SDK code that treats cost as text, such as Go code that calls `strconv.ParseFloat` on `TotalCost`.
* Ingest on BYOC data planes now keeps accepting runs during brief auth outages by using recently verified credentials.
* Coding agent Usage charts now refresh only when you press the new **Refresh** button beside the date range picker, so they no longer reload on focus, reconnect, or tab switches.

## Administration

* Your workspace now opens in the unified agent experience as soon as it is marked ready. The classic experience remains available as an opt-out in workspace settings.
* Revoked, deleted, and expired API keys stop authenticating right away instead of waiting for cached auth to refresh. Your tracing keys, service keys, and personal access tokens are checked against their current state on every request.
* `GET /api/v1/settings` now returns the full workspace model, the same response as `GET /api/v1/workspaces/{id}`. It adds fields such as `is_deleted`, `is_personal`, `permissions`, and `role_name`, and existing clients keep working.
* Members settings now match the API Keys page, with a searchable list, role and status filters, an All/Active/Pending/Deactivated toggle, sortable columns, and CSV export that follows your current filters. Select a member row to edit their name or role, and open a workspace count to search that member's workspaces. Role details and permissions previews now appear in invite and edit dialogs, with built-in workspace roles labeled Workspace Admin, Workspace Editor, and Workspace Viewer. Selecting Organization Admin sets the workspace fields to All workspaces and Workspace Admin, and you can find the reason for that in the disabled fields' tooltip.
* Workspaces that still call the deprecated `POST /runs/query` endpoint now see a countdown to its removal on January 31, 2027, in a banner at the top of the page. The banner offers a **Copy migration prompt** button for your coding agent, grows more urgent as the deadline approaches, and cannot be snoozed in the last 30 days.
* Organization model prices are now available for all workspaces. Admins and operators can set one price for an organization, and every workspace in it prices against that price unless the workspace defines its own. Organization prices reach only the workspaces on the data plane that served the write.
* Workspace-scoped MCP tools now require a `workspace_id` that is a LangSmith workspace UUID, and calls without one return an error instead of silently using the credential's default workspace. Organization-scoped tools do not require it.
* The `langsmith_agent` resource and `data.langsmith_agent` data source are now available in the LangSmith Terraform provider. You can create, update, import, and destroy agents as Terraform resources, and read their environments and tracing project IDs.
* Terraform: The langsmith\_workspace resource now accepts an optional data\_plane\_id, so you can create, rename, and delete workspaces on a BYOC data plane. Import and refresh keep workspace metadata visible with a warning when the data plane list is forbidden, and changes and deletion stay blocked until the data plane ID resolves.
* Custom organization roles now work with SCIM and SSO group sync. Name a group `LS:Billing Manager` to grant the **Billing Manager** organization role. Groups that reference an ambiguous role name are rejected, and unrelated groups still sync. Assignments update at the next sync, and a missing groups claim now removes SSO-managed assignments, as an empty list does.
* SCIM token creation, update, and deletion now require the `organization:scim-tokens:manage` permission. The Admin and Operator roles include it, and custom roles that relied only on `organization:authentication:manage` must add it to keep managing SCIM tokens.
* OIDC login now verifies ID token signatures against your provider's published keys before it trusts any identity claims. Token and UserInfo requests no longer follow redirects, so credentials cannot be sent to a redirect destination; self-hosted providers must expose their token and UserInfo endpoints directly, and providers without a reachable JWKS endpoint or a supported asymmetric signing algorithm can no longer log in.
* Microsoft Azure is now available as a cloud option when you sign up for LangSmith and in the Data Region menu when you log in. Choosing Azure takes you to the Azure US Central region.
* Resource tags now let you assign agent environments to a tag, so tagged projects appear as the agent name and environment, such as **Support bot** and **Production**. Selecting an agent lists its environments, and each tagged environment links to its tracing project.
* You can now bind workspace service keys to each environment of an external agent from the **API keys** item in the agent's settings menu. LLM Gateway requests made with a bound key are attributed to that agent and environment, and managing these keys requires the `workspaces:manage-keys` permission.
* Access policies now show the Add rule action beside the rules in the editor, and the Edit action sits beside Delete in the policy table. Role changes made in the policy editor are saved together when you select Save changes.
* BYOC deployments now pay 60% of SaaS rates for Agent Server and database Standard Units, which lowers those BYOC resource charges by 40%. SaaS, legacy LCU and LSU meters, database storage, and self-hosted Agent Run pricing are unchanged.
* Threshold-based model pricing is now available on BYOC data planes. Runs that exceed a model's token threshold, such as long-context input, are priced at the higher rate. Data planes on `0.18.18` or later get this pricing; check your version under **Settings** > **Data plane**.
* Dynatrace and PagerDuty alert actions now require the `workspaces:manage-secrets` permission to use a workspace secret. Dynatrace actions can only send to the exact host bound to the secret, and cross-host redirects are blocked.

## Deployment

* Deferred checkpoint deletion is now on by default for Postgres deployments. Thread delete and prune accept `sync_checkpoint_delete=true` to remove checkpoint data before the request returns.
* Runs that hit the stream size limit now send a gap event in place of the dropped event, so your client knows it missed an update instead of silently keeping the previous state.
* Run streams now end with an `end` event that reports the run's final status: `success`, `error`, `timeout`, `interrupted`, or `rollback` for a stateless run. If a stream closes without an `end` or `error` event, get the run to see how it ended.
* Run streams on the standard routes accept `lifecycle`, which sends an event when each subagent starts and ends, with the id of the tool call that started it. Tool events on these routes now arrive in the shape the v1 React hook parses.
* Run streams accept a repeatable `namespace` query parameter, so you can stream one conversation: the main agent's (`namespace=`) or one subagent's (`namespace=tools:<task_id>`). The stream drops the events of subagents that conversation starts. Without the parameter, streams are unchanged.
* Thread streams now announce which interrupts a run answers, so other open tabs hide them without a reload. v1 thread streams get an `interrupts` event, and Protocol v2 clients get `input.answered` on the `input` channel.
* Runs that resume an interrupt now accept `strict_resume: true` on run creation and on the Protocol v2 `input.respond` and `run.start` commands. A resume that answers an interrupt that is not waiting fails with `UnknownInterruptError` and leaves the thread unchanged. Python graphs need langgraph 1.2.20, which `/info` reports as `strict_resume`; JS graphs need @langchain/langgraph 1.7.0.
* Single-run cancel requests now accept `reason=taken` to mark input absorbed for steering, so you can tell that interruption apart from an ordinary cancellation. For thread-scoped cancellations, the recorded `cancel_reason` also includes the ID of the run that was active on the thread.
* Thread state endpoints now accept a `select` parameter, so you can return only the fields you need, such as `values.messages`, instead of the full state. On Postgres-backed servers, selected reads also skip loading the state you did not ask for.
* JS graphs with an output schema now stream only their output keys in `values` and `updates`, and `/runs/wait` returns only those keys. Runs that include the `events` stream mode now stream the same `values` and `updates` as runs without it.
* BYOC data planes that build images in their own cluster now accept GitHub repositories as deployment sources. Builds run as Jobs in your cluster, with build logs in the UI, and GitHub deployments are sized with `resource_spec` like Docker image deployments.
* GitHub outcomes for coding agents now work on BYOC deployments. Agents link GitHub through the workspace's Engine GitHub App installation, with no separate OAuth step.
* Scale-to-zero dev deployments are now available on AWS. New dev deployments scale to zero when idle and wake on the next request. The create page shows the Serverless option and scaling settings on AWS when your organization has scale-to-zero enabled.
* Azure BYOC data planes can now be created in 19 regions, up from 4, including Canada, Europe, the UK, India, Japan, Korea, Southeast Asia, and Australia. You can also add up to 14 customer tags to the Azure resources of a data plane, and the create data plane form now works on Azure with the Entra tenant ID, resource group ID, and VNet CIDR fields.
* Azure BYOC data planes now reach Blob storage and Key Vault only through private endpoints in the private link subnet, and storage accounts no longer accept public network access. The private link subnet, set by `privateLinkSubnetCidr`, must now be /28 or larger, and your customer role needs the `Microsoft.Storage/storageAccounts/PrivateEndpointConnectionsApproval/action`, `privateEndpointConnections/write`, and `privateEndpointConnections/delete` permissions.
* Data planes on Google Cloud can now be created from the Data Planes page, with Google Cloud region, project ID, provisioner service account, VPC network CIDR, and load balancer access fields. Each data plane in the list and in the data plane pickers now shows its cloud logo.
* Your GCP BYOC data plane now sends VPC Flow Logs for every subnet to Cloud Logging in your project, recording all flows aggregated over 10 minutes. The GKE cluster also enforces your project's Binary Authorization policy on pod images. A project without a policy allows every image, so existing workloads are not blocked.
* AWS data planes now deny S3 requests made over TLS versions below 1.2 for their blob, SmithDB, ClickHouse backup, sandbox snapshot, and VPC flow-log buckets.
* BYOC workspaces now show a connecting screen while your browser checks the data plane, instead of a half-loaded app. If a data plane is unreachable, the outage screen appears at once on your next visit in the same tab, and the app rechecks automatically every 30 seconds until the data plane recovers. The workspace switcher also shows a status dot beside each BYOC data plane so you can spot an outage before you switch.
* Deployment metrics now reject a `step` below 60 seconds, so `GET /v2/deployments/{id}/metrics` returns a 400 error for a smaller `step` and `step_seconds` values below 60 fail validation. Metrics are sampled every 30 to 60 seconds, so smaller steps return gaps rather than finer data.
* Analytics for an agent's deployment now includes a **Deployments** section with API Server, Workers, Postgres, and Redis charts. The **Monitoring** tab is hidden on deployments bound to an agent environment, and their alert settings now appear at the bottom of **Overview**.
* Agent Servers with both a license key and a LangSmith Cloud API key now authenticate with the API key first and fall back to the license key if that check fails. Agent Servers that authenticate against LangSmith Cloud with an org-scoped or multi-workspace API key now fail at startup, so set `LANGSMITH_CONTROL_PLANE_API_KEY` to a key scoped to a single workspace.
* New GCP BYOC data planes run their system nodes on N2 machine types, `n2-standard-4` by default, instead of E2. Existing data planes keep their current system pool.
* In multi-process mode, the `/metrics` endpoint now exposes `lg_api_run_failed_terminal_counter_total`, labeled by `error_category`, which counts runs that fail without retry. It also exposes `lg_api_sweep_failed_counter_total`, which counts sweeper iterations that fail to reclaim abandoned runs.
* Managed Deep Agents channels can now receive Slack edits, deletions, reactions, and changes to a channel itself, such as creation, rename, or archive, as `provider_event` deliveries. Choose them with `forwarded_events` on the channel, and edits and deletions arrive only in threads the channel already follows.
* Agents can now run in the background on Slack channels without a status indicator or Stop button on each message. Set `show_progress` to `false` on the event to keep replies, errors, and interrupts while hiding the thinking status and progress updates.
* Managed Deep Agent traces from GitHub-backed deployments now include the exact source commit as `revision_id`, so you can tie each trace to the code that ran. Explicit `LANGSMITH_REVISION_ID` and `LANGCHAIN_REVISION_ID` values you set still take precedence.
* Agent deployments can now assume roles in AWS, Azure, and Google Cloud with LangSmith workload identity, so you no longer need to store cloud keys as deployment secrets. Set `LANGSMITH_AWS_ROLE_ARN` for AWS, `LANGSMITH_AZURE_CLIENT_ID` and `LANGSMITH_AZURE_TENANT_ID` for Azure, or `LANGSMITH_GCP_WORKLOAD_IDENTITY_PROVIDER` for Google Cloud, and trust only the exact agent subject in that cloud.
* Deployments can now exchange their API key for an agent badge, a signed token valid for five minutes that names the agent bound to the deployment, at `POST /v1/agent-auth/token`. Personal API keys are refused.
* Agent responses now include `agent_uuid`, the agent's permanent identifier. Use it as the subject when you write workload identity trust policies, since `id` can be reused after an agent is deleted.

## Datasets and experiments

* Bulk example metadata update is now available in the Python, JavaScript, Java, and Go SDKs and the CLI through **update-metadata**. You can change metadata on many dataset examples at once, including moving examples into and out of dataset splits. Examples that are not in the dataset are reported as NOT\_FOUND.
* You can now list datasets with `GET /api/v2/datasets`. Each page returns `items` and a `next_cursor` that is null on the last page. Pass `next_cursor` as `cursor` to get the next page, and use `sort_order` to choose ascending or descending order.
* The `PUT /api/v1/datasets/{dataset_id}/splits` endpoint is deprecated and will be removed after May 31, 2027. Use the bulk example metadata update instead, with an `ARRAY_ADD` or `ARRAY_REMOVE` operation on the `dataset_split` key. Responses now include `Deprecation`, `Sunset`, and `Link` headers that point to the successor.
* Update parameters for datasets and annotation queues are now plain typed fields in the Go, Python, Java, and TypeScript SDKs, which breaks Go SDK code that used the old update types. The CLI `datasets update` command now takes `--transformation`, and the old `--transformations` flag still works.
* You can now choose a row height for experiment results tables: **Default**, **Tall**, or **Fit** to show each cell's full content. Your choice is remembered in your browser and carried in shared links. The control is unavailable in compact mode.

## Evaluators

* You can now create decision model evaluators with providers that use your own API key, such as OpenAI, without the LLM Gateway. Options that only run through the LLM Gateway, such as SemIf and ScaleDown, remain hidden until the gateway is enabled.
* Decision-model evaluators can now judge whole threads. Set `group_by` to `thread_id` on decision-model rules to evaluate each thread once it goes idle, instead of each run. Thread rules require `session_id`.
* Evaluators that use OpenAI models can now pick a **Flex** service tier in the evaluator form. Flex evaluator calls wait up to 10 minutes for a score, and each call is attempted once.
* Evaluators now accept an optional `metadata` JSON object on create, get, list, and update, and you can filter the evaluator list by `metadata` to find evaluators with matching values. Set `metadata` to null on update to clear it.
* Evaluator endpoints now return errors as RFC 7807 problem details with `application/problem+json`. Each error message appears in both `detail` and the deprecated `error` field, and status codes are unchanged.
* New OpenAI LLM-as-a-judge evaluators now start on `gpt-6-luna` instead of `gpt-6.1-sol`. Workspace default presets are unchanged.
* List run rules now returns one page at a time. Pass `page_size` and `cursor` to step through results, and use `next_cursor` from each response to fetch the next page.
* Coding agent overview now shows a Work type card that breaks down your agent's threads by the kind of work each one asks for: feature, bugfix, refactor, question answering, review, or off topic. The card shows each type's share, thread count, and cost, and it guides you through adding the Coding Work Type evaluator if you have not set it up yet. The Coding Work Type evaluator is available now as a prebuilt template that labels each coding-agent thread from its first message, and it requires a `TYPESAFE_API_KEY` secret in your workspace.

## Feedback

* You can now add or remove categories on a categorical feedback config with a PATCH to `/feedback-configs`, using `add_categories` and `remove_categories`, without re-sending the whole list. Retried edits are safe, and the Python and JavaScript SDKs expose the change as `add_feedback_categories` and `remove_feedback_categories`.
* Multi-select rubric tags in annotation queue CSV exports now list every category a reviewer picked for a run in one cell, separated by `; `, instead of showing only the most recent pick. Repeated picks from several reviewers appear once.
* Custom apps can now keep their current view in the URL through `window.langsmith.setRoute`, so links, refreshes, and Back and Forward return to the same view. Apps can also open external `https://` links with `window.langsmith.openUrl` and save files with `window.langsmith.download`, and the viewer confirms each one first.
* Annotation queue custom views now show each run's image attachments inline, so you can label product photos without opening the run. Images from other remote sources still do not load.

## Gateway

* You can now call Groq and Mistral chat completions through the LLM Gateway at `/groq/v1/chat/completions` and `/mistral/v1/chat/completions`, with usage and spend tracked for each call. Add `groq` or `mistral` to your Model Access policy to allow these routes.
* Saved model configs for DeepSeek, Groq, Mistral, Azure OpenAI, Anthropic on Vertex AI, and Databricks now run through `custom/<configName>`. DeepSeek, Groq, and Mistral requests always go to each provider's own API, so a saved base URL is ignored.
* Fallback triggers in the fallback chain form are now grouped by error type, such as rate limits and overload, server errors, and request timeouts. Select a group to enable all of its status codes, or click individual codes to fine-tune them. Time to first output is now a single field, and leaving it blank turns the timeout off.
* Kimi K3 replaces Kimi K2.6 in the gateway model list, Gateway Credits model access, the Playground Fireworks dropdown, and Managed Deep Agents model selection. Kimi K2.6 is no longer offered, because Fireworks has retired it.
* Spend caps can now count Anthropic OAuth usage. Turn on **Count Anthropic OAuth spend** in a spend cap's **Subscription settings (optional)** to include OAuth requests in the cap and in the Usage tab. Leave it off for flat-rate subscriptions.
* You can now set a spend limit that splits by a custom header for one API key, user, workspace, or organization, so each value of that header gets its own limit for only that subject. Select one subject in the spend-limit form and check **Separate limits by custom header** to create it.
* The LLM auth proxy now sends your IdP token only when your org has an Allowed URLs list, and it no longer sends the LLM auth proxy JWT on a redirect to a host outside that list. Requests to orgs set to **Allow all** or **Block all** no longer include the IdP token.
* Tool kits now appear on the Tools page for every workspace. Client setup for connected MCP servers is now on tool kits.
* Kit tools are now visible before you connect a server: tools/list shows the linked tools each missing credential unlocks, and calling one returns 428 with a connect link until the credential is connected.
* Tool kit refresh now returns 200 when a linked server needs a credential, and the response lists each missing credential with its verification URL in `missing_credentials`.
* Workspace admins can now store one credential for a header-based MCP server that every caller in the workspace uses. Setting it with `PUT /v1/managed-tools/servers/{id}/credential?credential_owner_type=workspace&credential_owner_id=<workspace ID>` permanently deletes every other owner's credential on that server, and calls without a usable workspace credential return a 409 that asks a workspace admin to fix it.
* Agents can now hold their own tool credentials. Admins connect credentials for an agent environment, and calls made with the agent's bound API key use them. Deleting an agent environment also deletes its credentials.

## Sandboxes

* Narrow AWS and GCP proxy rules with `match_hosts`, so hosts outside the list are no longer intercepted or authenticated. Presigned AWS URLs and GCS signed URLs now pass through unchanged on reads, so downloads from third-party signed links work again.
* Browser sandboxes are now available to every SaaS workspace as a beta, without requesting access. Browsers created with `POST /v2/sandboxes/browsers` are deleted 14 days after they stop by default, and you can set `delete_after_stop_seconds` to change that delay or to `0` to keep a stopped browser.
* You can now set `persistent` in the TypeScript SDK when you call `SandboxClient.createSandbox`. Pass `false` to turn off filesystem persistence for a sandbox, or leave it out to keep the server default.
* BYOC operators on AWS can set `sandboxes.juicefs.redisAuth` to `iam` when they create a data plane, so sandbox JuiceFS metadata connects to Redis with IAM authentication instead of a password secret. The setting cannot change after the data plane is created.

## Engine

* Engine is now available on Azure and GCP BYOC data planes. Turn it on with `spec.langsmith.engine.enabled`. On Azure, Engine calls Azure AI Foundry with workload identity, so no API key is needed. On GCP, Engine calls Claude through Vertex AI with workload identity. Engine requires sandboxes.
* Creating an issue with the option to have Engine generate a pull request now opens the PR when its fix run finishes. You need the `issues:update` permission on the project to use this option; Engine agents cannot use it.
* Engine now @mentions a coding agent's Slack bot under each new issue when you set one on a Slack destination, and the agent fields are available to every workspace.
* Issue charts now mark the pull requests that caused an issue and the ones that fixed it, with a chip on each marker line. Hover or click a chip to see each PR's title, link, and merge time.
* Applying a proposed context fix from the Engine issue page now requires a signed-in user with write access to the target Context Hub repo. Engine runs can still create and delete proposals, but they can no longer apply them to Context Hub.

## Prompts and playground

* You can now set a model's extra header value to a workspace secret in the Playground, so gateway credentials such as an `api-key` stay encrypted instead of being stored in plain text in the model config. Use the key icon in the header row to switch a value to a secret name.
* Prompt Hub repos and commits are now available in the TypeScript and Python SDKs. Use `client.repos` to manage repos and their directories, and `client.commits` to create, retrieve, and list commits.

## Fixes and improvements

> [accordion] Show all fixes
>
> * Fixed an issue where `PUT /store/items` ignored your store's `default_ttl` when the request omitted `ttl`. Items now expire after the configured default, and authorization handlers receive that default before the write so they can change or disable it.
> * Run details now show the `priority` and `priority_cache_read` token and cost breakdowns for OpenAI priority runs, which were missing before.
> * Runs created with `on_disconnect` set to `cancel` now stop when a client disconnects before the stream response arrives, instead of running to completion.
> * JS graphs no longer stream the tokens of model calls tagged `langsmith:nostream` in legacy `messages` mode. Those calls now stay out of your `messages/partial` and `messages/metadata` events, matching `nostream`.
> * Fixed an issue where string values that contain the text `\u0000`, such as generated HTML or JavaScript, came back with `\ufffd` in place of that text in state, streams, and stored threads. Actual NUL characters still become `\ufffd`, and the text now survives unchanged.
> * The Worker Job Stats chart now shows the true peak of concurrent jobs for each time range. Max Jobs and Active Jobs no longer grow inflated when you widen the time range.
> * Feedback that arrives after an evaluation finishes now appears in the comparison header averages, the evaluation progress, and the grid rows without a page reload.
> * Deleting a thread now also drops its cached stream events, so a thread re-created under the same id no longer replays the deleted thread's events when you join its stream with `Last-Event-ID`.
> * Fixed an issue where adding or removing a plan for an organization left plan-gated routes returning 403 "no plan found" for up to 60 seconds. Plan changes now take effect right away, and agents load as soon as a plan is attached.
> * VPC associations that you add to a BYOC private ingress zone are no longer removed during reconciliation, so they stay in place until decommissioning, and `additionalVpcAssociations` now lists only the VPCs you configure.
> * Online Evaluators no longer lists rules that Insights creates for itself, so you no longer see an "Evaluator not found" error when you open Insights. Your own evaluators and spend charts remain unchanged.
> * Scans now continue when the error or baseline query fails, as long as other queries returned traces. The run records a gap for the failed slice instead of aborting, and a retry over the newer half of the window that succeeds is logged as narrowed.
> * Resumable run streams no longer send an event twice when a Redis timeout or connection reset makes the server retry the publish.
> * Runs and thread streams that Redis cuts now reconnect in the SDKs and resume from the last event, instead of being reported as failed. Streams that stop reading for 30 seconds also end and reconnect.
> * `GET /v2/runs/{run_id}` now returns the run when `start_time` is omitted, instead of returning 501 Not Implemented. Single-run reads with permission filters also work without `start_time`.
> * Uploading an empty CSV, a CSV with only a header row, or a CSV that lacks the requested input or output column now returns a 400 error with a clear message instead of a 500 error.
> * Creating a BYOC data plane no longer fails with a 500 error when your organization sets a maximum service key expiry. The data plane's agents key is now exempt from that policy, and creation succeeds.
> * Snapshot captures of overlay sandboxes with deep layer stacks no longer fail with deadline exceeded. The capture request now gets 20 minutes, so large sandboxes finish in a single request. Failed captures no longer stay pending.
> * Custom output renderers now appear in annotation queues that have custom output rendering turned on. Queues without a saved **Classic Trace View** setting now open in the classic view by default.
> * Runs no longer fail on their first execution when your priority callback returns a `fairness_weight` key. The server ignores that key and logs a warning, and the run uses `priority` and `fairness_group`.

**October 26-November 2, 2026**

## Highlights

* **Granular workspace administration permissions**: You can now delegate workspace administration by action instead of granting the broad `workspaces:manage` permission. New permissions cover settings, retention, usage controls, security policy, resource tags, integrations, sandbox proxy profiles, credentials, restricted role assignment, and workspace deletion, and the UI shows controls based on the permissions a role holds. Existing custom roles with `workspaces:manage` receive the new permissions automatically and keep their current access, and the built-in Workspace Admin role includes them. [Learn more](../../Govern/Users%20%26%20access%20control/Role-based%20access%20control.md).
* **Organization custom roles for delegated administration**: You can now create custom roles scoped to your organization and assign them to members, pending invitations, and service account keys. Organization roles let you delegate granular administration without granting Admin or Operator. Custom organization roles cannot include legacy `organization:manage`, access-control management, authentication management, or Teams management permissions, and they are restricted by default. Members with `organization:members:manage` can invite or assign unrestricted roles, while restricted roles require `organization:access-control:manage`. [Learn more](../../Govern/Users%20%26%20access%20control/Role-based%20access%20control.md).
* **Prioritize runs with a priority callback**: You can add a `priority` section to `langgraph.json` that names a callback, and it sets each thread's priority from -5 to 5 at its first run. When every worker is busy, runs at lower levels start first, and runs at the same level start oldest first. Runs return `priority`, threads return `run_priority` and `fairness_group`, and the metrics report queue depth and wait time per level. Ordering applies when your deployment uses Redis, and removing the `priority` section turns levels off. The callback needs langgraph-sdk 0.4.9 and langgraph-cli 0.4.38 or later. [Learn more](../../../Deploy/Deploy%20to%20Self-hosted/Configure/Configure%20Agent%20Server%20for%20scale.md).
* **Human-in-the-loop prompts over MCP**: MCP clients on revision 2026-07-28 that support form elicitation are now asked for input when a graph pauses, and the tool call resumes with the answers. Text questions, interrupts with a `response_schema`, form and URL questions relayed from MCP tools, and LangChain human-in-the-loop reviews to approve, edit, reject, or answer are all supported. Clients that do not declare the required elicitation capability receive a missing-capability error, `-32021`, that names what to enable. [Learn more](../../../Deploy/Agent%20Server/Capabilities/Human-in-the-loop%20over%20MCP.md).
* **Review queued runs in their trajectory**: Run items in annotation queues now open in the run's trajectory, scrolled to the turn being graded, so reviewers read the conversation the way it appears in tracing instead of raw inputs and outputs. Messages use the same parser as the trace page, so provider-native content such as Anthropic `tool_use` blocks renders correctly. Child runs, and runs with no trajectory, show their inputs and outputs in conversation order, with each tool call folded into one row. The new view is read-only. To edit a run's inputs and outputs before you add it to a dataset, turn on **Classic Trace View** in the queue's data formatting settings. [Learn more](../../../Test/Annotation%20Queues/Use%20annotation%20queues.md#data-formatting).
* **Custom views for annotation queues**: You can now replace the default trace view in an annotation queue's middle pane with a custom view that you describe to LangSmith Chat, such as a chat transcript without tool calls. Chat previews each draft on the current queue item, and nothing is saved until you click **Save**. One view can serve several queues, and reviewers switch between the default and custom views with the **Custom view** toggle. A custom view is display only and cannot call the LangSmith API. Custom views succeed custom output rendering, which will be deprecated. [Learn more](../../../Test/Annotation%20Queues/Build%20custom%20views%20for%20annotation%20queues.md).

## Tracing

* Multipart and OTel batch ingestion now enforce all short-term usage limits, so your traces over an events-per-minute, hourly request, or hourly bytes limit get a 429 response. Batch requests to `/runs/batch` now count toward those limits as well.
* Default ingest limits for new and existing tenants are now 300,000 events per minute, 1,000,000 tracing requests per hour, and 15 GB of tracing payloads per hour. Tenants that still use the previous defaults are moved to the new limits, while customized values stay as they are.
* You can now stream v2 run, thread, and trace queries from the Python, JavaScript, Go, and Java SDKs, and from the CLI. Use the new `streaming` methods with `ai_search` to get results as Server-Sent Events.
* Run queries now return subtree totals for token and cost fields on root and intermediate runs. Parent runs in your run tables show usage that includes their descendant runs. Descendant usage counts even when a filter or time range excludes those descendants from the results.
* Agent Server and tracing integrations now accept an agent `address` in place of a project name, so you can send root runs for the Claude Agent SDK, Google ADK, OpenAI Agents SDK, OpenAI Realtime, and Gemini Live to an agent environment. Setting both an `address` and a project name is rejected.
* Tool Gateway can now write each tool call into your LangSmith trace as a child run under the calling run, when the request includes the `langsmith-trace` and `baggage` headers. Each run records the tool, server, kit, the identity the call acted as, outcome, and timing, but never tool arguments or results. Workspace admins can also turn on **Record tool call traces** in the new **Usage** tab on the Tools page, which lists recent tool calls and opens each one's trace.
* Tracing for OpenAI's hosted Agents API is now available in beta through `wrap_openai`: each finished session turn appears in LangSmith as a trace with one run per model call, tool call, and subagent, and each session is one thread. Turns started inside a `@traceable` function nest under that run.
* The `POST /api/v1/runs/group` endpoint is now deprecated and will be sunset on January 31, 2027. Use `POST /api/v2/threads/query` to query threads instead. The endpoint continues to work until then.
* The Python SDK now shows deprecation warnings for `list_runs()`, `read_run()`, and other methods that will be removed on January 31, 2027, when you call them from your own app code. To hide them, pass `-W ignore::DeprecationWarning` to Python.
* Your AI search parse requests are now rate limited per source IP at 25 requests per minute, and excess requests receive HTTP 429. Rotating `x-api-key` or `x-user-id` headers no longer resets this limit.
* Your `POST /api/v1/sessions` and `PATCH /api/v1/sessions/{session_id}` responses now return the complete session, including `last_run_start_time`, the same fields as a default GET. The Python SDK's `sessions.create()` and `sessions.update()` return a `TracerSession`, and the TypeScript SDK's `sessions.update()` returns the deprecated `TracerSessionWithoutVirtualFields`.
* You can now store your API key as a reference instead of in plaintext: `langsmith profiles create` accepts `--api-key-env` to read the key from an environment variable, or `--api-key-cmd` to run a command such as a password manager lookup, and the CLI and Go SDK resolve it each time the profile is used. The Python SDK reads `api_key_env` profiles too, while the JS and Java SDKs do the same but do not yet run `api_key_cmd`.
* You can now choose which `langsmith auth login` profile and config file the SDK uses, with the new `profile` and `profileConfigPath` options in JavaScript and `profile` and `profile_config_path` options in Python. Set `preferProfileAuth` or `prefer_profile_auth` to use that login even when `LANGSMITH_API_KEY` is set, with the profile's endpoint and workspace. Clients that do not set these options behave as before.
* Write replicas on another instance no longer receive your base workspace ID, which fixes 403 errors on every write. Each `LANGSMITH_RUNS_ENDPOINTS` entry can now set its own `workspace_id`, which is sent as that replica's tenant for org-scoped keys.
* Alerts for an agent now show across all of its environments, and you can filter them by environment. When you create an alert, the agent and environment are prefilled, and the alert form shows which agent the alert belongs to. You can also switch the agent from the alert form.
* Agents now show the custom avatar you upload for them everywhere they appear in the app, including the agent switcher, tables, simulations, search results, and the agent overview header.
* The LangSmith CLI no longer offers an `--accept` flag on any generated command, including `sessions dashboard`, `threads query`, `traces query`, and `public:runs` commands. Before this change, passing `--accept text/event-stream` printed nothing and exited with status 0.
* Commands that take a project now accept `--project` with a project name, so you no longer need the project's UUID. If `LANGSMITH_PROJECT` is set, commands that require a project use it when you do not pass one, and `--session-id` and positional IDs still take precedence.
* Selecting a day in the date-time range calendar now covers the full day, from midnight through 23:59:59. If the end day is today, the range ends at the current time instead.
* Bulk exports now accept v2 filter syntax, such as `run_type:llm`, on SmithDB-backed deployments. Filters are checked when you create the export, so an invalid filter returns a 400 error with the reason.

## Evaluators

* You can now create a decision-model evaluator in one API call, choosing Jev, SemIf, OpenAI Decisions, a TypeSafe-compatible endpoint, or a saved model configuration. Each question becomes a feedback key on the project or dataset you attach it to.
* New evaluators start with **Trace Evaluator Runs** turned off, so their runs are not traced unless you turn it on. Existing evaluators keep their current setting.
* LLM-as-judge evaluators now return a 400 error when you save them with a prompt that has no model or no output schema, including when you reuse an existing evaluator. Each run no longer fails with a raw langchain\_core error, and the message tells you to select a model or add an output schema, such as `score: bool`.
* Thread evaluators now let you set Compacted from a gear on the trajectory preview, so your evaluator can grade a compacted trajectory without a separate picker option. The variable stays named `trajectory`, and a Custom badge marks it when compaction is on.
* You can now list evaluators, get a single evaluator by ID, and list run rules from MCP clients. Evaluator lists omit code, which you can read with `get_evaluator`. Run rule responses mask webhook header values and alert routing keys, and show only the host of each webhook URL.
* You can now search evaluator templates by name, description, type, or category in the Configure Evaluator picker and the empty state on the Evaluators page. Matching templates appear as you type, and a Clear search button restores the full gallery when nothing matches.
* You can now bulk-delete online evaluators from the LangSmith CLI with `langsmith online-evaluators bulk-delete`, passing one `--evaluator-id` per evaluator. The command asks you to confirm before it deletes, and `--yes` skips the prompt.

## Datasets and experiments

* JavaScript evaluations now accept an `uploadRuns` option, either a boolean or a function that receives each example, so you can choose which runs upload while every result stays available locally and to summary evaluators.
* You can now download CSV exports with each cell on a single line by choosing the single-line option in the dataset format selector or the experiment download dialog. Line breaks in cells appear as literal `\n` and `\r`, and the default CSV download still keeps original multiline cell values.
* You can now cap a taskset run's model spend with a monthly spend limit, and cancel a run that is queued, preparing, or running with a new cancellation endpoint. Trials that finish after a run's last progress check are now recorded when the run times out or is cancelled, instead of being marked not run. Capped runs on self-hosted instances are rejected with a 400 error.

## Feedback

* Annotation queue review now uses three column headers, so you can move between items with the arrow keys and find **View all**, item navigation, and reviewer actions in one place. Press V to close the item pane and open it again, and hover over buttons to see their shortcuts. Requeue is no longer available for any queue type.
* The annotation queue sidebar now shows each run's name, a preview of its inputs, and its relative start time, with threads marked by a chat icon and their first user message as the preview. Each row also shows the first eight characters of its run ID on a second line, so reviewers can tell apart runs that share a name.
* Annotation queues have a new **Show reviewer notes to other reviewers** setting under **Collaborator Settings**. When it is on, your review pane lists other reviewers' notes on each run as read-only entries with their names. It is off by default, so queues keep blind reviews unless you turn it on.
* Rubric items in annotation queues can now be required or hidden based on the answers to earlier items, using the new `required_if` and `visible_if` fields. A rule can only reference an item that comes before it in the rubric, and omitting either field keeps its stored value.
* The Add feedback picker on runs now lists keys with human feedback in the current project first, under **Recently used in this project**, and removes the dashed suggestion chips from the Feedback section.

## Prompts and playground

* New Anthropic and Anthropic-compatible model configurations start with a max output tokens default of `8192` instead of `1024`, and resetting the max output tokens field restores `8192` for Anthropic configurations. Existing saved configurations and explicit token limits are unchanged.
* The deprecated LangServe provider no longer appears in the provider picker in Playground, evaluators, or saved model configurations. Your existing LangServe configurations keep working, and automatic default model selection no longer chooses LangServe.
* You can now select GPT-6.1 Terra from the OpenAI model dropdown in Playground, model configurations, and Model Access suggestions by choosing `gpt-6.1-terra`.
* Prompt Hub errors for the `langsmith` CLI now follow RFC 7807 problem details, with `application/problem+json` bodies on commit endpoints and per-field messages in `errors` for `422` responses from the repos endpoints. Deleting a repo that does not exist now returns `200` instead of `404`, so retrying a delete is safe.
* You can now page through long commit histories and repo lists with `page_size` and `cursor`, using the `next_cursor` value from each response until it is `null`.
* LangSmith Chat's docs tool now searches and reads official LangChain and LangSmith documentation directly from docs.langchain.com, so it no longer depends on a Chat LangChain deployment and returns the source text for LangSmith Chat to answer from.
* LangSmith Chat can now find your Tool Gateway kits and their tools' input schemas, so it can write calls from custom apps to services like Google, Slack, and your own APIs. LangSmith Chat lists the kits you can use, and for a kit it lists each tool with its input schema and any services you have not connected yet.
* LangSmith Chat now opens a fresh chat in each new browser tab and window instead of resuming the conversation from your previous session. Past conversations remain available in the thread history.

## Deployment

* Creating a Azure data plane now requires the direct role assignments for LangSmith in the resource group to use your organization's external ID as their description. Creation fails with a 403 error, `azure_external_id_mismatch`, when they do not. Reapply the LangSmith BYOC Terraform module with your external ID before creating a new data plane, and deleting an existing data plane still works without it.
* You can now supply your own security groups for the AWS EKS cluster, Postgres, SmithDB metastore, Redis, and the ingress NLB through `spec.vpc.byoVpcSecurityGroupIds`, with 1–5 IDs per role. Crossplane then creates no security groups or rules for those roles, which helps accounts that deny `CreateSecurityGroup` and `Revoke*`. You can also set `karpenter.amiId` once to apply to every node class that does not set its own `amiId`.
* GCP data planes now take per-service image versions under `spec.langsmith.images`, the same way AWS and Azure data planes do. Rollouts of LangSmith images to GCP data planes now move every service to the new release tag, and third-party images keep their own tags.
* Bring-your-own-cloud (BYOC) Azure data planes can now reach a private AKS cluster API through a private endpoint on the cluster, without access to the AKS node resource group. Your cluster does not need an API Server VNet Integration subnet, and you no longer need to create the **private-link** subnet's delegation. Azure requires the approval of the endpoint, which LangSmith requests automatically.
* Azure BYOC clusters now run database pods on dedicated node pools, and SmithDB query, ingestion, and compaction workers cache data on local NVMe disks. New metastores default to PostgreSQL 18. Your system pool stays at three fixed nodes by default.
* Azure BYOC teardown now keeps your resource group, Key Vault, and trace and SmithDB Blob storage. Teardown deletes the AKS cluster, PostgreSQL, Redis, sandbox storage, network resources, and private DNS.
* Your BYOC Azure data plane creation now checks regional and VM-family vCPU quota for the system node pool before it starts, and it stops with an error if the quota is insufficient. The check also enables PostgreSQL zone-redundant high availability only when the selected region and size support it across two zones, and otherwise creates a single server.
* New BYOC data planes on Azure now start with three fixed `Standard_D2s_v6` system nodes, each with 2 vCPU and 8 GiB of memory, to match the AWS system node group. Existing data planes keep their current system node size.
* Self-hosted and BYOC system nodes that use a custom launch template now require IMDSv2 and always encrypt the node volume. Existing node groups that use a custom launch template roll to the new template version.
* Internal and public load balancers in AWS BYOC deployments now expose only HTTPS on port `443`. Monitoring that calls the load balancer directly on port `15021` must use a different path, because health checks still reach gateway pods on that port.
* New GCP and Azure data planes stay on the Crossplane composition revision that matches their **module-version**, so applying a new Crossplane release no longer moves them. Existing GCP data planes need a one-time update to the same selector before GCP releases apply on merge.
* Redis Cluster deployments that connect with **REDIS\_DATABASE\_URI** now take TLS from the URI scheme: use `rediss://` to enable TLS, the same as standalone Redis. The `REDIS_CLUSTER_USE_SSL_CONNECTION` setting now applies only when the cluster is seeded from `REDIS_CLUSTER_DATABASE_URIS`. Self-hosted Helm chart users who set `redis.external.cluster.tlsEnabled` with `connectionUrl` should switch to `rediss://`, since `nodeUris`, `password`, and `tlsEnabled` are deprecated in Helm chart v0.18 and supported through v0.19.
* On LangSmith Azure, `langgraph deploy --remote` now uploads your source tarball and builds it for you, and `langgraph deploy` now builds and pushes your image locally. Older LangGraph CLIs get a message asking you to upgrade before either command works.
* Deployment logs and build logs now load for deployments on Azure LSD. Previously the Logs tab returned an error there. Build logs also show for Azure builds, including builds that already ran.
* Azure deployment creation now shows the GitHub connection and repository picker instead of a plain repository URL field.
* Azure deployments now collect compute and database usage every five minutes and report hourly totals for billing. Usage from before `2026-10-27T00:00:00Z` is not reported.
* Managed Deep Agents is now available on GCP and Azure BYOC data planes when Fleet is enabled. Agent revisions, deployment workers, Trigger Server, and Agent Auth OAuth callbacks now reach your data-plane endpoint, and trigger and channel APIs are exposed at both the direct and chart-derived paths.
* Deployments that push images with `internal_docker` now store their image repository in the deployment's workload region, so images pushed from the CLI land next to the deployment. Existing deployments move to the regional repository the next time you request a push token or start a build.
* When webhooks are disabled with `http.disable_webhooks`, your runs and crons no longer resolve or store the `webhook` URL you send, and a cron PATCH whose only field is `webhook` returns a 422 saying webhooks are disabled.
* Run attempts and drains are now stored in Postgres, so your runs no longer lose their retry count when Redis restarts or drops counters between retries. During rollout, active runs might run for more than the allocated number of retries on failure.
* Metrics requests for deployments that omit `step` now pick a step that returns about 60 points per series, with a minimum of 60 seconds. For example, a 30-day query no longer fails with a 502 error, and a 7-day query returns 10080-second intervals instead of a point per minute.
* Deployments now set `LANGSMITH_ENDPOINT` to the same value as `LANGCHAIN_ENDPOINT`, so app code that reads only `LANGSMITH_ENDPOINT` sends traces to the correct region. You can now set `LANGSMITH_ENDPOINT` on Cloud SaaS deployments, and a value you set yourself still takes precedence over the default.
* Studio now shows a wrench icon and tool count on each ToolNode in the graph, with a hover card listing every tool the node runs. While tools run, a badge beside the node names them, for Python and JS agents.
* Agent Server images and user graph dependencies now accept redis-py 8.x, so your graphs can install redis-py 8 without a version conflict.
* Runs now include a `langgraph_graph_load_ms` value in their metadata, showing how long your graph took to load. You can filter on it in LangSmith traces to find slow graph loads. For prebuilt graphs that are not created by a factory, the value is close to 0.
* You can set `systemNodeGroup.releaseVersion` in your BYOC AWS configuration to move EKS-selected system nodes to a patched AMI release. System nodes now also follow the cluster's Kubernetes version, so they upgrade after the control plane during an EKS upgrade.
* Bring-your-own-VPC data planes on AWS can now place databases in your app subnets. Set `byovpc.private_db_subnet_ids` to the same IDs as `byovpc.private_app_subnet_ids` if your VPC has no dedicated database subnets. Public subnets must still be distinct from the other tiers.
* GCP data planes now allow up to 512 vCPUs and 2048 GB of memory for automatically provisioned nodes, up from 96 vCPUs and 384 GB. Rolling updates on a full LangSmith install no longer fail with a Pending pods error caused by the old cap.
* Newly provisioned AWS BYOC data planes now start their backend and listener services with larger default CPU and memory allocations. Existing data planes keep their configured resources.
* GCP BYOC data planes on the US control plane can now run in **us-west1**. Customers can select this region when they create a data plane.
* Self-hosted data planes can now run scale to zero deployments with `dev_zero` and `dev_free_zero` when your administrator enables the setting. Deployments created from an image without `deployment_type` still stay non-zero.
* Your agent can now load Google Sheets through LangSmith Tool Gateway once your workspace has Gateway enabled and Google Sheets allowed. The agent reads spreadsheets directly, and every Sheets edit, such as writing ranges, adding sheets, or creating charts, waits for your approval before it runs. Connecting Sheets starts Google sign-in only when you ask for it.
* The thread storage endpoint, `GET /threads/{id}/storage`, now returns storage usage for threads on SQLite deployments, matching Postgres.

## Engine

* Removing an Engine evidence trace from an issue can now be undone. Click Undo in the "Trace removed from issue" toast, or on the greyed card itself, to put the trace back on the issue with its original reason. Undoing a removal also takes its rejection back out of the issue's history, so Engine does not treat the removal as a correction.
* Engine now records the feedback keys it cites for each issue trace, and the issue detail lists those keys with their trace counts. Clicking a key opens the newest trace that cites it. Linking a run to an issue through the API now returns the stored link, including any `triggering_feedback_keys`.
* Engine is now off by default for BYOC data planes until you enable it on each data plane; an unset Engine setting no longer inherits your LangSmith Cloud setting, and existing explicit choices are unchanged.
* Engine can now call model gateways behind LangSmith's LLM auth proxy without a static API key. Set `ENGINE_GATEWAY_AUTH=llm_auth_proxy` to have each Engine run mint its own short-lived token. Setting this together with `ENGINE_GATEWAY_API_KEY_FILE` is a configuration error, and `GO_ENDPOINT` must be set explicitly.

## Gateway

* The custom **Gateway** workspace role now grants only `gateway:invoke` and `workspaces:read`. Existing service keys assigned this role lose the removed permissions when your Terraform configuration applies, so confirm that your keys do not depend on creating runs or projects, managing model prices, exporting data in bulk, or reading agent auth connections.
* You can now target LLM Gateway policies at specific Agents, at every Agent in one or more environments, or at one Agent within an environment. Spend caps, rate limits, model access, and guards apply to the Agents you select in a workspace. Set the **workspace\_id** matcher with **agent\_id** and/or **agent\_environment** matchers, using `LOCAL`, `DEVELOPMENT`, `STAGING`, or `PRODUCTION` for the environment.
* Saved max-token and reasoning-effort defaults on your model configurations now apply to gateway requests, so requests that omit these settings use the values you saved. Explicit values in a request still take precedence over saved defaults.
* Gateway usage reports now show input, output, and total token counts alongside spend, with exact counts available on hover, so you can reconcile gateway usage with your tracing projects. Cached token share also appears for model breakdowns.
* You can now call a second Azure resource in your workspace by writing its name in the model field as `<resource>/<deployment>`, such as `ai-gateway-uat-eastus2/gpt-5.4`. Each resource uses its own API key, stored as a workspace secret named `AZURE_FOUNDRY_API_KEY_<RESOURCE>`, and requests for an unknown resource return a 400 that names the secret to add. Existing `azure/<deployment>` models work as before.
* You can now turn on model cooldown in the **Advanced** section of fallback chains. When a model fails the number of times you set, your gateway skips it for the cooldown period you choose, and the last model in the chain is always tried.
* Gateway traces now record whether an agent was verified by an agent badge or by its API key, in the new `gateway.agent_proven_by` metadata field. Badge checks are off until you set `AGENT_AUTH_BADGE_PUBLIC_JWKS`, and gateway policies can match on the `agent_proven_by` field.
* The workspace MCP servers list now shows ten servers per page with pagination controls below it, so **Built-in tools** stay near the top of the page.
* The BigQuery tool server now includes `bigquery_query_read_only`, which runs one read-only GoogleSQL SELECT query. Nested SELECTs, CTEs, joins, and unions are supported. Multi-statement scripts and write statements are rejected before they run.
* Tool kits now have a search mode for agents with many tools. Add `?mode=search` to a kit's MCP URL, and `tools/list` returns three tools: `search_tools` finds matching tools, `get_tool` returns one tool's definition, and `call_tool` runs a tool after checking its arguments against the schema. Calling a tool directly by name still works, and the default `full` mode is unchanged.

## Sandboxes

* Sandbox usage now shows CPU (vCPU-hours), memory (GiB-hours), and storage (GiB-hours) in place of dollar estimates, with daily charts grouped by workspace or resource, Top Resources ranked by any of the three metrics, and CSV export of individual resources. Storage totals now keep recorded measurements when some hourly samples are missing, and days with no storage measurements appear as gaps.
* Non-persistent sandboxes are now available to all tenants. Set `persistent` to `false` when you create a sandbox to get a disposable sandbox whose writes are discarded on stop. Creates that omit `persistent` remain persistent, and combining `persistent: false` with `preserve_memory_on_stop` or snapshot capture is still rejected.
* Sandbox proxy rules can now rewrite HTTPS requests to a different destination with a `rewrite` rule. Set `host` to send matching requests to an HTTPS destination, or `sandbox` with `port` to send them to another sandbox in your workspace over an existing sandbox link. Use `credentials` to choose whether incoming credential headers are stripped (the default), redacted, or kept.
* Proxy-backed AWS role rules now accept `session_tags`, so your role's policy can scope each sandbox with `${aws:PrincipalTag/...}` without hitting the 2,048-character session policy limit as you add mounts. Tags are fixed at create, and your role's trust policy must allow `sts:TagSession` for the LangSmith principal.
* Batch deleting sandboxes now skips any sandbox outside your editing scope, reporting it as `sandbox not found` instead of deleting it. Sandboxes you can edit are still deleted.
* Sandbox memory history on the Metrics tab now reports guest RAM, so an overlay sandbox that reads its shared base no longer shows memory above its configured limit. Memory history recorded before the host upgrade for overlay sandboxes is cleared.
* Sandboxes are now available on new Azure BYOC data planes. Sandboxes run on dedicated nodes with their own workload identity, and your data plane stores sandbox files in its own Blob storage.
* Command history is now available in sandboxes in the EU, APAC, and AWS production regions. Your sandboxes capture command history, and the authenticated history endpoints return it for list, detail, and output reads.
* The Go SDK now runs commands in a sandbox without a shell through the new `Argv` field on `Run`, and the `Timeout` field now sets the timeout you request instead of falling back to the server default.
* Self-hosted LangSmith installs now show a banner to organization admins and operators when the sandbox runtime falls behind or runs ahead of the control plane's release, or when sandbox hosts stop reporting, and the banner names the setting to change.
* Sandbox browsers are available in beta. A browser is a sandbox that runs one persistent Chrome, which you keep logged in to your sites and lend to your agents. Each attached sandbox drives its own window over the Chrome DevTools Protocol, and you can watch every window in LangSmith, take one over to log in or enter details, and hand it back. Logins survive restarts. Manage browsers through the `/v2/sandboxes/browsers` API or the Go SDK, and connect clients outside a sandbox, such as Playwright on your laptop, through each attachment's `api_cdp_url`. [Learn more](../../../Deploy/Sandboxes/LangSmith%20Sandboxes.md).

## Administration

* Organization members with custom roles can no longer demote, remove, rename, or reset the password of Organization Admins or Operators. Only Organization Admins can manage Organization Admins, and Admins and Operators can manage Operators and reset other users' basic-auth passwords.
* You can now assign Organization Viewer or Organization Restricted to workspace-scoped service keys when you create or edit them. Workspace access stays limited to the workspaces you select.
* Callers without the rules:update permission now see run rule webhook header values masked as \*\*\*\*\*\*\*\* instead of the real credentials, and saving a masked value back to a rule returns a 400 error instead of overwriting the stored secret.
* Admins can now restrict specific tag keys on new datasets, projects, experiments, prompts, and sandboxes with ABAC deny policies on the tag-on-create permissions. Editors can still apply all other tags when they create these resources. Creating a sandbox with tags now requires the sandboxes:tag-on-create permission instead of workspaces:resource-tags:manage, so Editors and deployment-runtime keys can tag sandboxes at create unless a deny policy restricts the key.
* You can now delete access policies from the policy table after typing the full policy name to confirm, and the policy stays in place with the error shown if the deletion fails. You can also add roles when you create a policy, and attach or remove roles from an existing policy's details.
* You can now retrieve the list of resource and permission pairs that access policies support, so you can build policy editors that offer only valid choices. Only organization managers with the ABAC entitlement can call the new `/api/v1/platform/orgs/current/access-policies/catalog` endpoint.
* Teams are now available in the public LangSmith REST API, with 17 operations for managing teams, members, workspace grants, and access policy attachments. Enabled organizations no longer need a rollout override for the Teams settings pages.
* Workspace picker groups workspaces under their dataplane name and region, with LangSmith Cloud workspaces in a separate group. Search matches dataplane names and regions as well as workspace names and IDs.
* Organization members with `organization:read` can now select a data plane in workspace pickers without infrastructure read access. The picker shows only the data planes and workspaces you can access, and it still falls back to the full list on older backends.
* Model price tiers can now be defined by context length: your workspace can set a `prompt_tokens_above` threshold on a model price through `/api/v1/model-price-map`, and tiers are priced by their threshold alongside the standard row.
* Org admins can now upload a CSV of email addresses when inviting members, and the invite form shows a clear alert with the number to remove when your list goes over your remaining seats or the 500-invite limit.
* Paid organizations without a card on file now see a "No payment method on file" message and a **Set up billing** button on the billing page. Adding a card keeps your current plan, and Developer organizations no longer see a "Remove payment method" action when there is no card to remove.
* Agents connected through the remote MCP server can now create, update, and delete custom model prices, and filter the model price list by `provider`, so you can price models at your own negotiated rates.
* You can now retrieve, rename, and delete workspaces from the LangSmith CLI with `langsmith workspaces retrieve`, `langsmith workspaces update`, and `langsmith workspaces delete`, using the `--id` flag for the workspace ID. Delete still asks for confirmation before it runs.
* Custom app editor now discards undeployed changes when you leave edit mode: reopening the editor loads the latest deployed version of your app, and the exit dialog says so.

## Fixes and improvements

> [accordion] Show all fixes
>
> * Workspace switching is available again in the collapsed sidebar in LangSmith and Fleet, so you can change workspaces without expanding navigation.
> * Agent list requests no longer fail with a 500 timeout after a few pages of results on self-hosted installs without PgBouncer. Requests to `GET /api/v1/agents` now return within normal response times for tenants with many Agents.
> * Online evaluator previews now show the full trace by default when you add an evaluator from a tracing project. Before, a template card could open the preview on a single inner step, and the evaluator test graded that step. New evaluators now start with the **top-level traces only** filter.
> * Engine retries a failed repository clone once before giving up. If the retry also fails, your scan reports the connected repository as unavailable this run instead of treating it as disconnected, and run metadata lists the failed repository URLs.
> * Experiment batches no longer re-send their request after a timeout, rate limit, server error, or lost connection, so runs and model calls are not duplicated. Errors that occur after a batch starts now stop further retries and are reported as failures.
> * Fixes Playwright's browser driver and other subprocesses started from worker threads failing to launch on LangSmith Deployments. Subprocesses now start normally from your deployment's worker threads.
> * Tool calls that retry after you decline or cancel a Tool Gateway connection now return an error that names the servers you did not connect, instead of asking you to connect the same account again.
> * Creating a sandbox from a snapshot whose layers overflowed Firecracker's pmem window failed with "Cannot create pmem device" and a 500 error. Layered captures now squash the lineage before the window overflows, and creates from snapshots that cannot boot on any host are refused with a 422 error that reports the snapshot's size.
> * Invitation links that show as expired after SSO sign-in now offer **Switch sign-in method** or **Switch account**, which signs you out and returns you to the invitation so you can sign in with the invited email.
> * Failed root runs in thread Details now show their error status and error preview instead of appearing as successful.
> * Code evaluators that return `0` or `False` now record that score as feedback instead of dropping it. Evaluators that return an unusable value now show an error explaining why, instead of leaving the run with no score.
> * Prompt webhook deliveries for tag creates and updates now send `created_at` as an RFC 3339 UTC timestamp, such as `2026-10-19T14:35:00Z`. Receivers that parse timestamps strictly no longer reject these deliveries.
> * Engine scans on large projects no longer abort when a latency, token, or cost p99 query times out. The scan completes with the error and baseline traces, and the agent is told which outlier stratum is missing.
> * Deployment pages no longer stay on a loading state indefinitely when a deployment stops responding. The **Assistants** and **Threads** tables now time out after 30 seconds, show **Deployment not responding**, and keep retrying until the deployment answers.
> * Your first Gateway Credits purchase after upgrading a free organization to developer no longer fails with "Your organization is not set up to purchase Gateway Credits." The dialog waits for the upgrade to apply, shows a "Finishing your upgrade" banner, and completes the purchase on its own.
> * Snapshots now become ready and gain their tag in the same step, so a box created by name:tag right after a snapshot shows ready no longer returns a 404 `snapshot "<name>:<tag>" not found` error. A build whose tag is refused by the naming rules now fails at once and is not retried.
> * Onboarding emails and invite emails with the LangSmith logo now send again. Previously, they failed to send and left the logo missing.
> * Files passed as `attachments` on `updateRun` or on a `RunTree` patch are now stored with the run in the JavaScript SDK, instead of being silently dropped.
> * Evaluator tables now show the spend limit that applies to each LLM rule, including the organization's default weekly limit once the rule has made its first evaluator call. Rules without a limit of their own no longer show N/A under **Weekly Limit** and **Percent of Spend Limit** on the evaluator page and in a project's **Evaluators** tab. Rules that never call an evaluator model, such as code evaluators, still show N/A. The `effective_spend_limit` field is returned on rule responses.
> * Connecting a GitLab token and the scheduled token rotation now work on instances that cap token lifetimes below a year. Rotation steps down through 180, 90, 60, 30, 14, 7, and 2 days and keeps the longest lifetime your instance accepts. Tokens that were previously stuck failing every 15 minutes after a cap was lowered now rotate on the next sweep.

**October 19-26, 2026**

## Highlights

* **New sidebar for all workspaces**: The new sidebar now appears in every workspace and replaces the old sidebar. The organization and workspace menu at the top of the sidebar replaces the LangSmith wordmark and product switcher, so you switch organizations and workspaces from one place. The custom wordmark logo no longer appears in the sidebar; upload a custom organization avatar to brand it. [Learn more](../../Overview/Agent-based%20workspaces/Navigate%20agents.md).
* **Create examples with reference\_outputs**: The API and the Python, JavaScript, Go, and Java SDKs now use `reference_outputs` to set the expected outputs when you create examples, including in bulk. `outputs` still works as a deprecated alias, but sending both `reference_outputs` and `outputs` in the same request is rejected. Existing code keeps working, and responses, updates, and multipart uploads still use `outputs`. [Learn more](../../../Test/Datasets%20%26%20Experiments/Datasets/Create%20a%20dataset/How%20to%20create%20and%20manage%20datasets%20programmatically.md).
* **Store rejects ambiguous namespace labels**: Store operations from your graphs now reject namespace labels that are empty or contain `.`, the same rule the HTTP store API already applies. Previously a label such as `"tenant.bob"` addressed the same items as the namespace `("tenant", "bob")`, so graph code that built namespaces from untrusted input could read, overwrite, or delete another namespace's items. Such calls now return an invalid input error, and the fix is also in Agent Server 0.16.2 and 0.15.5. [Learn more](../../../Deploy/Get%20started/Reference/Agent%20Server%20changelog.md).
* **Organization-wide bulk export creation limits**: LangSmith Cloud now limits bulk export creation across all workspaces in an organization, in addition to the existing per-workspace limits: 1,000 creates per hour and 1,000 active schedules per organization by default. When an organization exceeds a limit, `create_bulk_export` returns a 429 response, with a `Retry-After` header for the hourly limit. Exports that existing schedules create automatically do not count toward the hourly total, so running schedules are never blocked. [Learn more](../../../Monitor/Debug/Bulk%20export%20trace%20data/Bulk%20export%20trace%20data.md).

## Tracing

* The `langsmith` CLI now includes `threads query`, `threads stats`, `threads aggregate-stats`, `threads share`, `traces query`, `runs create`, `runs ingest-batch`, `runs get-url`, `runs share`, `public runs retrieve`, and `public runs query`, so you can search threads and traces, write runs, and share them without calling the API directly.
* Filtered run trees now have a **Full tree** or **Matches only** switch below the active filters, so you can keep the full trace hierarchy visible with matching runs highlighted. Matches only remains the default.
* Your trace tooltips and thread summaries now show a **Cache hit rate** based on cache-read tokens as a share of input tokens, and the thread summary displays it as a percentage. Cache hit rate appears as 0% when your model reports zero cache reads, and it is hidden when the usage is not reported.
* Trajectory now keeps your reading position in the URL: reloading or sharing a thread link opens Messages at the turn and run you were reading, and a Back to trajectory button on Details returns you to that message.
* Bulk export partitions no longer fail within minutes when the trace store is busy. A rejected partition now waits and runs again for up to 2 hours without using up its retries.
* You can now open the **Share** menu on a run and choose **Copy URL** to copy the link to the current view without making the run public.
* You can now filter traces by when their feedback was modified by passing `min_feedback_modified_at` and `max_feedback_modified_at` to `POST /v2/traces/query`, the same feedback window that `/v2/runs/query` already supports. The bounds apply to the feedback conditions in `trace_filter` or `tree_filter`, so each request must include at least one feedback condition, such as `eq(feedback_key, "correctness")`.
* You can now request up to 10 sum, avg, min, max, or percentile aggregates over token and cost fields in one call to `/v2/runs/analytics` by sending a `metrics` array instead of `metric`, so you no longer need to run the same query once per metric.
* The LangSmith MCP `query_runs` and `fetch_runs` tools now return `app_path` by default, so agents can link directly to the canonical run page in the LangSmith UI instead of building trace URLs from run IDs.
* You can now drag table column headers to reorder columns, and the order is saved per table in each browser. Hover or focus a header to reveal a grip to its left, or use **Move left** and **Move right** in the column menu.
* Global search now lets you search across all agents with the new **Filter by current agent** toggle in the search footer, and sandboxes are included when filtering by agent.
* Agent registry CRUD is now available in the Go, Java, JavaScript, and Python SDKs, so you can create, retrieve, list, update, and delete agents with typed objects and the `client.agents` service.
* Creating an agent with the Python, JavaScript, Go, or Java SDK no longer requires `source_type`; when omitted, it now defaults to `EXTERNAL`, so your endpoint-hosted agent is registered without extra configuration.
* You can require explicit agent creation for tracing in your workspace, so traces and tracing projects no longer create agents implicitly; send traces only to agents you register with `POST /api/v1/agents`. Workspace admins can turn this on with the `require_explicit_agent_creation_for_tracing` field in the workspace settings API, and requests that would create an agent from a trace are rejected with a 403 error.
* Agents now record an owner: new agents are assigned to the user who creates them, and the owner appears in the **Owner** column of the All Agents table and on the agent overview page. Workspace managers can change an owner from the agent actions menu, and the `owner_id` field on `PATCH /api/v1/agents/{agent_id}` sets or clears it.

## Prompts and playground

* LangSmith Chat's model picker now offers Sonnet 5.5, Opus 5.5, GPT-6.1 Sol, GPT-6 Luna, and Gemini 3.8 Flash, and Sonnet 5.5 is the default for new chats. Sonnet 5, Haiku 4.5, and GPT-5.6 Terra have been removed from the picker, and your saved model configurations keep working.

## Feedback

* Feedback can now record the ID of the feedback config it was written against through the new `feedback_config_id` field, and the server rejects IDs that do not belong to the same feedback key in your workspace.
* You can now read, edit, and delete run feedback, create and update feedback tokens, and delete feedback configs from the `langsmith` CLI with `langsmith feedback retrieve`, `langsmith feedback update`, `langsmith feedback delete`, `langsmith feedback tokens create`, `langsmith feedback tokens update`, and `langsmith feedback configs delete`. The deprecated `langsmith feedback "<note>"` alias is removed, so use `langsmith report` to submit a note and `langsmith feedback` to manage existing feedback.
* Creating a feedback tag now refuses a key that is already used in the same place, such as a queue rubric, the queue review view, or a run's feedback, with the message "This feedback tag is already used here." Queues also cannot be saved with a rubric that lists the same key twice.
* You can create a key's enforced feedback config from the JS and Python SDKs with `isEnforced` or `is_enforced`, which requires the `feedback-configs:manage-enforced` permission that workspace admins have. Creating a config no longer changes a key's score direction unless you pass `isLowerScoreBetter` or `is_lower_score_better`.
* Feedback created with a `traceId` through the JS SDK is now batched with your runs and sent in the background, so `createFeedback` returns immediately. Call `awaitPendingTraceBatches()` to wait for delivery; feedback with `extendTraceRetention: false` still posts directly to `/feedback`.

## Datasets and experiments

* The `langsmith` CLI now includes commands for comparative experiments, dataset sharing, splits, cloning, and version tagging. Run `langsmith datasets retrieve-version` to read a version by time or tag, `langsmith datasets versions retrieve-diff` to compare two versions, and `langsmith datasets update-tags` to move a tag to a version.
* You can now list examples with only the fields you select by passing `exclude_default_fields=true` to `GET /api/v1/examples`, combined with `select`, so that `select=id` returns only example IDs without inputs or other default fields. The default response is unchanged when the flag is omitted. The Python, JavaScript, and Go SDKs expose this through `list_examples`, `listExamples`, and `ExampleListParams`.

## Evaluators

* Trajectory evaluators can now grade a shortened version of each conversation. Turn on the **Compacted** switch under the trajectory source in the evaluator editor, and the evaluator receives the shortened messages both when it runs and when you test it.
* Your TypeSafe and TypeSafe-compatible evaluators can now send extra request headers, such as `TypeSafe-Danger-Zone-Long-Context`, from the **Extra Headers** field in the model configuration. Long threads that previously hit the context limit can now be scored with the beta long-context option enabled.
* Sandbox evaluator **Test** results now show the full evaluator traceback in expandable error details, so you can see which evaluator function and line failed. Tracebacks over 64 KiB are shortened in the middle and marked as truncated.
* You can now create, update, and check spend for online evaluators from the `langsmith` CLI with `langsmith online-evaluators create`, `update`, and `spend`. Listing, reading, and deleting evaluators remain available through `langsmith evaluator list`, `get`, and `delete`.
* Code evaluators can now score whole threads. Select **Threads** for a code evaluator rule, turn on **Enable advanced features**, and define `evaluate(ctx)`. Set the evaluator's input to `thread`, `all_messages` (the default), `human_ai_pairs`, or `first_human_last_ai` to choose which view of the conversation it receives. Each thread gets one score. [Learn more](../../../Monitor/Observe/Online%20evaluators/Set%20up%20online%20code%20evaluators.md).

## Deployment

* Your review form now shows a decision picker for human-in-the-loop interrupts, so you choose approve, edit, reject, or respond and fill in only that decision's fields, and a single-decision interrupt no longer makes you type the decision type by hand. Per-call tool approvals in chat use the same approve, edit, reject, and respond card one tool call at a time, and long decision descriptions start cut short behind a Show more button.
* `GET` and `POST /threads/{thread_id}/history` now accept a `select` parameter that returns only the named fields of each state, such as `tasks` or `checkpoint`, or a single key of the state values like `values.messages`. Unknown fields and `values.` with no key return a 422 error, so you can request just what your client reads from each history entry.
* Studio's right-side Interact and Trace panel can now be hidden with **Hide side panel** and shown again with **Show side panel**, and it stays hidden when you switch between Graph and Chat or reload the page. Showing it restores the width you had before.
* Studio chat lists your most recently updated threads first, so a thread moves to the top when a run starts or finishes instead of staying at the bottom of the list.
* New AWS data planes created without a `trace_storage` value now store traces in SmithDB instead of ClickHouse. To keep the ClickHouse default, pass `trace_storage` set to `CLICKHOUSE` in your `POST /orgs/current/data-planes` request. Existing data planes keep their current trace storage.
* The MCP endpoint now returns HTTP 403 for requests whose `Origin` header your CORS settings do not allow, on every MCP protocol revision, which blocks DNS rebinding attacks. Loopback origins such as `http://localhost` remain allowed, so list your browser-based MCP clients' origins in `CORS_ALLOW_ORIGINS` or `CORS_CONFIG`.
* You can now stop every in-flight run on a deployment at once with the new kill switch, which is available to Workspace Admins by default and to custom roles that have the `deployments:cancel-runs` permission. Pressing Stop returns the operation's progress and keeps updating until all targeted runs have stopped, and the latest operation remains visible after a page reload.
* JS graphs can now call their own deployment with the SDK client by passing the `langgraph_api:url` context variable as `apiUrl`, including under custom auth, where the calls run as the user who started the run.
* You can now enter custom IAM role names and a custom Karpenter instance profile name when you create an AWS data plane with **Use Existing IAM Roles**, so the data plane works with the names from your BYOIAM Terraform module outputs. Set them under **Advanced settings**, and the names are only accepted when `byoiam.is_enabled` is `true`.
* Managed Deep Agents are now enabled on AWS BYOC data planes, and trigger and channel endpoints under `/api/v1/triggers` and `/api/v1/channels` are routed to the trigger server, so your channel and trigger requests reach it and agent revisions can read Context Hub through the public data-plane URL.
* Production deployments on Azure now get their own private managed PostgreSQL database, provisioned automatically with each deployment, and you can resize it when you change the database tier.
* Deployment metrics charts in the **Monitoring** tab now load on Azure deployments, showing CPU, memory, restarts, replicas, requests, latency, and run queue for your deployment. Azure metrics requests over 32 days are shortened to the last 32 days.
* Azure BYOC data planes now reach the LangSmith control plane over Azure Private Link, so your data plane sends its API and heartbeat traffic to a private endpoint inside your VNet while your applications keep the same hostnames. LangSmith approves the endpoint connection automatically, and HTTPS requests can fail or time out until approval completes.
* Your Azure BYOC Redis connections now verify the certificate hostname for cluster shards, so Redis startup no longer relies on skipping that check.
* Self-hosted installations with one database and authentication, and BYOC data planes, can now migrate existing tracing projects and experiments to Agent Platform agents automatically. The migration stays off until you set `AGENT_PLATFORM_MIGRATION_ROLLOUT_ENABLED` to `true`, and each BYOC workspace reports readiness to the control plane after it is verified.
* AWS BYOC data planes in private mode can now skip the Route53 private hosted zone and apex record by setting `spec.ingress.customerManagedDns` to `true`, which requires a BYO VPC. Point your own DNS for the ingress hostname at the internal NLB, and your data plane readiness will not wait on Route53 records.
* Self-hosted deployments on the bundled operator can now manage extra ServiceAccounts and SecretProviderClasses from the deployment settings, with a YAML/JSON editor and Secret mount paths for SecretProviderClasses.
* Thread history responses are now capped by size when `LANGGRAPH_THREAD_HISTORY_MAX_STATE_BYTES` is set: history returns the newest state and stops before the entry that would exceed the limit, so large threads no longer produce oversized responses. The variable is off by default.
* Queue workers now scale on runs that can start: the queue autoscaler counts running runs plus one pending run per thread that is due within 10 minutes and has nothing running, so runs waiting behind a running run on their thread no longer add queue pods.
* Local runs with `langgraph dev` no longer report usage to LangSmith, so they are no longer billed at the self-hosted rate. Deployments built from the published images keep reporting as before.

## Engine

* You can now connect a GitLab instance in **Settings > GitLab** with a service account token, then add GitLab projects to an Engine board alongside GitHub repositories. Scans, fixes, and merge request reviews work on GitLab projects, and merging a fix's merge request completes its issue.

## Gateway

* Model fallback chains now accept an optional `ejection` block with `failure_threshold` and `cooldown_seconds`. When a candidate fails the chain's trigger conditions the threshold number of times within the window, your gateway skips that candidate for the cooldown period and moves to the next candidate, so repeated provider failures no longer slow every request.
* You can now route requests to Deep Infra through the LLM Gateway with your workspace **DEEPINFRA\_API\_KEY**, using either Chat Completions at `/deepinfra/v1/chat/completions` or Anthropic Messages at `/deepinfra/v1/messages`, and set Deep Infra as a fallback provider.
* Your Usage tab can now break down spend by any `X-Gateway-*` header through the new **Custom Dimension** option in **Breakdown by**, which defaults to `X-Gateway-Service` and works without a spend policy. Changing the header name updates the chart and the URL, so shared links keep the same grouping.
* Requests to the LLM Gateway that authenticate with a deployment's service key, including preview deployments, now include the Agent and environment that the deployment is bound to in request metadata and gateway traces, so you can filter gateway policies and traces by agent.
* Gateway traces for a single request now share a `gateway.request.id`, and each attempt records its position in the fallback chain, the gateway overhead before its provider call, and the time spent on failed fallbacks, so you can group a request's attempts and see where its latency went.
* Gateway traces that exceed your monthly trace limit are now stored without their content instead of being rejected, and the trace metadata includes `content_quota_exceeded: true` so you can identify them.
* You can now call OpenAI Decisions models through the unified `/v1/systemone` endpoint by setting `model` to `openai/gpt-6-luna`, using OpenAI's native Decisions request and response format without translation.
* Traces for BYOK calls to Anthropic and OpenAI now include a `provider_key_hint` metadata field that shows a redacted form of your key, so you can match each trace to the key that made the call and reconcile it against vendor billing. Calls to other providers and calls to custom endpoints do not record a hint.
* You can now register a private MCP server and build a personal tool kit from it that only you can see and use. Choose **Personal** when you add an MCP server or create a tool kit, and find them on the Users tab under **Tools**.
* Workspace admins can now list every member's personal MCP servers by passing `owned_by=any` to `GET /v1/managed-tools/servers`, with each server showing its owner. Members who call it receive a 403 response.
* New tool kits default to **Use connected tools**, so a kit with servers from a profile and servers added by you returns tools from the connected servers instead of failing discovery when one credential is missing.
* Managed MCP servers and tool kits now send clients that support URL elicitation a link to connect the required credential, instead of only a 428 response that requires a retry. Clients without that support keep the existing 428 response.
* Managed tools server lists now show a `credential_status` for each server (`connected`, `needs_connect`, `needs_reconnect`, or `unavailable`), so you can tell when a server needs you to connect or reconnect and when Agent Auth is temporarily unavailable. Listing servers also makes a fixed number of Agent Auth calls regardless of how many servers are on the page, so lists load faster.
* Managed tools MCP servers no longer send your custom credential headers to a different host, port, or scheme after a redirect; cross-origin redirects now fail with a blocked-redirect error, and same-origin redirects keep working. Servers that redirect to another origin must be registered at their final origin.

## Sandboxes

* Sandboxes now live-migrate to another host when their host drains, with no per-tenant flag or per-sandbox opt-in required. Sandboxes that cannot move, such as those with role-backed S3 mounts, are still suspended. Your requests in flight at the moment the sandbox pauses can fail with a 409 `Sandbox closed the connection while the request was in flight.` error, and `extra_config.experimental.live_migration` is still accepted at create but ignored.
* Snapshots can now carry sandbox settings with the new `include` parameter on `POST /api/v2/sandboxes/boxes/{name}/snapshot`, so a sandbox created from the snapshot starts with its mounts, proxy config, env vars, resources, lifecycle timers, and labels unless the create request sets them. Capturing `mounts`, `proxy_config`, or `env_vars` that hold literal secrets requires `confirm_allow_snapshot_secret_values: true`, and access delegation is never carried.
* Service URLs and browser window links can now be embedded in an iframe on the origins you name with `embed_origins`, so your app can show a sandbox's dev server or a browser window next to its own UI. Viewers using a LangSmith login sign in from inside the frame through a popup, and token-mode links return an `embed_url` that keeps the token out of server logs.
* Redirects returned by your sandbox, such as a service URL that sends `/` to `/login`, now reach the browser unchanged and resolve against the service URL host, instead of being followed by the platform.
* Updating, starting, or stopping a sandbox now requires runtime access: the sandbox's creator, or a role with `sandboxes:exec`. Editors with only `sandboxes:update` who did not create the sandbox receive a 403 and their changes are no longer saved or pushed to the host.
* Sandboxes now allow up to 256 concurrent TCP connections per vCPU. Connections beyond the limit are closed immediately, and new connections are refused until usage drops.
* Sandbox registry listing now supports cursor pagination with `page_size` and `cursor` on `GET /api/v2/sandboxes/registries`, so you can page through registries without skipping or repeating results when registries are added or removed between requests.
* Private ECR registries now authenticate with an IAM role on BYOC AWS data planes that have sandboxes enabled. Register an ECR registry with a role ARN, then browse its repositories and build snapshots from images in that registry.
* Enabling sandboxes on an AWS data plane created before sandbox provisioning shipped now succeeds. Previously, enablement failed on these data planes.
* You can now manage sandbox registries, browsers, service URL sharing, snapshot lookups, and usage costs from the `langsmith` CLI under `langsmith sandboxes`, including `sandboxes registries update` with `--new-name` and `sandboxes browsers attachments create` with `--window-name`.
* In follow view, a browser window now holds still and pans only while your pointer rests on one of the arrow zones at its edges, so the page no longer slides with every pointer move.

## Administration

* Tracing keys now receive a 403 Forbidden on the Agent Server auth routes, the OAuth token routes, the LLM auth proxy JWT routes, and the internal alerts aggregation route, so they can no longer reach these endpoints. In multipart run ingestion, feedback sent with a tracing key is dropped while the batch's runs still ingest, and a batch containing only feedback returns 403 Forbidden.
* Tracing keys now have their own maximum expiry: admins set the **Tracing Key Maximum Expiry (days)** limit in **Settings** > **Max expiry settings**, separate from the Service key limit, and new Tracing Only keys default to and are capped by that value.
* You can now manage API keys in one streamlined table, with saved column preferences, URL-backed filters that persist when you share a link, and full-schema CSV exports that include every matching key. The Workspaces column shows the single workspace name directly, or opens a searchable list when a key spans several workspaces, and the default workspace always appears first.
* You can now edit the SAML metadata URL or XML of a configured SSO provider in **Settings** > **SSO Configuration** without deleting and recreating the configuration. The new metadata must have the same entity ID as the current configuration.
* Self-hosted deployments using **OAuth with PKCE** now show a dismissible warning to organization admins that the method is deprecated and will be removed in a future release, with a link to the migration guide for switching to OAuth with a client secret.
* Workspaces created on the new experience can now switch to the classic experience from **Settings** > **General**, and switch back again.
* The `langsmith` CLI now creates workspaces with `langsmith workspaces create`, reads workspace settings with `langsmith settings list`, reads server details with `langsmith info list`, and reads product feedback with `langsmith product-feedback retrieve`. You can also run `langsmith auth signup` to create a LangSmith account in the browser and log the CLI in to it.
* Your workspace info endpoint at `GET /v1/platform/workspaces/current/info` now returns a `dashboard_url` field with the base URL of your LangSmith dashboard, so you no longer need to derive it from the API hostname. The same field is returned from the `PATCH` response.

## Fixes and improvements

> [accordion] Show all fixes
>
> * Percentage error alerts that filter on an error message now report the correct error rate instead of 100%, and the alert preview divides matching errors by all runs in the same population.
> * Experiment comparison computed columns that show a single output field, such as `outputs.response`, now display a preview with an **Expand** button instead of the "too large to render" error when full outputs are not yet loaded.
> * Categorical feedback labels that are numbers, such as `1`, now stay selected after you pick them in an annotation queue rubric or on the run page, instead of appearing unselected after saving. Clicking the selected label again still clears it.
> * Clicking **Evaluator trace** from a feedback popover now opens the evaluator's trace with the run peeked on first load, so your trace no longer briefly shows "Something went wrong" before it appears. Evaluator traces for evaluators without an evaluator page now open under **All agents** instead of the agent picker.
> * Playground experiment batches that exceed the request timeout now return a result for every run, so completed runs keep their outputs and evaluators receive them instead of batches stalling with no result.
> * The Engine GitHub repository picker now shows repositories as each page loads, so large installations with more than 100 repositories no longer stay in the loading state until every page has arrived.
> * Fixed the Redis run queue starting two runs of one thread at the same time, so a thread's runs now run one after another. Also fixed a pending run that stayed queued until the sweep after its earlier run was cancelled or deleted; the next run now starts without waiting for the sweep.
> * Sandbox cost breakdowns now show dollar amounts for Standard Units invoices instead of Unavailable, with compute and storage priced per resource and totals that match the invoice.
> * Traces now appear for Claude calls made through Amazon Bedrock Runtime, including inference profile model IDs such as `global.anthropic.*` and `us.anthropic.*`, for both JSON and streamed responses. Each call writes a trace, spend record, and policy-violation record in the `gateway` project, as it does for direct Anthropic calls.
> * Command-click or Ctrl-click on a run in the runs table now opens the correct trace in a new tab, including in tables that show runs from multiple projects.
> * Evaluator spend under one cent now displays its real value instead of $0, so a week with $0.00026 of spend shows \$0.0003 on the spend tile, chart tooltips, and the weekly limit row, and the chart's y-axis labels show distinct sub-cent values.
> * Shared links to experiment traces now load on open instead of showing "Something went wrong" when the trace's example is far down the results table.
> * Running a two-prompt experiment from the playground on an agent-scoped URL, an annotation-queue run, or a Studio thread run no longer freezes the tab. Both prompt columns now complete.
> * Engine now links the pull request for commits that landed through a merge queue or submit queue, instead of showing (no PR) when the commit message names the PR.
> * Runs whose stream events fail to publish now finish their work instead of stopping early and being recorded as successful, timed-out runs end their stream with a `TimeoutError` error event, and resumable runs in `messages` stream mode replay their message events when rejoined with `Last-Event-ID`.
> * When an MCP server rejects your stored credential, your client now receives a LangSmith reconnect link instead of the upstream server's sign-in challenge, so you can reauthorize the connection from LangSmith.
> * Browser window links now load their live view script, so the window page no longer shows a "This page's script is missing." error and streams video in every stream mode.
> * Trace queries that time out now show a **Query timed out** error with guidance to narrow the time range or simplify filters, instead of **No runs found**. Partial results still appear with a prompt to narrow your time range.
> * Expanded sections in the dataset example side panel now update to the selected example when you switch between examples, so every part of the panel matches the example you selected.
> * Playground now returns a 502 status with the provider's message when a model provider fails with a 5xx error, instead of a generic 500 that looked like a LangSmith failure. Retry the request to see if the provider has recovered.

**October 12-19, 2026**

## Highlights

* **Tracing-only API keys**: You can now create tracing-only API keys scoped to one or more workspaces, so applications can send traces without being granted broader access. Create keys from the new **Tracing Only** option, then list and revoke them from the **Tracing** tab in organization settings or through the `/orgs/current/tracing-keys` API. Tracing keys can only write runs and create projects, so a leaked key cannot read data or change other resources. [Learn more](../../Account/Create%20an%20account%20and%20API%20key.md#tracing-keys).
* **ScaleDown provider in LLM Gateway**: You can now call ScaleDown operations (summarize, extract, classify, compress) and its Decisions model through the LLM Gateway. Use the native `/scaledown` routes, unified `/v1/chat/completions`, or `/v1/systemone`, and runs are traced and priced as ScaleDown. You can also name ScaleDown in model access policies, save it as a model configuration, and use it as a fallback candidate. [Learn more](../../../LLM%20Gateway/Call%20the%20gateway/Direct%20model%20access.md).
* **Create BYOC data planes on GCP**: You can now create and delete BYOC data planes in your own GCP project with `POST /orgs/current/data-planes`, passing `cloud` as GCP along with `gcp_project_id`, `provisioner_service_account`, `region`, and `vpc_cidr`. GCP data planes run Cloud SQL Postgres in high availability by default, and you can set a two-hour weekly `maintenance_window` in the data plane settings. GCP BYOC is available on the US control plane for organizations with BYOC enabled. Creating a GCP data plane is API-only for now. [Learn more](../../BYOC/Bring%20Your%20Own%20Cloud%20%28BYOC%29.md).

## Administration

* The **Settings** > **Webhooks** page now pages through all webhooks, filters by type and feature, and offers a **Send test event** action for every feature. The Destinations and Configurations tables now show every row, not only the first 25.
* Engine access is now split into separate permissions: `organization:engine:read` to view Engine configuration and access requests, `organization:engine:manage` to turn Engine on or off and manage managed evaluation consent, and `organization:usage-controls:manage` to change spend limits and pause or resume runs. Organization Admins and Operators keep their existing access, and users with only spending permission see project labels and spending controls without full project configuration.
* You can now create and delete organization-wide teams from **Settings** > **Organization Teams**. Creating a team opens a dialog for its name and description, and deleting one asks you to type the team's name first. Both actions require organization team management permission, and the buttons are disabled with a tooltip when you lack it. Workspace teams are now created and removed only by granting or revoking an organization team's access to a workspace, so each grant always has exactly one workspace team that starts with no members or policies.
* IdP-synced teams now pick up members from SCIM groups and SSO group claims whose names match the team's IdP group name, so a user who belongs to a matching group joins the team and keeps its workspace access without an organization role.
* Workspace secrets can now be assigned allowed hosts: the secrets list can include each secret's hosts, and the new per-key `PUT /current/secrets/{key}` and `DELETE /current/secrets/{key}` endpoints let you create, update, and remove a secret along with its hosts. You can also view and edit a secret's allowed hosts and header on the workspace secrets page, and set them when adding a provider secret.
* Webhook destinations now report a delivery status in the API. A destination whose endpoint fails three times in a row is marked `FAILING` with a reason, such as `URL_NOT_FOUND` or `AUTH_FAILED`, and returns to `HEALTHY` after a successful delivery.
* Organization creation is now consistent between the **Settings** organization picker and the organization menu in the footer. Creating a new organization is disabled for SAML SSO sessions and when the instance disables organization creation, and it no longer requires management permission in the current organization.
* Agent Auth can now create a GitHub App owned by an agent from the App's manifest, or bring an existing GitHub App by its App ID and private key, and then install it through a session on the app's connection. Agents can read an app's GitHub status, change its webhook URL, and delete it, which also uninstalls it from every account where it is installed.
* Self-hosted and BYOC installations can now configure their own Slack App from organization settings, with credentials scoped to each data plane and Slack notifications available in BYOC data planes.
* Device activation now shows the name, logo, and links of the app requesting the code before you approve it, and preselects the organization and default workspace you picked last time. Select **Change** to open a searchable picker for either.
* Webhook destinations that have failed on every delivery for more than 24 hours now receive each event once, without retries. A destination resumes retries after its next successful delivery.
* You can now create as many Context Hub webhooks as you need in a workspace; the per-workspace limit no longer applies, and the Context Hub page no longer shows a webhook count. The Prompt Hub webhook limit is unchanged.
* You can now filter the **Settings** > **Model pricing** list by provider and sort it by start date, and both settings stay in the page URL so you can share or bookmark a filtered view.
* Startup program customers on the Plus plan now move to the October 2026 Startup plans and keep their current term. The Plus plan now lists its workspace limit as "Up to 3 workspaces" on the pricing, Members, and upgrade pages.

## Engine

* Close an issue as Done, Not Important, or Incorrectly Flagged from the new **Close** menu, and a banner under the header shows how it was closed. Done reopens if the issue recurs, while Not Important and Incorrectly Flagged stay closed. The **Incorrectly Flagged** filter is now **Dismissed**.
* Installation administrators can now configure one Engine GitHub App for their self-hosted or BYOC deployment from **Settings**, without editing deployment environment variables. Repository connections, sign-in, and webhooks use the configured App, and replacing or deleting it takes effect immediately.
* Every active Engine issue now offers a coding-agent handoff right away, with no seven-day wait, and boards with a connected repository keep the PR button as the primary action.
* Fix pull requests that Engine opens on your GitHub repositories are now ready for review instead of drafts, so the CI and review workflows in your repository run on them as usual. The **Open a pull request for every fix** setting in **Issue boards** now uses this behavior.
* Issue charts now mark when each fix's pull request merged, drawing a dashed line labeled PR #N on the recurrence and metric charts, so you can see whether recurrences stopped after a fix. An issue whose description names the pull request that introduced it also gets a red marker on both charts, and its chart start moves back to that merge when the gap is no wider than the traces' span.

## Gateway

* Azure Foundry models can now be used with an Entra ID service principal (tenant ID, client ID, and client secret workspace secrets) instead of an API key, so organizations that disable API keys on their Azure resources can use the gateway. An existing `AZURE_FOUNDRY_API_KEY` still takes precedence when set.
* Gateway requests that send a conversation or prompt cache key in the body but no session header now get tagged with that key as their session, so traces from OpenAI, LangChain, and Vercel AI SDK clients no longer show an empty thread.
* You can now edit a custom model configuration from its card in the LLM Gateway playground by selecting the sliders button on the card, without selecting the model first. The card updates right after you save.
* Gateway policy names in simulator block errors are now links that open the matching policy row in the gateway settings, with the row highlighted, so you can jump straight to the policy that blocked a request.
* TypeSafe-compatible configurations can now use an endpoint URL exactly as entered, without LangSmith appending `/v1/systemone`. Clear the **Append /v1/systemone** checkbox in the model configuration to use this mode; authentication remains Bearer-only.
* Gemini 4 Argon is now available in the Playground and in gateway model configurations for Google AI and Vertex AI, and TypeSafe gateway configurations now include the `jev-1.14.0` model alongside `jev-latest` and `jev-preview`.
* Responses from configured custom models and fallback models now report the model that actually served the request, so model pricing reflects the underlying provider model instead of the custom alias.
* You can now add an Anthropic Compatible Endpoint in the Gateway and Playground by entering a full endpoint URL, model name, and workspace API key. Requests are sent to the exact URL you enter, and Anthropic subscription credentials are never forwarded to it.
* Each row in the Model Fallbacks table now has an **Open in Simulator** link that opens the Simulator with the chain's primary model preselected, so you can run the fallback chain right away. Aliases and models that are no longer available open the Simulator with nothing selected.

## Sandboxes

* Writable S3 mounts can now encrypt uploads with a customer-managed KMS key by setting `encryption.kms_key` to a KMS key ARN in the mount's region. Uploads to buckets whose default encryption is SSE-KMS also persist now, instead of being deleted after the write succeeds.
* Sandbox command history is now enabled in APAC, EU, and US GCP production regions, so you can view retained stdout and stderr from sandbox commands, including after a Box has stopped.
* Sandboxes can now authenticate to AWS, GCP, and Azure with short-lived workload identity instead of static keys: set `aws.role_arn`, `gcp.workload_identity_provider`, or an `azure` proxy rule with `tenant_id` and `client_id`, and the egress proxy adds the cloud credentials to requests so the sandbox never holds them. Azure Blob Storage is also available as an `azure_blob` mount type.
* Running sandboxes can now be live-migrated off a draining host with a pause of only tens of milliseconds, instead of being suspended and woken on another host.
* Sandboxes on BYOC data planes no longer stop together when their host runs out of memory. Sandboxes can now use the full node. Existing BYOC data planes keep their current limits until their configuration is updated.
* Sandboxes are now available to Azure production organizations, letting you create, run, stop, resume, and delete sandboxes and open their service URLs at `*.azure.smithbox.dev`. Sandbox compute and storage usage is reported for billing.

## Tracing

* The All agents page now shows agents in a sortable table with Name, Most Recent Run, Created At, Trace Count, Total Cost, Error Rate, latency, tokens, and Agent ID columns; Trace Count, Total Cost, and Total Tokens now sum across all environments, and a new "About these metrics" tooltip explains which columns use the most recently active environment.
* You can now send OpenTelemetry traces to an Agent environment instead of a project by setting the `Langsmith-Agent-Id` and `Langsmith-Agent-Environment` headers. Span attributes such as `gen_ai.agent.name` do not address traces, so existing exports keep going to their project. The Go tracer also reads the `LANGSMITH_AGENT_ID` and `LANGSMITH_AGENT_ENVIRONMENT` variables, and the Java exporter accepts an address through its builder.
* Runs and traces queries in the API now accept `min_feedback_modified_at` and `max_feedback_modified_at` to filter by when feedback was last modified, as long as the query includes a feedback condition. Requests that use these bounds on a deployment that cannot apply them return a 501 error instead of ignoring the bounds.
* Trace messages now include each LLM call's prompt cache breakdown in group metadata, so you can see per call whether the prompt was read from cache or written to it, including the cache TTL, under `token_usage.input_token_details` and `cost.prompt_cost_details`.
* Long filter queries can now wrap across multiple lines. A new **Wrap filters** button appears when a query overflows the filter bar, and your choice is remembered for each project and run details view. Wrapping is off by default.
* You can now rank grouped metric results by total cost by setting `rank_groups_by` to `total_cost`, so when a query returns more groups than `limit`, the groups with the highest cost are kept. The default is still run count. This option works with **name**, **run type**, **tag**, and **metadata** group-bys, and is not supported with **project** or **feedback** group-bys.
* Cached input tokens from OpenTelemetry GenAI spans now count at the cache rates instead of the full input rate. Spans sent with the dotted keys `gen_ai.usage.cache_read.input_tokens` and `gen_ai.usage.cache_write.input_tokens` are now read, and reasoning tokens sent as `gen_ai.usage.reasoning.output_tokens` are now recorded.
* Dashboard ratio KPI charts now include a **Display as percentage** option, so a value such as 0.16 runs per feedback can appear as 16%. Decimal display remains the default, and your choice is saved when you edit the chart.
* You can now sort the Agents list by `name`, `last_run_start_time`, or `created_at` in ascending or descending order with the `sort_by` and `sort_order` query parameters on `GET /api/v1/agents`. Agent responses also include a `created_at` timestamp.
* You can now rename an agent from the **Agent settings** menu on the agent overview page, and the new name appears in the agent details and agent list right away.
* You can now start a new agent from a Build / Connect menu: **+ Agent**, the agent switcher's **+**, and the **Create new agent** tile all open the same menu, with Build (Without code, With code) and Connect (Trace an existing agent) choices.

## Datasets and experiments

* The annotation queue and dataset pickers now list every queue and dataset in your workspace, not just those matching your agent scope, and load more as you scroll. After you add tracing runs, threads, or examples to a queue or dataset from a picker, that queue or dataset is tagged to your current agent so it appears there next time.

## Deployment

* MCP tool results are now returned as valid JSON instead of Python repr() text, failed runs include the full error message, and a tool that pauses for human input returns an explicit error instead of looking like a success.
* Azure data planes can now be created and deleted from the API on Azure control planes. Creating an Azure data plane takes a resource group ID and an Entra tenant ID, and returns 202 while the reconciler applies the data plane. Deleting an Azure data plane also works while it is still provisioning.
* The MCP endpoint now accepts clients on MCP revision 2026-07-28, which send their protocol version and capabilities with each request and discover the server with **server/discover**.
* A2A SendMessage now honors non-blocking configuration: setting `configuration.returnImmediately` to `true` (or the legacy `blocking` to `false`) returns the new task right away with its submitted or working state, so you can poll it with GetTask until it completes. Blocking remains the default, and non-boolean flag values are rejected with an invalid params error.
* Deployment runtime keys now mint with a new `DEPLOYMENT_RUNTIME` role, which has Editor permissions plus gateway, sandbox, and agent-auth-credentials:use access, instead of workspace admin. Agent Auth credential reads from deployments with user-owned connections now work without granting `workspaces:manage`. Keys created before this change keep their existing permissions.
* Local image builds with `langgraph deploy` now work on LangSmith AWS deployments once your administrator configures the push role. Pushes go to a separate per-deployment ECR repository. This requires a newer LangGraph CLI, and the server tells older clients to upgrade.
* Renaming a tracing project that a deployment sends traces to now returns a 409 error, so deployment traces stay in one project. Rename the project only after you detach or redeploy the deployment.
* Serverless M and L deployments now run a single replica, matching the Serverless S tier, so the replica count shown in the plan summary is the count your deployment actually uses.
* You can now create an AWS data plane that stores and queries runs in SmithDB only, without ClickHouse. Set `trace_storage` to `SMITHDB` when you call `POST /orgs/current/data-planes`; the default remains `CLICKHOUSE`. Existing data planes keep ClickHouse, and turning it off on an existing data plane is not yet supported.
* Self-hosted deployments can now set the CPU autoscaling target as a percentage of the container's CPU limit, turn off CPU scaling or the CPU limit for the api-server and queue, and configure scale-up and scale-down behavior for autoscalers, in the container spec editor and the API.
* Subagent calls in the Studio chat tab now show a live card with the subagent's name, task, status, and the tool it is currently running, and expanding a call shows the subagent's conversation before its arguments and result.
* Runs now ignore a `cron_id` sent in `config.configurable`, `context`, or `checkpoint`, so only runs fired by a cron carry a `cron_id`.
* You can now deploy a Managed Deep Agent from a GitHub repository. Point the deployment form at a project directory with `agent.py`, `agent.ts`, or `agent.tsx` at its root, and LangSmith checks the entrypoint before it queues a build. The deployment page shows channel authorization links and any warnings from syncing the agent's schedules and channels.

## Evaluators

* Code evaluators can now use workspace secrets: select a secret in the advanced features panel and the sandbox proxy sends its header to the hosts allowed for that secret, so the secret value never enters the evaluator code. Saving fails with a clear error when a secret has no allowed hosts, has no header, or cannot be used under your organization's restricted egress settings.
* Evaluator spend charts, stat cards, and spend-limit monitoring on the Evaluators page now show only the evaluator spend for the agent you have selected, instead of the application tag filter. Filtering **Evaluators** spend data by agent is also available in the SDKs through the new `agent_id` parameter.
* You can now attach an existing workspace evaluator to an agent from the empty state of the Evaluators page, using the new **Add existing evaluator** button. Evaluators from the dataset attach flow now list all workspace evaluators, and attaching a dataset to an evaluator also attaches that dataset to your agent.
* Ask LangSmith Chat to create an evaluator from the Playground's Evaluate mode and it now opens the New Evaluator panel for the selected dataset with a drafted judge that is grounded in each example's reference outputs; you still press **Create** to save it. Outside Evaluate mode, LangSmith Chat finds and confirms a dataset, switches the Playground to Evaluate mode over it, and opens the same panel.
* Rules that are turned off no longer count toward your run rule limit, so you can keep disabled rules without using up a slot. Enabling a rule or creating one as enabled now returns an error when your tenant already has the maximum number of enabled run rules.
* Thread rules now stop fetching a window once its threads exceed the size limit, record an error for that window, and move on to the next window instead of running the worker out of memory. Evaluator validation returns a clear message when a project's recent threads are too large to evaluate.

## Feedback

* Annotation queue and manual feedback forms now follow a key's enforced feedback config, so scores outside its range are flagged before you submit, and the form shows the enforced rules instead of letting you define a conflicting config.

## Prompts and playground

* Prompt webhooks are now available in the Python, TypeScript, Go, and Java SDKs and in the `langsmith prompt-webhooks` CLI command, so you can list, create, retrieve, update, test, and delete them programmatically or from the terminal.
* Playground requests that use the OpenAI or Azure OpenAI Responses API with unsupported Seed or input schema settings now return a clear 422 error that names the rejected fields, and Playground invocations that run longer than 290 seconds now return a 504 timeout error with a retry suggestion instead of an ingress failure.
* Organization-scoped model configs can now be read and, with the right permission, managed with a service key that has no workspace, so API calls that previously returned a workspace-required error now succeed.
* Tag webhooks now report the same author name as commit attribution in the `created_by` field, so tag creation and update events show the name of the user who made the change instead of an empty value when the profile has no display name.

## Fixes and improvements

> [accordion] Show all fixes
>
> * Tool results from Anthropic models now appear under their matching tool calls in traces instead of as User messages, so each result shows beside the call that produced it.
> * Runs started or resumed through HTTP event-streaming commands are no longer blocked from being created by a malformed `langsmith-metadata` baggage value.
> * Experiment comparison and grouped views no longer fail with a "time\_range duration exceeds maximum of 401 days" error for experiments that have no explicit start time or that were created long ago. These views now load, with the lookback limited to 400 days.
> * Sending feedback with a thread ID to a project older than 400 days no longer fails with a 500 error; the anchor run is now found within the 400-day retention window.
> * LangSmith Chat now reports a failing tool call back to the model instead of ending the turn, so a tool error such as a 503 or a missing resource lets the model retry or tell you what failed, and other tool calls in the same step still finish.
> * Rules whose run output contains the literal text `\u0000` no longer fail to save their batch with an "invalid input syntax for type json" error, so affected rules commit their windows instead of retrying them on every run.
> * Claude Code image reads now work on Responses routes, so a tool result that contains an image is translated instead of failing with a 400 error about non-text blocks.
> * Audit log entries that contain NUL bytes in their operation name or enrichment fields are no longer rejected by the database, so the rest of the batch is saved and the affected entries are stored with the NUL bytes removed.
> * Sandbox costs in **All Workspaces** now keep the totals and rows from workspaces that load successfully when another workspace fails, with a partial-results warning and a **Retry** button that lists each workspace that could not be loaded.
> * Selecting AI search from a scope with an existing query now adds a separate AI search row and keeps your typed query in place, instead of clearing it.
> * Cancelled runs now stop within one heartbeat interval even when the cancel signal is briefly lost, instead of continuing until the run finishes.
> * Sorting by **End Time** in the dataset Experiments table no longer shows a "Failed to load experiments" error; that column now has no sort control, so the table loads normally.
> * The composite score picker now lists every feedback key that has number scores, including keys from annotation queues with categorical rubrics and keys written through feedback links. Before, those keys were missing from the picker.
> * Thread evaluators now receive the user and assistant turns in `human_ai_pairs` and `first_human_last_ai` for threads that contain a tool message without `tool_call_id`, instead of an empty input.
> * Opening a deleted prompt or context resource URL now shows a "Prompt not found" or "Resource not found" page with a link back to the list, instead of an endless loading skeleton.
> * Running `agent-browser` with `--cdp`, `connect`, `--auto-connect`, or a provider against a sandbox browser no longer fails with a "Cannot use --ca-cert with --cdp" error, and the attached browser works as expected.
> * Requests that send `typesafe-*` headers to the gateway now pass those headers through to the upstream provider, so features such as long-context requests that depend on them work as expected.
> * Invite email links for organizations created with newer UUIDv7 IDs now open the invitation instead of showing "Page not found".
> * The expand button now opens the **Shortcuts** pane when side navigation is open on narrower browser windows, instead of doing nothing.
> * Studio keeps its top bar and agent selector visible when an agent fails to load, such as when no assistants are deployed or the server is unreachable, so you can switch to a different agent.

**October 5-12, 2026**

## Highlights

* **AI search for runs, traces, and threads**: You can now describe what you are looking for in plain language on a tracing project page and search runs, traces, and threads with it. Select the AI option in the filter bar, type your query, and click Search or press Enter to apply it together with your structured filters, date range, and selected tab. Stats and filter counts are unavailable for submitted AI searches. Organization administrators turn on AI search in organization settings, including for personal organizations. When the service is busy, you see an "AI search is busy" message and can submit again. [Learn more](../../../Monitor/Debug/Viewing%20%26%20managing%20traces/Filter%20traces.md).
* **Find text within run details**: You can now search the loaded content of a run with Find, opened with Cmd/Ctrl+F in the active pane. Find matches input and output messages, object fields, tags, and metadata, shows a match count, and provides next and previous controls. Selecting a result expands the target and scrolls to the highlighted text, including the exact line and columns in JSON and YAML views. [Learn more](../../../Monitor/Debug/Viewing%20%26%20managing%20traces/View%20traces.md).
* **Granular organization permissions replace manage access**: Organization actions now require dedicated permissions instead of the single broad organization manage permission, so you can grant access to members, access control, authentication, security policies, billing, usage controls, retention, data planes, workspace creation, OAuth applications, and GitHub integrations separately. Updates through `PATCH /orgs/current/info` check the permission for each field you send, and read access to billing, data planes, and integrations is separate from manage access. Organization Admins and Operators keep their existing access, and the UI hides or disables controls you do not have permission to use. [Learn more](../../Govern/Users%20%26%20access%20control/Role-based%20access%20control.md).
* **Self-serve plans move to October 2026**: Existing self-serve Cloud customers are moving onto the October 2026 plans, which price usage in LangChain Standard Units. The new plan starts on the 1st of the current month at 00:00 UTC, so usage for the whole month is billed under it. Customers with a contract, a credit grant, or price adjustments on their plan stay on their current plan. [Learn more](https://docs.langchain.com/langsmith/pricing-plans.md).

## Administration

* You can now turn on AI search for your organization from the Projects page, with a consent step that explains data processing and PHI limits. Organization admins can enable it directly, and other members can send a request to their admins from the same dialog.
* Teams can now be managed with organization-level and workspace-level permissions, and the Teams APIs return 403 unless your organization has the `can_use_teams` setting enabled. Built-in roles such as Organization Admin and Workspace Admin receive the new teams permissions automatically.
* The ABAC settings page now includes Attributes, Policies, and History tabs, each with search and filters that persist in the URL and a CSV export. Attribute values show how many resources carry each value, and History lists policy create, update, delete, attach, and detach events for a chosen time range.
* You can now export organization members and API keys to CSV from the **Settings** page. The export includes every row that matches your current tab, search, and workspace filters, including rows on other pages.
* Custom roles can now be granted Engine permissions in **Settings** > **Roles**, with all four Engine permissions shown in the role editor and saved with the role.
* Traces from enterprise plans and self-hosted deployments are now billed at a flat 0.0075 LSU per trace, with no extended retention surcharge, unless your contract sets different rates.
* Bulk exports now bill each completed export partition by its uncompressed bytes through usage reporting in Metronome, so partition usage appears in your billing records once the feature is enabled for your environment.
* Custom MCP servers behind a LangSmith tunnel now accept headers such as `x-api-key` and `Cookie` exactly as servers outside a tunnel do, so customers no longer need to rename them, and OAuth-protected MCP servers can use a tunnel for their token, registration, and protected-resource endpoints. An authorization endpoint behind a tunnel is rejected at provider creation and update with a 400 error, because the browser cannot reach it.
* The hosted LangSmith MCP server now accepts access tokens issued for the LangSmith API, so one OAuth grant can be used for both the API and MCP. Other token audiences are still rejected.
* Agent Auth now mints GitHub App installation tokens, so agents can call `connections.get` on a `github_app` connection and receive a working token with the permissions you allowed, renewed automatically before it expires.

## Deployment

* Deployment settings now open in a side pane from the gear button, with General, Source, Preview Builds, LLM Gateway, and Scaling sections saved together through one Save. Scaling moved out of the header into the pane, and the pane is 960px wide, so fields no longer stretch across the full viewport.
* Deployment overview now shows a Revisions card beneath Details, with the current revision pinned at the top and New Revision as its primary action, so you can check status without leaving the page. The separate Revisions tab is removed, and bookmarks to tabs after Overview open the tab to their right.
* Deployment Monitoring now includes a Traces section with trace count, latency, and error rate charts that follow the same time picker as the server metrics, and the 7-day Trace Count chart has moved off the Overview to give Details more room.
* Custom headers for the deployment now live in the Connect dialog, where you can add, edit, and save them without leaving the page. Headers are still stored only in your browser, and the Settings dialog no longer shows them.
* The Source section of the deployment details card now shows where each deployment comes from: GitHub deployments link to the tracked branch or tag with auto-deploy status, Docker and template deployments show their image, and CLI uploads show that they deploy with langgraph deploy.
* Deleting a deployment now removes its database and metadata immediately instead of after a delay, so you can delete its tracing project right away and create a new deployment with the same name without waiting. Deleting a deployment now requires you to type "permanently delete" to confirm.
* You can now change the GitHub repository of an existing deployment in **Settings** > **Change repository**, or with `source_config.repo_url` on `PATCH /v2/deployments/{id}`, so a renamed or transferred repository no longer requires a new deployment. Saving does not redeploy; the next revision builds from the new repository.
* You can now edit environment variables on preview deployments and save them as a new revision, using the same editor as regular deployments. Deployment settings, scaling, and rollback remain unavailable for previews.
* You can now pass `exclude_metadata` to `POST /threads/search` and `POST /threads/count` to leave out threads whose metadata matches any object you list, such as automation threads in the Open SWE sidebar.
* Paused threads no longer show as `idle` after a run is cancelled or rolled back before its first checkpoint; they stay `interrupted` while their interrupts are pending. Cancelled runs now report why in `cancel_reason`, and thread `error` holds only real failures.
* Deployment log requests now read at most five pages from the logging backend per call, so sparse filters return sooner; when a response is short or empty, follow the returned cursor with **Search older** or keep the live tail running to get more lines.
* Studio chat now accepts TXT, CSV, TSV, Markdown, and JSON files, and sends them as text so Send no longer does nothing when you attach one.
* Studio's top bar now shows a **Connection** button for deployed agents, which opens the Agent Server URL and custom headers for that deployment. A rejected deployment's failure screen offers **Set custom headers**, which saves the headers to that deployment and retries. Header editors also gain a **Bulk edit** option that accepts YAML, JSON, or a pasted cURL command, and it imports the `-H` headers from the command.

## Gateway

* Gateway fallback simulation lets you test a workspace fallback chain by picking a model in the simulator and choosing Healthy, Rate limit, or Outage behavior for each model in the chain, so you can see which model answers and how much latency each fallback adds.
* Added OpenAI Decisions to the gateway at `/openai/v1/decisions` and `/openai/decisions`, so you can send native question-and-answer requests through the gateway with model access policies applied and get typed answers back unchanged. Decisions requests now appear as traces in LangSmith with answers and token usage, and count toward gateway spend caps.
* Scaledown compress, extract, classify, summarize, and decisions requests now produce traces in LangSmith with input and output token counts, and the models are priced at \$0.05 per million input tokens.
* You can now choose Automatic, Bedrock Runtime, or Bedrock Mantle as the preferred Bedrock endpoint for Bedrock models in the LLM gateway. Automatic keeps the current routing based on the model ID, so you only need to pick an endpoint for models available through both Bedrock surfaces.
* Gateway traces now have their own **Traces** tab next to **Usage**, so you can browse, filter, and expand requests sent through the LLM Gateway without leaving the Gateway page. Links from the **Usage** tab open this tab with the same filters applied.
* You can now add custom regex patterns to guard policies in the Gateway, so you can have matching text redacted from requests before they reach the upstream model. Add a pattern in the `detect.custom` field of the guard policy config, using a single Go regular expression (RE2 syntax) of up to 512 bytes.
* You can now invoke managed-tools MCP servers and gateways with an access token from your workspace's OIDC identity provider by sending it in the X-Agent-Auth-Principal-Authorization header. Workspace managers can link one provider under **Settings** > **Tools** > **Configure OIDC**.
* MCP gateways now support up to 10,000 tools, and you can choose connection requirements for each gateway: **Require all connections** makes every provider connected before any tools are available, while **Use connected tools** lets people use connected providers and keeps unavailable tools hidden.
* Adding a server as Public now fails with a clear error when the server requires OAuth or other authentication, instead of saving a server that shows Connected but cannot list its tools. Servers that answer without credentials, such as DeepWiki, Exa, and Jina, still save as Public.
* The managed tools OpenAPI spec at /v1/managed-tools/openapi.json is now available in production, not only in development and staging. Requests still require workspace authentication, the lmt\_enabled entitlement, and mcp-servers:read permission.

## Sandboxes

* Sandbox command history is now retained for Boxes that have run Execute API commands, so you can list, filter, and search past commands and read their stdout and stderr output after the Box stops. This capability is off by default and must be enabled by your deployment through `SANDBOX_COMMAND_HISTORY_ENABLED`.
* Sandbox egress can now route through your own HTTP forward proxy: set `SANDBOX_EGRESS_UPSTREAM_PROXY_URL`, or `sandboxes.authProxy.httpProxy` in the self-hosted Helm chart, to send plain HTTP as absolute-form requests and HTTPS and raw TCP through CONNECT tunnels. Destinations listed in `SANDBOX_EGRESS_UPSTREAM_PROXY_NO_PROXY` use standard NO\_PROXY matching and are dialed directly.
* Self-hosted customers on Azure can now disable access keys on Azure Managed Redis and still run sandboxes by setting `sandboxes.juicefs.redis.iamAuthProvider` to `azure`, so sandbox file metadata connects with Microsoft Entra ID instead of a password. The sandbox host and the formatter Job need Azure Workload Identity, and that identity needs a data access policy on the Redis instance.
* Sandbox filesystem capacity is now capped at 640 GiB by default, so creating or resizing a sandbox above that limit returns a validation error instead of failing later. Operators can change the limit with `SANDBOX_MAX_FS_CAPACITY_BYTES`, and existing sandboxes keep their current size.
* You can now suspend the sandbox host pool by setting `spec.sandboxes.host.suspended` to `true`, which stops sandbox hosts and hides the sandbox UI while keeping managed storage and configuration in place. Setting it back to `false` restores the sandbox UI and host capacity, and the host autoscaler resumes control of replicas.

## Tracing

* OpenTelemetry span attributes that are not part of the LangSmith schema are now stored in run metadata for all tenants in US, EU, AWS, Azure, and GCP APAC production environments, so they appear in the **Metadata** section of each trace.
* Custom charts now support token and cost detail metrics, including cache creation and read, reasoning, audio, image, and video, with sum, min, max, and percentile aggregations. The Prompt cache hit rate chart template is available for tracing projects, and these metrics appear only on data planes that report token detail support.
* You can now add any environment from any agent to a dashboard chart, including environments that belong to agents other than the one currently selected.
* Adds `GET /api/v1/sessions/resolutions`, which takes an agent environment, an experiment ID, or the workspace's evaluators and returns the tracing project `session_id` for that address, so you can pass it to any endpoint that accepts a project ID. Addresses you cannot read return 404, and BYOC workspaces return 501 for now.
* Multipart run uploads and OTEL trace batches now count toward your short-term ingestion limits for tracing bytes, tracing requests, and events per minute. OTEL trace batches also now stop with a 429 once you reach your monthly unique-traces limit, instead of writing past it.
* Trace tree requests now return at most 1000 runs by default, down from 5000, and a `max_runs` value above 1000 is rejected.
* Semantic run, trace, and thread queries are now rate limited per workspace and endpoint: frontend requests allow 25 per minute and API-key requests allow 10 per minute, and requests over the limit return a 429 with Retry-After.
* Agents in the Agent list are now ordered by their latest run start time, so agents with recent activity appear first, and agents without runs appear last. If you saved a list cursor from before this change, the request now returns 400; restart from the first page to continue.
* When ingestion adopts a new tracing project as an agent, the agent now also gets empty **Local**, **Development**, and **Staging** environments alongside **Production**. Migrated agents keep their original tracing data in **Production**, and other environments are created when a deployment requests them.
* Insights reports now include category and subcategory endpoints that let you browse classified root runs and their counts for a saved Insights configuration when online Insights is enabled.
* Run rule webhooks that reach the shared delivery engine now report their final delivery result in the rule log, so a webhook that fails or does not finish in time shows as an error on its batch and runs instead of as a success.
* Self-hosted installs with an online license key now receive new model prices hourly, so prices no longer wait for a full release. Installs that have turned off usage reporting, air-gapped installs, and data planes do not sync.
* LangSmith Chat now always opens in the right sidebar, which can be resized, and the left navigation collapses when LangSmith Chat opens. The floating window and the **Move to sidebar** and **Detach from sidebar** controls are removed.

## Engine

* Engine now watches CI on the pull requests it opens for your issues and, when checks fail on its own commits, automatically pushes a revision that reproduces the failing checks and fixes them, up to three revisions or 90 minutes per chain.
* Boards can now notify you when Engine opens a fix pull request. Slack destinations that also get issue alerts post the fix PR as a reply in that issue's thread.
* Slack destinations can now mention a coding agent on new issues, or under the Fix PR ready message when that is on, with a custom instruction set in the **Message to the agent** box. Engine's own fix run continues independently of the mention.
* Engine is now available on BYOC data planes that report Engine enabled, and each data plane has its own independent monthly Engine budget. Background Engine runs on these data planes now honor your current plan eligibility and Engine opt-out settings.
* Engine now uses GPT-6.1 Sol as its heavy OpenAI fallback and GPT-6 Luna for Codex fix reviews and implementation, with usage priced in LCU for both models.
* The issues agent can now file an issue from a single trace, so one clear failure no longer has to wait for a second matching trace before it is reported. Patterns that still lack evidence remain on the Agent Overview watch list.
* Board trace filters now show how many traces from the last 30 days match the condition as you type, and **Add** is disabled when it would match none, so a filter on a child run no longer saves with zero traces.
* The Engine agent can now read a repository's full commit history and compare commits through the GitHub REST API from its sandbox, including on private repositories, so it can trace an issue past the 50-commit clone's root. Access is read-only and the token never enters the sandbox.
* Closed issues with a pull request now keep a view-only PR link, the history line names the merged PR or Linear sync that resolved the issue, and "Watch" is now "Save for later" across the issue board and LangSmith Chat.
* Issue validation now replays each source run against its fix preview deployment, so a validation no longer fails when the original run used non-chat input, checkpoint state, or agent-type configuration that trace-only chat reconstruction could not reproduce. Roots that cannot be replayed are reported with a stable failure reason instead of being judged.
* Self-hosted deployments can now pull a FIPS-compliant Insights Engine image, `langsmith-insights-engine-fips`, alongside the existing Insights and LangSmith Chat FIPS images.

## Evaluators

* Code evaluators in run rules can now define `evaluate(ctx)` to score runs, and the sandbox prefers it over `perform_eval` in Python and `performEval` in JavaScript, which still work as before. The `ctx` object exposes `run` and `example`, with the same fields available as attributes.

## Feedback

* Annotation queue reviewer notes now save as you type, so each run keeps a single note that persists when you reload or move to another item, with no send button required.
* Feedback comments and evaluator reasoning now render markdown, so headings, lists, bold, italic, and inline code stay readable in the trace view, annotation queues, experiments, and the runs table popover.
* Annotation queue rubric items now return the feedback config they use, so the rubric shows the right scale or categories when a feedback key has more than one config. Items not yet linked to a config show the key's first config, and deleted configs are left out.

## Datasets and experiments

* Dataset tables now preview the most distinguishing input field in each example instead of the first field, so rows with a shared value such as a constant brand no longer look identical in the Inputs column of the Examples tab, public shared datasets, and experiment comparison tables.

## Prompts and playground

* You can now select Claude Haiku 5.5 in the Playground and in gateway model configuration for Anthropic, Amazon Bedrock, and Google Vertex AI.

## Fixes and improvements

> [accordion] Show all fixes
>
> * Fixed an issue where runs could be missing from SmithDB when a trace was upgraded (for example, after feedback was added) before the run's initial data finished writing. Runs now appear in SmithDB, and pending run updates are no longer left with an empty end time.
> * Fixed a crash in the run detail view and peek pane when a run's message list became shorter while the page was open; the view now renders the remaining messages instead of failing.
> * Deep-linked traces now appear in the thread view even when the thread index has not caught up yet, and turns that are still missing a number show a refresh button in place of the number so you can load it on demand.
> * Runs, Traces, and Threads keep rows that already loaded when a search fails partway through, showing the error in a banner above them. Failed later pages no longer load endlessly or fetch further automatically, and Search retries them.
> * Fixed a bug where tool results and messages inside LangChain and LangGraph traces could show the wrong jump target and spurious issue banners; the Open run action now works correctly for linked runs inside sub-agents.
> * Command-click on macOS or Ctrl-click on Windows and Linux on a run in the runs table now opens that trace in a new tab, while an ordinary click still opens the run in the side panel.
> * Run queries that return too much data now fail with a clear 400 error that says the run exceeds the response size limit, and overloaded query requests now return a 429 that asks you to retry later instead of a generic 503.
> * OpenAI Responses traces that include additional tools now show each tool definition inside its Developer message, with descriptions, typed parameters, and required fields, instead of falling back to the Fields view.
> * Custom dashboards you created in your workspace now appear in the **Dashboards** list when an agent is selected in agent monitoring, instead of being hidden by the agent filter.
> * Agents in projects with restricted access now open right after creation instead of showing "Project not found" until the project list refreshes.
> * Creating or upserting a project named `evaluators`, `playground`, or another internal tracing name now keeps it as a plain project instead of an agent, and renaming an agent to one of those names returns a 409 error with a clear message.
> * Insights reports no longer publish when parent category generation fails. Instead, the job ends with an error, and if the clustering model rejects the request, the error message tells you to check your model credentials and settings.
> * Claude Haiku 5.5 runs are now costed at its base rate of \$0.10 per million input tokens instead of the five-times-higher long-context rate, which had inflated costs for first-party, Vertex, and Foundry runs.
> * Past LangSmith Chat chats now show their saved messages right away instead of an empty panel for up to a few minutes when the chat uses a Bedrock model with an IAM role.
> * LangSmith Chat turns no longer fail with "network error" when your connection drops mid-turn, such as when Wi-Fi changes or a VPN reconnects. The run continues on the server and reconnects to your chat instead of being cancelled.
> * Fixes DeltaChannel reads and prunes that could lose state on threads with checkpoints saved without snapshot counters, or with durability="exit"; reads and prunes of these threads now keep the channel's older values intact.
> * Fixed a bug where a DeltaChannel written by several parallel tasks in one super-step could be read back in a different order than the run produced, so **get\_state** and the next run returned reordered values; these now match the order the run returned.
> * Creating a run with a run ID that already exists now returns a 409 Conflict error on SQLite, Postgres, and in-memory deployments, instead of an internal server error or being silently ignored.
> * Rejoining a failed resumable run with `Last-Event-ID` now replays the run's final `error` event, so a client that reconnects after a failure can tell the run failed. Joining with a `stream_mode` filter also returns that `error` event.
> * Fixed v2 thread event streams ending silently when reading events fails: the SSE stream and WebSocket now send a final error frame with the unknown\_error code before closing, so clients can tell a failed stream from an idle one.

**September 28-October 5, 2026**

## Observability and evaluations

### Tracing

* The LangSmith MCP adds a `query_runs` tool that accepts the same parameters as the SDK's `client.runs.query()`, including typed `selects` for costs, token breakdowns, and full inputs and outputs, with cursor pagination. It returns token counts and USD costs by default. `fetch_runs` now also returns costs and token counts, and is deprecated in favor of `query_runs`.
* Costs now resolve for every OpenAI model on the pricing page, including those listed only under "All models", such as GPT-5.6 Luna and Terra. The daily price sync previously read only the models the page shows by default, so the rest kept stale prices. [Learn more](../../../Monitor/Trace/Configuration%20%26%20troubleshooting/Cost%20tracking.md).
* Costs now resolve for the open models Vertex AI hosts through Model-as-a-Service: DeepSeek, Qwen, GLM, Kimi, MiniMax, and GPT-OSS. [Learn more](../../../Monitor/Trace/Configuration%20%26%20troubleshooting/Cost%20tracking.md).
* The Messages view now shows the user message on OpenAI Responses API calls that send it as a plain string, which is how calls chained with `previous_response_id` or a conversation send each new turn.
* The Messages view requests smaller pages, so long threads no longer fail with a response size error.
* When a trace or thread filter fails, LangSmith shows the error below the filter and keeps the selected run details open, so you can edit or clear the filter without leaving the page.
* Creating a public trace or thread share link now requires permission to read the runs, including their inputs and outputs.
* The LangSmith Chat model picker now offers Claude Sonnet 5.5. Sonnet 5 stays the default.
* LangSmith Chat can now take about four times as many steps in one turn, so a large custom app build finishes instead of ending with a "Recursion limit of 250 reached" error.
* Chat on a Gemini 3.x model through Vertex AI now completes turns that call several tools in a row.
* Apps that LangSmith Chat builds now page through lists such as annotation queue items instead of showing only the first page.
* Sorting tracing projects by **Most Recent Run** now orders projects whose runs reference dataset examples by their latest run, instead of grouping them with empty projects.

### Datasets and experiments

* LLM-as-a-judge evaluators using Claude Opus 5.5 or Sonnet 5.5 on Amazon Bedrock no longer fail because of unsupported forced tool choice.
* Creating an evaluator now selects the default evaluator model preset from model settings, including LangSmith Gateway presets.
* Clicking **Test** on a thread or trajectory evaluator now shows export and validation failures instead of appearing to do nothing. Evaluator tests also show configuration errors, such as a missing endpoint URL, in the evaluator panel.
* Deleting a code evaluator no longer times out waiting for sandbox snapshot cleanup.
* Experiment run progress now reflects recorded runs when available, rather than only settled batches.
* **Add to dataset** now saves the full source run metadata, and metadata you supply is merged with the run's metadata instead of replacing it.
* Replacing a dataset's examples with `PUT /v1/platform/datasets/{dataset_id}/examples` succeeds again when the request updates existing examples.
* LLM-as-a-judge evaluators whose prompt carries both an old and a current output schema now check scores against the schema the judge uses, so scores are saved under the right feedback keys.

### Feedback

* Runs opened in an annotation queue now show the same top bar as runs in tracing, so annotators can switch between the Trajectory and Details views while reviewing.
* Annotation queue instructions keep their line breaks in the review side panel, so multi-line and list-style instructions display as written.
* Adding a run to a dataset from an annotation queue now saves your edits when the output is a single message, and shows an error if the example cannot be created.

### Prompts and playground

* GPT-6.1-Sol is available and selected by default for new OpenAI prompts in the Playground and new model configurations.
* Claude Sonnet 5.5 is available in the Playground and model configurations for Anthropic, Amazon Bedrock, and Vertex AI.
* Gemini 3.7 Flash and Gemini 3.8 Flash are available in the Google Gemini and Vertex AI model selectors.
* The LangSmith MCP's `get_prompt_by_name` now returns the prompt template. New tools let agents push prompt versions, browse commits, manage commit tags, update or delete prompts, and read and commit Context Hub agent and skill files.
* Editing a Context Hub webhook now loads its saved custom headers, so saving no longer overwrites them.
* Loading a saved Bedrock Converse configuration whose model ID is an application inference profile ARN now keeps the provider set in **Extra Parameters**.

### Engine

* Engine usage, spend limits, and pricing now display in LangChain Standard Units (LSUs). Dollar amounts are unchanged. [Learn more](../../../Engine/LangSmith%20Engine.md#manage-engine-costs).
* Issue validation requests its judgment as a tool call, so a failed structured-output response no longer aborts the run.
* Engine projects that previously selected Skills for Coding Agents now use standard issue analysis, with scan cadence based on their configured analysis level.
* Engine project boards no longer show the floating feedback survey.

## Deployment

* Agents connected to LangSmith's native MCP server can find deployments and revisions and read build or runtime logs, filtered by revision, time, search text, and severity. Deployment summaries omit secrets and environment configuration.
* The revision line on a deployment's **Overview** tab shows the commit title, links to the commit on GitHub, and shows the exact time in your local time zone. A failed revision reads "Build failed" or "Deploy failed", with the full error a click away.
* Deployment log API entries now say whether a line came from the API server, a queue worker, the build, or the platform, which replica wrote it, and selected fields of structured JSON log lines such as run and thread IDs.
* Studio's thread sidebar and the deployment **Threads** tab request only the fields they display, so lists load for deployments whose threads previously exceeded the Agent Server response size limit.
* Searching server or build logs for text that contains quotes or backslashes now returns matching lines instead of an "Invalid or expired offset" error. Log searches are limited to 1,000 characters.
* Server and build logs for deployments hosted on AWS now list the most recent lines first when sorted newest first.
* The deployment **Overview** tab no longer shows a Postgres disk usage banner. Disk usage is still charted on the **Monitoring** tab.

## Sandboxes

* The LangSmith MCP can read, write, and search sandbox files, stream long-running sandbox commands, share sandbox ports behind LangSmith login, and report sandbox usage, organization usage, audit logs, usage limits, trace retention settings, and organization members.
* Sandbox proxy rules accept `match_headers` entries such as `"authorization: Bearer account-b"`, so several rules on one host can each swap a different placeholder for its own credential and serve multiple accounts.
* A memory-preserving sandbox that was snapshotted while running now resumes with all of its memory after its next stop and start.
* A brief storage backend error no longer leaves a sandbox's filesystem returning I/O errors until restart.

## Administration

* OAuth applications registered under **Settings** > **OAuth applications** can use one access token for both the LangSmith API and the Remote MCP server, instead of authorizing each separately.
* Calls through LangSmith Managed Tools now appear in audit logs as `invoke_mcp_server` or `invoke_mcp_gateway`, with the server or gateway and the tool called. Audit log entries also include the request's duration and user agent.
* Search organization and workspace settings from the keyboard, and open **Settings** with Command + comma on Mac or Ctrl + comma on Windows and Linux.
* Search permissions by group, name, or identifier in role previews and the role editor.
* Usage charts and CSV exports keep historical usage when billing metrics change and hide metrics with no usage.
* Sign-up and login retries no longer carry stale authentication errors into their return URLs.

### LLM Gateway

* Route ScaleDown requests through the LLM Gateway with your workspace's `SCALEDOWN_API_KEY`. Native compression, extraction, classification, decisions, summarization, and batch APIs keep their request and response formats.
* The LLM Gateway applies existing custom provider fallback policies when you call a saved model configuration through a unified endpoint. Explicit model configuration policies take precedence.
* The LLM Gateway now accepts a Responses `function_call_output` whose output is an array of text parts. Gemini and other translated providers previously returned a 400 on this form, which broke MCP tool results sent by LangChain.
* Fallback chain model selectors show **Workspace** or **Organization** badges for custom model configurations.

**September 21-28, 2026**

## Observability and evaluations

### Tracing

* The Trajectory view is available to everyone, with turn navigation, expandable messages, and consistent trace details.
* The tracing quickstart and guided onboarding now cover Claude Code, OpenAI Codex, VS Code Copilot, and Cursor, with plugin installs and environment setup generated for your project and region. [Learn more](../../../Monitor/Trace/Tracing%20setup/Integrations/Developer%20tools/Trace%20Claude%20Code%20sessions.md).
* Gemini runs now report cost regardless of which SDK traced them. Previously, Gemini calls traced through clients other than `google_genai` showed no cost. [Learn more](../../../Monitor/Trace/Configuration%20%26%20troubleshooting/Cost%20tracking.md).
* Traces can now contain up to 100,000 runs.
* Revamped tracing filters are available whenever SmithDB queries are enabled, without a separate feature flag.
* The **Error** column shows error descriptions directly in the trace table again.
* The trace **Tools** tab shows function tools alongside provider server tools such as OpenAI `tool_search`.
* Delete a bulk export destination that no bulk export uses with `DELETE /api/v1/bulk-exports/destinations/{destination_id}`. Destinations still referenced by a bulk export are rejected.
* Custom model price entries now have a **Clone** action, like built-in entries.
* Run latency values over two minutes display in minutes.
* The LangSmith Chat model picker now offers Claude Opus 5.5 and Gemini 3.8 Flash, and Gemini models complete turns instead of failing on the first message.
* Drop or attach images in LangSmith Chat, anywhere in the panel.
* LangSmith Chat lists runs with previews of their inputs and outputs and opens a run in full only when needed, so large projects no longer make chats and custom app builds fail with "An internal error occurred".
* LangSmith Chat renews its access during a long turn, so reads of your queues, datasets, and runs keep working instead of ending the turn with an "Invalid token" error.
* LangSmith Chat groups three or more consecutive exploration actions while building custom apps. Groups open automatically when an action fails or needs attention.
* Chat keeps working past the first tool call when a workspace model configuration points at Gemini on Vertex AI.

### Datasets and experiments

* Completed annotation queue items can now be deleted from the queue's single-item and bulk views, and through the delete APIs.
* Custom output renderers in the experiment comparison and single-experiment panes now receive the example's inputs in `metadata.inputs`. Reference outputs are sent with `type: "reference"`, matching the documented message format. [Learn more](../../../Test/Datasets%20%26%20Experiments/Datasets/Custom%20output%20rendering.md).
* Trajectory evaluators are available on every data plane that reports the trajectory runtime as supported, without a per-workspace rollout flag.
* The trajectory API returns each message's tool definitions only when the request sets `include.tool_definitions` to `true`. The rule editor's **Test** preview now matches what live trajectory evaluations send to the judge.
* **Include annotator name and comment per row** on the experiment CSV export now takes effect for every workspace.
* Online LLM-as-a-judge evaluators that return a placeholder JSON field such as `output` now store feedback under the evaluator's configured name.
* Updating an online evaluator rule through the API no longer fails when the request includes a hub prompt reference but leaves out `evaluator_version`.
* Thread evaluators no longer offer the **Align Evaluator** flow or correction datasets, since alignment requires run-level examples.
* Pairwise annotation queues now show `true` and `false` output values when a field is expanded.

### Feedback

* Annotation queue rubric items now appear in the order they were added instead of alphabetically, in the queue editor, the review sidebar, and CSV exports.
* Feedback extra metadata, including nested metadata, now round-trips through direct and multipart ingestion.
* The legacy `error` field on feedback creation is deprecated. Send evaluator failures through `extra.error`. The legacy field remains supported and takes precedence when both are provided.

### Automations

* Evaluator traces now use the evaluator's display name instead of the generic `RunnableSequence` name.
* When an automation cannot fetch runs after its retries are used up, the rule log shows the error that occurred, such as a timeout.

### Engine

* Paste, drop, or attach up to four images in the Engine chat composer and send them with your message.
* Engine settings open in the board's detail area instead of a slide-over pane, so a settings link can be shared and reopened.
* Engine highlights support for finding and fixing issues across multiple GitHub repositories, with a shortcut to manage connected repositories in settings.
* References to other Engine issues in descriptions and proposed fixes link directly to the matching issue. Hover over a link to see the issue title.
* Connecting a GitHub repository no longer starts a fix run for every open code-rooted issue at once. A fix run starts when you ask for one, or on the board's schedule.
* Unlinking a pull request from an issue now holds. Engine reads the issue marker only when the pull request is opened, so put the marker in the body when you open it.
* Engine boards can use write-only custom authentication headers when replaying traces against deployments with custom authentication.
* Engine fix branches now start with `langsmith-engine/` instead of `issues-agent/`. Issues with a fix branch reserved before this change keep their `issues-agent/` branch.
* Retrying or editing a message after a turn was cut short no longer fails with "Attempting to delete a message with an ID that doesn't exist".

### Prompts and playground

* Claude Opus 5.5 is available in the Playground for Anthropic, Amazon Bedrock, and Vertex AI, and is the default model for new sessions with those providers.
* The OpenAI model dropdowns now suggest `gpt-6-sol` and `gpt-6-luna`.
* The Playground renders editable prompts from traces containing LangChain message objects, including multimodal content and messages without an explicit role.
* Prompt webhook custom headers now persist when saved.
* The Playground no longer crashes when streaming longer responses.

## Deployment

* The **Overview** tab summarizes the deployed revision on a single line, with its source, age, and logs, and reports a newer rollout there as it queues, builds, or fails. A deploy that failed after replacing the running workload offers a rollback from that line.
* Production deployment pages show whether the deployment is responding to requests right now, separately from revision status. The badge also appears for deployments served from a custom URL.
* GitHub revisions show the commit title alongside a badge with the branch and short SHA. The Deployments API returns `repo_commit_title` next to `repo_commit_sha` on each revision.
* Deployments pinned to an annotated Git tag now record the commit the tag points to in `repo_commit_sha`.
* Server logs include API and worker logs for AWS deployments whose pod names are shortened by Kubernetes.
* Studio waits for deployment details to load instead of briefly showing a connection error, and shows the cause when a deployment cannot be loaded.

## Sandboxes

* `access_delegation` on sandbox create now works with a workspace service key, so a deployment that holds only a service key can give its sandboxes capped LangSmith access. Narrowing the key's role narrows the sandbox, and deleting the key revokes it.
* Each file shared through a sandbox download link is served from its own host, and `csp_sandbox_flags` accepts `allow-same-origin`, so an HTML page can use `localStorage` and IndexedDB without other files reading them.
* Sandbox calls return 503 with a `Retry-After` header while no host is available, instead of a 502, so clients that retry on 503 recover during host maintenance.
* Creating a snapshot from an image with no `linux/amd64` variant, such as an arm64-only image built on Apple Silicon, now fails immediately with a message naming the image's platforms.
* The snapshots table shows tags as badges and a short snapshot ID below each name. Snapshot selectors offer the latest version of each system snapshot.
* Browser editing for Custom Apps is available to eligible workspaces with sandbox support enabled, and Custom Apps no longer displays a `Beta` badge.

## Administration

* Cloning a dashboard now requires both the `charts:read` and `charts:create` permissions. Roles that can only view charts, such as Workspace Viewer, can no longer clone dashboards, and custom roles that should keep cloning need `charts:create`.
* Changing the role on a workspace-scoped service key now requires permission to manage keys in every workspace the key covers.
* Preview the base permissions of each selected role in the service key creation form.
* Agent Auth connections support encrypted, write-only `token_request_headers` for OAuth token exchange, refresh, and revocation.
* Resolving Agent Auth principals accepts the `deployments:create` permission in addition to `workspaces:manage`, so Workspace Editors can run `mda dev` with user-owned connections.

### LLM Gateway

* Choose hosted models, providers, or saved configurations from a searchable model picker, run a sample request, and copy its code. [Learn more](../../../LLM%20Gateway/Get%20started/LLM%20Gateway.md).
* Keep sample code visible while a Gateway request runs, then inspect the response, serving model, HTTP status, token usage, and trace. [Learn more](../../../LLM%20Gateway/Get%20started/LLM%20Gateway.md).
* The LLM Gateway no longer blocks Claude Max and other provider-billed subscription requests when a Gateway spend policy is exhausted. Rate limits, model access policies, and guardrails still apply.
* The LLM Gateway preserves Claude feature headers and classifier fields through Anthropic, Amazon Bedrock, and Vertex AI Messages routes, including streaming. This enables Claude Code's no-charge server-side auto mode checks where the model and platform support them.
* Vertex AI model configurations route Anthropic Claude models to Vertex AI's native Anthropic Messages API, while Gemini and open models keep using the OpenAI-compatible endpoint.
* The LLM Gateway omits temperature from unified API requests unless the destination OpenAI model and reasoning setting support it, preventing unsupported-temperature errors on newer models.
* The `phase` marker Claude Code sends on partial-turn content blocks no longer causes a 400 error when a `/v1/messages` request targets a Chat Completions model. The marker is dropped with a warning.
* The spend chart y-axis shows cents when total spend is below a dollar, instead of rounding every label to \$0.

**September 14-21, 2026**

## Observability and evaluations

### Datasets and experiments

* The completed items list in an annotation queue now offers Add to Dataset for selected thread items, importing each thread as a multi-turn example.
* Edit and delete in the experiments table now check project permission, to match BE.
* Charts now show shape-aware loading skeletons instead of temporary zero values while data loads. Evaluator spend charts use bar and metric placeholders that preserve the final layout.
* Downloading experiment results with "Include annotator name and comment per row" now keeps automated evaluator scores in every feedback column, alongside human annotations.
* The evaluators list API accepts an agent\_id filter to return evaluators attached to the agent's environments or tagged datasets.
* An evaluator using an organization-scoped model configuration that authenticates with an API key no longer attempts a per-model OAuth token exchange. Amazon Bedrock models configured this way are no longer rejected as unsupported.
* Categorical evaluator fields resize with the editor pane, keeping descriptions and remove-category buttons inside the feedback configuration card.
* Evaluator side panels disable Save while the configuration is invalid and display the reasons. Correcting the configuration enables saving again.
* Evaluator forms explain validation errors in the Save tooltip instead of a banner. Save remains disabled until the configuration is valid.
* Evaluator side panels show mapping errors and prevent saving when run evaluators use thread or trajectory sources, or thread and trajectory evaluators use run sources. Validation updates when the evaluator target changes.
* Evaluator variable mapping now explains clearly that trajectory and non-trajectory variables cannot be used together.
* Trajectory evaluation selects the latest trace by its root run's start time rather than a child LLM run's start time. Trajectory metadata reports each trace's actual root start time and marks scopes with missing root timestamps as incomplete.
* The evaluator configuration form now displays the complete sampling-rate percentage at every supported input size.

### Feedback

* The header count and the delete confirmation on the annotation queue "View all items" page now reflect the active time range instead of the whole queue. The item count endpoint accepts min\_start\_time and max\_start\_time.
* Changing a feedback score on a completed queue item previously raised a "Failed to update review time" error even though the score saved. The toast is gone; the score still saves as before.
* The annotation queue size endpoint now counts queue entries whose runs were deleted, matching the queue's run list instead of silently dropping them.

### Tracing

* Publicly shared thread pages no longer show a share action that cannot succeed.
* Insights no longer warns that it is optimized only for OpenAI or Anthropic when both selected models use another provider.
* Insights report jobs now retry with a smaller page size when a trace scan times out, instead of failing the whole report.
* Alerts using input, output, or error text filters match runs regardless of the blob storage and ClickHouse search settings. Search tokens are still written to ClickHouse only when both blob storage and ClickHouse search are enabled.
* Starting a new conversation immediately after a reply, then sending a message, no longer loses that message. LangSmith Chat now streams it into the new conversation instead of dispatching it against the previous one.
* When a tracing batch takes longer to upload than the server will wait, /runs/multipart and /runs/batch now stop reading and return 408 Request Timeout instead of a 503. A timeout caused by the server rather than the upload returns 504.
* Insights now recommends a capable thinking model and a fast summarization model with a large context window, without warning against mixing providers.
* The LangSmith Go and Java SDKs can now save Insights report configurations, enabling clients to create UI-visible Insights reports programmatically.
* The Columns menu on a tracing project's traces and runs table now lets you deselect Status and Name, and drag them into any order alongside the other columns.
* Dashboard chart feedback key suggestions now include keys from both run-level and thread-level feedback.
* The project stats sidebar shows Cache Hit % above streaming rate, helping you see the share of input tokens served from the prompt cache.
* Select TURN\_NUMBER when listing thread traces to return each trace's chronological position across pages. Turn numbers are also available for public shared threads.
* The LangSmith Go and Java SDKs can now list, update, and delete saved Insights report configurations, including their recurring schedules.
* LangChain trajectories use message IDs from root runs to identify the main conversation, falling back to the existing selection when no unique match is available or optional root enrichment fails. Other formats do not fetch this enrichment. Processing runs and optional roots share one byte budget, and the default message-view and trajectory contribution limits are 200 MB.
* The thread traces API now accepts `trace_filter` and `tree_filter` query parameters for filtering root runs and matching runs anywhere in a trace tree.
* The disclosure header of the linked-issues section in the trace detail pane now renders at its intended height instead of clipping its content.

### Engine

* Engine issue descriptions preserve their concise prose while rendering mentioned file paths, functions, classes, tools, and code identifiers as inline code.
* The issue detail header read its timestamp from the issue's last-modified time, so routine updates, such as Engine linking new evidence and refreshing the description, made a closed issue appear to have just been marked done. The header now reads "Updated `<when>`"; who closed the issue and when is shown in the history below it.
* Engine now scans projects whose names contain punctuation, Unicode, or other special characters instead of leaving their boards stuck while analysis starts.
* An Engine scan no longer fails outright when its project-stats request does not come back. It proceeds with the errored and baseline traces it can still select, tells the agent which selections are missing, and records why the stats call failed.
* The LangSmith Chat composer now accepts focus when a side pane such as Edit Engine Settings is open, so you can ask questions without closing your settings first.
* LangSmith Chat keeps your conversation as you navigate and reload within a browser tab, and starts a new one in a new tab or after you restart the browser. Earlier conversations are still available from the conversation history.
* Opening a past LangSmith Chat conversation no longer fails with "Unable to connect to LangGraph server" when the workspace's model credential can no longer be resolved. Reading a conversation only needs its stored history; sending a new message still reports the underlying credential error.
* Run local production-parity red-team checks against supported Dev targets with their configured trace project and repository context.
* The LangSmith Chat icon and suggested question now share one continuous background, so the launcher reads as a single pill in light and dark mode.
* Engine now reads the contents of successful tool results rather than only their status, so it files issues where a call returned less data than its own result claims or where a value arrived truncated. Defects that never surface as an error are no longer passed over.
* The Home page no longer shows the Engine announcement banner. Engine remains accessible through its Home card and issues section.
* Engine issue boards now show a spinning “Generating fix” action instead of “Open PR” while a fix is still being generated.
* An Engine Red Team run on a project that Engine has already scanned now starts from that project's Agent Overview and runs a shorter confirmation scan, instead of re-deriving the application map every time.

### Automations

* Automations grouped by thread can now send webhook payloads with matched conversations and their runs.
* A backfill that finds every run on a page already processed now continues to the next page instead of ending the window early, so the runs behind that page are still evaluated.
* A thread or trajectory automation batch that fails its last retry no longer leaves a partial page cursor behind, so the next scheduled window starts from the beginning of the window instead of mid-page. An automation whose trajectory service URL is not configured now records one failed rule-log entry instead of retrying until the attempt limit.
* A trajectory evaluator's retention upgrade no longer bounds the trace by an approximate start time, so the root run and its earliest children are upgraded along with the rest. The evaluated-run link on a trajectory evaluator's trace is withheld until it can point at the right run.

### Monitoring and alerting

* Choosing a Slack channel for alert notifications now works in workspaces large enough that the channel list had stopped loading altogether.
* Charts now show loading placeholders that match their final visualization, including bar, line, donut, metric, and sparkline charts.

## Deployment

* Scale-to-zero deployments reject rollbacks to revisions below LangGraph API 0.13.0 or without a known compatible version. The rollback dialog directs you to rebuild the target commit with a supported version.
* Your plan's included free Serverless deployment is now assigned automatically no matter how you create it. Previously only deployments created through the web app took the free slot, so a first deployment created via the CLI or API was billed even when a free one was available.
* Newly created Slack apps in mention mode respond to explicit mentions in group DMs and their threads, preventing duplicate runs from overlapping events. One-to-one DMs and all-messages mode continue to receive ordinary messages.
* Section dividers in agent overview cards and Gateway connection panels have stronger contrast in light and dark mode.
* The Studio memory editor keeps its close button visible while you scroll through long memory items.
* Filter the custom apps list by creator and preserve the selection in the page URL.
* Creating a dev deployment now shows how many free deployments your organization has left and uses an available free slot automatically. The separate free deployment option has been removed.
* Self-hosted upgrades can rerun the usage metering migration without duplicate-trigger errors or replacing existing model pricing with default rates.
* Managed Deep Agents can discover OAuth settings from an MCP server's authentication challenge when well-known metadata lookup fails.

## Sandboxes

* View compute and storage cost estimates for individual sandboxes and snapshots in Granular usage. Filter by workspace, date, and resource type, and export the breakdown as CSV.
* New custom apps open the preview panel when Polly starts writing files. The unfinished first draft stays covered until generation completes and the preview is ready.
* Custom app previews show an animated loading illustration while starting, with a static version for reduced motion. Published previews fade in when ready.
* Pasting an ECR repository or image URL keeps AWS IAM role authentication available. Registry forms explain that the registry hostname is saved and repositories are selected when creating a snapshot.
* Create sandboxes from a shared, read-only catalog of system snapshots: system/default:latest, system/custom-apps:latest with Smith Apps tooling, and system/code-evaluators:latest with NumPy preinstalled. Choose system or workspace snapshots from the same sandbox and Fleet selectors.
* The system/code-evaluators:latest snapshot includes pandas, jsonschema, SciPy, and scikit-learn alongside NumPy, so evaluators can use ACE's supported Python packages without installing them.
* A sandbox calling the API under an access-delegation grant can still create sandboxes, but can no longer give one a grant of its own. Audit entries for a delegated call now name the sandbox that made it.
* A sandbox's service URLs can now be listed, showing which ports are shared and how, and sharing can be turned off for one port or all of them. Previously a service URL could be created but never inspected or withdrawn.
* An app served behind a LangSmith-login service URL now receives the signed-in user's id and email as X-Langsmith-User-Id and X-Langsmith-User-Email. The signed X-Langsmith-User-Token carrying the same identity is unchanged, and remains the right choice for an app that needs to verify it.

## Administration

* You can revoke and reinstate personal access tokens directly from the API Keys table in Settings. Reinstatement preserves the token's expiry date, and expired tokens show a disabled Reinstate key action with an explanation.
* Revoking a personal access token preserves its original expiry. Reinstating the token restores access only while that expiry remains valid.
* Adds a reusable ThinkingState component for AI activity, with three animation variants, an opt-in elapsed timer, and reduced-motion support.
* Agent Auth automatically registers MCP OAuth clients that require client-secret authentication, storing their credentials securely alongside existing public-client support.
* Managed Parallel tools require a paid workspace plan. Tool calls returning HTTP 200 record usage at 1,000 calls per LangSmith Unit.
* Agent-auth principal creation accepts provider and subject without an issuer. Omitted or null issuers use an empty namespace, while supplied issuers retain their existing validation.
* Browser Back retains navigation guards when returning to the initially loaded page, including cleanup of empty, undeployed custom apps.
* Open Notifications in the sidebar to view platform announcements and account notices without interrupting your work. Incident alerts remain at the top of the page.

### LLM Gateway

* Group LLM Gateway usage by Model Provider within an API key or user to compare spend across providers and filter to specific providers.
* The Gateway provider search field now uses a more comfortable height while remaining aligned with standard component sizes.
* Gateway requests now log traces only to the shared gateway project instead of also creating duplicates in API-key or user-specific projects. Existing caller-specific projects and their historical traces remain unchanged.
* The LLM Gateway now supports direct passthrough requests to TypeSafe's System One API using workspace credentials.
* LangSmith applies configured LLM Gateway guard policies to TypeSafe System One prompt state before forwarding requests.
* LLM Gateway traces for TypeSafe Jev calls now include token usage and calculate costs at TypeSafe's published rate.
* LangSmith now supports TypeSafe in model access policies and provides System One examples for direct Gateway requests.
* Gateway data protection now scans string values throughout nested TypeSafe System One state objects and arrays, including fields such as name, id, and instructions. Redaction preserves the native payload structure for both Gateway Credits and bring-your-own-key requests.

**September 7-14, 2026**

## Observability and evaluations

### Feedback

* Feedback in annotation queues are now attributed by whichever identity the request resolves, so a reviewer's own answers count toward required fields.
* When a score sent through the SDK violates the workspace feedback key configuration, multipart ingest now accepts the request and records error feedback on the run with the rejection reason in the comment, instead of returning a 400 that dropped the run and every other feedback sent with it.
* The annotations pane notes now work when the session\_id is invalid, but a valid trace\_session\_id is provided.

### Engine

* Engine issue validation now reconstructs prior thread turns before replaying a trace, so follow-up failures are judged in the same conversation context.
* Engine issue validation now retries when preparing replay traces hits a Runs API rate limit, instead of treating that as a permanent failure and leaving the result inconclusive.

### Tracing

* Starting September 14, 2026, traces ingested into LangSmith SaaS with extended retention are kept for at most 180 days. Existing extended retention settings above 180 days are applied as 180 days for new traces, and new settings above 180 days are rejected. Self-hosted and BYOC deployments are unchanged. [Learn more](../../../Monitor/Trace/Configuration%20%26%20troubleshooting/Usage%20and%20billing.md#data-retention).
* Chat on a tracing project now reads the filters, view, time window and selection you have on screen, names runs and threads by what was asked rather than by the app that served them, and says what it is working through while it reasons.
* Interacting with LangSmith Chat in the sidebar, including conversation history and model selection, keeps the peeked run or thread pane open. Clicking outside the pane and chat still dismisses the pane.
* Model configurations that set a Vertex AI multi-region location such as `us` or `eu` now reach the correct Google endpoint instead of failing with a 400. Configurations using a single region or `global` are unaffected.
* LangSmith MCP now includes a `list_model_price_maps` tool for searching and paginating model pricing rules in a workspace.
* Trace tree connector lines now join smoothly between rows.

### Prompts and playground

* Switching between files in Context Hub now keeps the selected Preview or Source view.
* Organizations with the LLM auth proxy enabled can select Google Vertex AI models in the playground and Agent Builder without storing a Vertex service account key in the workspace.
* Context Hub repositories now support up to 1,500 files, allowing agents with larger skill collections to sync successfully.
* OpenAI model configuration dropdowns now suggest gpt-6-astra.

### Datasets and experiments

* Trajectory online evaluators now route to the correct applier and receive trajectory input. Malformed configurations surface as visible errors instead of silently producing empty evaluations. When trace retention is enabled, trajectory rules extend retention for the latest trace in each resolved trajectory.

## Deployment

* Find custom apps by name or creator from the custom apps list.
* Updating install or build commands through the deployment API now creates a new revision. Docker sources reject these commands because they deploy prebuilt images.
* After a Managed Deep Agent run paused for credentials resumes, the Slack connect card is removed instead of being replaced with a confirmation, so the agent's reply is the next thing in the thread.
* Managed Deep Agent runs paused on a Slack credential prompt now resume once the last connection completes, instead of stalling after all integrations are connected.

## Sandboxes

* LangSmith Cloud can now assume tagged customer IAM roles for ECR repository discovery and snapshot image pulls.
* Sandboxes now use the guest kernel's maximum open-file limit, allowing highly concurrent agents and subprocesses to run without exhausting the default descriptor ceiling.
* Sandboxes now pass raw TCP connections to literal public IP addresses when the destination IP and port are explicitly allow-listed. This supports clients that resolve a service and dial its public IP directly. [Learn more](../../../Deploy/Sandboxes/Sandbox%20auth%20proxy.md).

## Administration

* Authenticated service startup checks now use endpoint authentication when the deployment info endpoint is protected.
* LangSmith Cloud now warns organization admins in the days before an enterprise contract or a cancelled plan expires, so they can renew before losing access.
* Workspace administrators can view workspace-level Agent Auth connections from the Integrations settings page, including authentication type and update details.
* Workspace administrators can select an Agent Auth connection to inspect its associated credential metadata without exposing secret or token material.
* Built-in workspace roles stop returning the retired repos:\* and run-rules:\* permissions, which were renamed to prompts:\* and rules:\* and are rejected when creating a custom role. Copying a built-in role's permission list into a new custom role now works. [Learn more](../../Govern/Users%20%26%20access%20control/Organization%20and%20workspace%20operations%20reference.md).
* The organization SSO login URL now accepts a `redirect_to` path, so a link like `/sso/login/<slug>?redirect_to=/o/<org>/projects/p/<project>/r/<run>` lands on that page after SAML sign-in instead of the workspace root.
* Organization Operators can no longer grant the Organization Admin role to a service key, or change the roles of a service key that already holds it. A service key also can no longer change its own roles; another credential must make the change.

### LLM Gateway

* GET /v1/models now returns only the models your model access policies allow, so the gateway no longer advertises models that would be rejected when called.
* New model access policies now include a generated policy name that you can keep or edit before creation.
* The LLM Gateway uses each saved model configuration's provider and API preference when selecting a fallback, so Bedrock Claude models use the Messages API instead of an OpenAI-compatible endpoint.
* Data policy dialogs now show a Personally Identifiable Information (PII) option under Data protection for every organization. Organizations without the PII entitlement see it locked, with a link to request access.
* The LLM Gateway returns resolved model names and cost-tracking provider identities in the `x-langsmith-gateway-metadata` response header for unified requests, including configured models and fallbacks. Client-side tracing can use these values as `ls_model_name` and `ls_provider` for accurate pricing, while preserving normalized pricing model names across fallbacks.
* Model Access policies can now allow a workspace's saved model configurations, either all of them or a chosen few, by enabling the new "Model configurations" provider. Requests that reach a configuration, including fallback candidates that resolve to one, are permitted for the calling credential's workspace, where previously any Model Access policy blocked them.

**August 31-September 7, 2026**

## Observability and evaluations

### Automations

* Configuring an evaluator with a trace or tree filter no longer times out while loading the sample run shown in the preview.

### Datasets and experiments

* The add-to-dataset popup for threads now offers New Dataset, which creates the dataset empty and adds the selected threads to it.
* Requesting dataset runs with a limit above 100 now returns a 422 naming the cap instead of a generic internal error.
* Mapping an evaluator prompt variable to a single message, such as `output.messages[0]`, now renders that message instead of an empty value.
* Validating examples with unsupported completion outputs now reports a schema validation error instead of failing with an internal error.
* Passing a malformed share token to the shared-dataset projects endpoint now returns a validation error naming the bad value instead of an internal error.
* Trajectory batch reads now run on a dedicated in-cluster gRPC service instead of the `smith-go` monolith, so load and memory pressure from trajectory evaluations no longer competes with UI and API traffic.
* Dataset CSV and JSONL exports now require both dataset read and download permissions. Direct API requests without download permission return a forbidden response.
* IssueBench now includes a benchmark task that compares pre- and post-Opus 5 agent traces for cost and trajectory regressions.
* Dataset experiments launched from edited Hub prompts save portable Gateway model configurations while preserving the variable mappings used for execution. Saved drafts exclude runtime credentials and remain compatible with standard LangChain SDKs.
* Editing surfaces such as evaluator forms, playground prompts, and dataset examples no longer error out when the editor unmounts while its content is still refreshing.

### Engine

* When Engine marks an issue as a duplicate, the issue header now shows a Duplicate link to the original instead of a history note that included the other issue's id.

### Prompts and playground

* Requesting, updating, or deleting a playground model configuration with a malformed ID now returns a validation error naming the bad value instead of an internal error.
* Sending a null artifact to the prompt canvas now returns a 422 naming the missing field instead of a generic internal error.
* Context Hub now opens markdown files in Source mode on the exact bytes stored in the repo, and saving a change no longer rewrites files you did not edit. Previously, the rich-text editor reserialized every markdown file in the directory on load, which could strip XML-style delimiters and add backslash escapes to untouched content.
* Claude Fable 5.1 is now available in the Anthropic, Bedrock, and Vertex AI model selectors in the playground.
* Prompts saved with a LangSmith Gateway model now use a standard ChatOpenAI manifest with the unified Gateway URL and a `LANGSMITH_GATEWAY_API_KEY` secret reference, so they can be pulled and run with standard LangChain SDKs.
* Amazon Bedrock models in the Playground now expose the same request timeout and max retries options as other providers, so long-running agent calls are no longer cut off at the AWS client default of 60 seconds.
* Gateway presets retain their model settings and stay selected when reopened without changes. You can explicitly clear a model selection, and new Gateway configurations no longer preselect a model or impose a default output-token limit.
* The Playground now runs saved LangSmith Gateway models, including models with bound settings, through the configured Gateway using the authenticated request context. Ordinary OpenAI and custom-endpoint models keep their existing routing.

### Tracing

* The thread header now has Add to dataset and Add to annotation queue buttons in every thread view, including Messages, Turns, and Details, so a whole thread can be added without selecting a run.
* Use the new `/v2/threads/stats` endpoint to retrieve thread and trace counts, latency, token, cost, and feedback statistics for a tracing project.
* Thread query clients can request server-sent events to receive results progressively while preserving cursor pagination.
* Use `/v2/threads/stats` on self-hosted deployments backed by ClickHouse, including when SmithDB queries are disabled. Scoped trace and thread filters still require SmithDB and are ignored otherwise; tree filters are best-effort.

## Deployment

* When a Slack channel event fails before reaching your Managed Deep Agent, for example a dropped delivery, a missing bot token, an interrupt that cannot be shown, or an ambiguous route, it now surfaces in `mda logs` and the deployment logs UI instead of failing silently.
* LangSmith MCP connectors use Client ID Metadata Documents when supported, with dynamic client registration retained as a compatibility fallback.
* Agent OAuth connections now show a provider-branded result page after authorization, making successful and failed connection attempts clearer.
* Managed Deep Agent channel replies now name a missing workspace connection and show how an agent developer can configure it, instead of reporting only a generic run failure.

## Sandboxes

* Commercial private ECR registries can now assume an AWS IAM role on demand, enabling repository and tag search while avoiding expiring saved authorization tokens.

## Administration

* Self-hosted LangSmith operators can configure how many days before license expiration the warning banner appears with `LICENSE_EXPIRATION_WARNING_DAYS`. The default remains seven days.
* OAuth authorization sessions now accept `owner_type` and `owner_id`, so a human can authorize a managed credential for either a user or an agent.
* Workspace editors can now assign resources to an Application tag value from Settings > Resource Tags instead of hitting a permission error. [Learn more](../../Govern/Organization/Workspace%20setup/Set%20up%20resource%20tags.md)
* The workspace switcher now accepts workspace IDs in addition to workspace names, making it easier to locate a workspace when only its ID is known.
* OAuth authorization sessions now accept workspace owners, allowing one managed OAuth credential to be shared across a workspace.

### LLM Gateway

* Set `ls_provider` on OpenAI-compatible model configurations to populate trace metadata and match custom models to provider-specific pricing through the LLM Gateway. [Learn more](../../../Monitor/Trace/Tracing%20setup/Manual%20instrumentation/Metadata%20parameters%20reference.md#ls_provider)
* LLM Gateway fallback chains can now advance to the next model when a candidate does not return response headers within a configured timeout. Active response streams continue after headers arrive.
* Gateway requests authenticated with a session or OAuth bearer token retain their authentication and workspace context across internal routing, including model fallbacks. This prevents authentication failures when a request requires another Gateway hop.

**August 24-31, 2026**

## Observability and evaluations

### Tracing

* ABAC policies can grant access to matching project traces.
* Open deployment threads directly in tracing.
* Clearer Engine issue actions now appear on traces.
* You can read shared threads through the public API.
* Trace and tree filters now apply to thread evaluations.
* Unsupported run filters now return clearer errors.
* Studio Trace nested run selection now works correctly.
* The Gateway usage view can open filtered traces.

### Datasets and experiments

* Experiment evaluator column names now use the full column width.
* You can clone model configurations.
* Tuned Evaluators are easier to find in tracing projects.
* Data grids now adapt to enlarged browser fonts.
* Form errors are announced consistently.
* The dashboard crosshair stays synchronized across charts.
* The Engine chat launcher now suggests questions.

### Engine

* Engine now uses application-scoped project counts.
* Create existing Engine issues in Linear.
* You can open a pull request for an Engine issue straight from the toolbar.
* Engine issues stay in sync with Linear.
* Engine now shows a release announcement in the sidebar.
* Engine now distinguishes a missing capability from an errored or partially wired tool, reducing false-positive Feature Gap issues.
* Pull requests for Engine fixes now open automatically.
* Opening a second linked trace from an Engine issue now works reliably.
* Open PR also works for fixes that have fallen behind the base branch.
* Engine usage now costs 40% fewer Usage Credits.

### Gateway

* Newer OpenAI models now route through Amazon Bedrock.
* Trailing slashes now work on LLM Gateway routes.
* Recursive LLM Gateway configurations are now prevented.
* PII redaction is now a separate LLM Gateway entitlement.
* Claude Max OAuth traffic is now excluded from Gateway spend.
* Saved model configurations now work on the unified LLM Gateway endpoint.
* Custom providers now work on the unified LLM Gateway endpoint.
* Gateway data policies are available by default.
* You can use saved model configurations in LLM Gateway routing.
* Gemini Enterprise Agent Platform gateway now supports existing web credentials.
* OpenAI-compatible API base paths are now respected.
* Custom provider configurations become available faster.
* LLM gateway traces no longer capture request and response content by default.
* Long-lived API keys are now available in the Gateway quickstart.

### Platform and deployment

* Dedicated deployments now run at least two replicas.
* Run rules now support Redis cluster-safe mode.
* Thread annotation queues are now available in self-hosted deployments.
* Thread automations can add to annotation queues in self-hosted deployments.
* Sandbox execution timeout errors are clearer.
* Updating a sandbox's proxy config no longer conflicts with a start.

### Fleet

* Fleet sandbox APIs now work with external OIDC auth.
* Fleet computers keep uploaded Excel workbooks locally.
* Check Outlook calendar availability.

**August 17-24, 2026**

## Observability and evaluations

### Datasets and experiments

* Freeform rubric items in an annotation queue now support an optional regex validator. A reviewer's comment that doesn't match the configured pattern is blocked from saving, with an inline error, instead of silently persisting.
* Organization admins can open Tuned Evaluator settings directly from paused evaluator warnings and disabled-toggle tooltips. Other users see guidance to contact an organization admin.
* Annotation queues now support a Data Formatting setting that hides selected JSON paths from a run's Inputs and Outputs while reviewing; pick fields via checkboxes generated from a sample run, or type a path manually. Applies to run items only, not threads.
* Tuned Evaluators are now hidden in BYOC workspaces and self-hosted deployments, where LangChain-managed inference is unavailable.

### Tracing

* Hovering a bar in the trace waterfall view now shows the same run info tooltip as the run tree, including start and end time, time to first token, token and cost breakdown, and tags.
* Insights now recommends GPT-5.6 Terra and Claude Sonnet 5 for thinking, plus GPT-5.6 Luna for OpenAI summarization.
* Opening a trace from an Insights category now keeps the trace pane header inside the pane: the header actions, including Run in Studio, switch to their compact form whenever the pane is too narrow for the full-size buttons.
* LangSmith Chat now reads as a record of what it did. Every tool it runs gets a row naming the action and what it acted on, with the result one click away; a plan appears when it takes one on, and a subagent shows the steps it is working through. Long results fold to a readable height, files and diffs render as files and diffs, and the panel can be resized or docked to the sidebar.
* Add a guard in the langchain and anthropic trajectory extractors to prevent errors when a run's messages field isn't stored as a list, consistent with the vercel and otel adapters.
* Insights category names that do not fit in the table column now show their full text on hover.
* Insights table columns can now be narrowed beyond their header labels, with full header text available on hover when truncated.
* Thread detail panes now slide into view consistently when opened from a tracing project.
* Opening a shared link to an issue now loads that specific issue, including issues marked as ignored, instead of displaying the first issue in the list.
* Runs using the bare "gpt-5.6" model id now calculate cost correctly. The pricing rule previously only matched the "gpt-5.6-sol" id variant.
* Controlled inputs no longer create redundant local state updates, preventing rare page crashes while typing in tracing filters.

### Engine

* The recurrence chart on an issue now labels its x-axis with a day-and-month axis instead of repeating the month on every tick, runs its window up to the present, and states when the issue was last seen. An issue that stopped recurring months ago no longer looks like one that recurred this morning.
* Copy Fix now pastes diagnosis, linked traces, and LangSmith CLI commands, plus a silent PR marker. When a PR in the connected repo includes that marker, Engine attaches it and shows open, closed, or merged status.
* Each row in the Engine issue list now shows the timestamp the list is sorted by, labeled and right-aligned; "Created 5d ago", "Updated 3h ago", "Seen 11m ago"; in place of the trace count. Hovering any issue date, on the row or in the issue header, shows the created, updated, and last-seen times together.
* The Engine overview no longer shows a duplicate configuration button. Engine settings remain available from the issue board toolbar.
* Sorting the Engine issue board now orders purely by the chosen field (Severity, Last Seen, Last Updated, Created, or number of traces), including resolved and dismissed issues. Status and other filters hide mismatches immediately, and each board remembers its sort and filters in the browser.
* The Fix panel can detach a linked GitHub pull request from an issue without closing it, so a different PR can be attached afterward.
* The issues API accepts a `trace_id` query parameter that returns only the issues with a run linked from that trace.
* Searching the project switcher on the Engine page now matches project names the same way the tracing project list does, instead of returning loosely-related projects.
* A pull request opened from an Engine issue now takes its title and description from the fix run's own commit message, so it explains the change a reviewer is looking at instead of restating the issue report. Every fix PR also links back to the issue it came from.
* The sidebar no longer displays the Try Engine promotional popover over the Tracing link.
* Listing Slack channels for a workspace with tens of thousands of conversations needs more than one of Slack's rate-limit windows. The background refresh now has a budget that spans them, so the picker fills instead of staying empty.
* The Slack channel picker for watching alerts now opens toward the left, keeping the full channel list visible within the issue panel.
* The Engine issue list now opens on a Default sort that leads with watched issues that have picked up new traces, then open and fixing work, then quiet watched issues, with closed and ignored ones last. Severity and last-seen order issues within each group.
* The Engine issue list's Status filter now covers triage state only; Open, Resolved, and Incorrectly Flagged; where Open includes issues with a fix in flight or under watch. A new Activity filter selects those independently, so filtering to Open no longer hides issues Engine is actively working on.
* The standalone Engine page now links directly to the selected project's tracing view.
* LangSmith Chat now reads the Issues Board beyond the issue you have open, ranking issues by what to triage first, what fired most recently, or what cites the most traces, and measuring how a board breaks down, recurs, spreads and trends over a period you choose. It also checks an issue against the traces it cites before telling you the failure is real.
* Listing Slack channels stopped after a fixed number of pages, so a workspace with tens of thousands of archived conversations had its channel list quietly cut short. Paging now runs until Slack reports the end of the list.

### Prompts and playground

* Context Hub repositories containing legacy files beneath linked directories can now be read, materialized, cloned, and edited. Reads use the linked directory contents, and the next successful edit removes conflicting legacy entries without changing linked repositories.

### Monitoring and alerting

* Create and edit alert actions now remain in a sticky footer, so you can submit changes without scrolling to the bottom of the form. [Learn more](../../../Monitor/Observe/Monitoring%20%26%20alerting/Alerts%20in%20LangSmith.md).
* The Streaming rate over time template now divides runs with a first token time by LLM runs only, so a new chart matches the streaming rate shown elsewhere in LangSmith.
* Adds a reusable BarChart component to the LangSmith design system, standardizing grouped and stacked bars, horizontal and vertical layouts, multiple value axes, threshold bands, interactions, and keyboard accessibility.
* Webhook test notifications now show the destination's HTTP status and reason phrase, helping you diagnose URL, availability, and authentication failures.

### Automations

* Thread webhook and annotation-queue automations now show thread filters instead of run filters, and no longer default to Is Trace = true.
* Automation rules scoped to threads now show the project's thread idle time, with a link to change it in project settings.

## Deployment

* Studio chat now shows results for provider built-in tools such as web\_fetch and web\_search, and groups a run of consecutive tool calls into a single collapsible entry instead of one row per call.
* Self-hosted deployment forms now preserve fractional CPU request and limit values for application and queue containers.
* GCP Redis IAM cluster discovery now uses TLS when Redis cluster TLS is enabled, allowing self-hosted deployments to combine IAM authentication with TLS-required Memorystore clusters.
* Studio switches deployment and connection controls to compact icons when the graph pane is narrow, preventing toolbar actions from overlapping.
* Deployment Overview now surfaces high Postgres disk usage and pending run counts, so operators can spot issues without opening Monitoring.

## Sandboxes

* Sandboxes now mount Context Hub repositories through a read-only, host-served filesystem, so files are directly accessible without polling for asynchronous guest materialization. Repository updates appear atomically, and mounts recover across memory-backed stop and start.
* Attach a free-form description when creating or capturing a snapshot, and to proxy rules and proxy configs. Descriptions are stored and returned on reads, so you can hand an agent a plain-language summary of what its sandbox image and network access can do.
* Sandbox file downloads now accept a Range header, so you can fetch part of a large file or resume an interrupted transfer instead of starting over. Responses carry an ETag for safe resumes and the same path answers HEAD, reporting a file's size without transferring it.
* You can now mint a signed link that downloads a single sandbox file with no LangSmith credential, so files can be handed to a browser or any client that cannot carry an API key. Links are served from the sandbox service domain, never expire unless you set expires\_in\_seconds, and can pin the response content type and disposition. A link's content is cached indefinitely, so mint a new link when the file changes.
* Sandbox proxy rules and callbacks no longer accept match\_hosts patterns like `*.com` or `*.co.uk`, which would have sent injected credentials to every host under a top-level domain. Wildcards must now name a registrable domain, such as `*.example.com`.
* GET /v2/sandboxes/boxes now pages with page\_size and an opaque cursor, returning items and next\_cursor. The limit and offset parameters and the sandboxes and offset response fields still work but are deprecated.
* Updating a sandbox's proxy configuration no longer requires the sandbox to be running. A stopped sandbox stores the new configuration and applies it the next time it starts, instead of rejecting the request.
* GET /v2/sandboxes/snapshots now pages with page\_size and an opaque cursor, returning items and next\_cursor. The limit and offset parameters and the snapshots and offset response fields still work but are deprecated.

## Administration

* Organization admins can now delete custom roles from the roles settings page. Roles still in use by a user, SCIM group, or SSO settings cannot be deleted until reassigned.
* Each data plane card in organization settings now has a copy button next to its name, so you can grab the data plane ID without opening dev tools.
* Custom roles can now grant feedback-configs:create, feedback-configs:update, and feedback-configs:delete independently of feedback submission, so a role can be scoped to submitting feedback without also being able to create, edit, or delete feedback config (rubric) definitions.
* Billing settings now name the two credit tabs Credit usage (previously Contract usage) and Credit grants (previously Credits). Credit usage tracks burndown against your prepaid gateway credits.
* The Storybook overview now links every component card to its dedicated page and shows accurate progress examples.
* The login CAPTCHA now appears beside the active email or SSO field while preserving entered form values when switching methods.
* Workspace roles can grant API key creation and deletion without granting full workspace administration. Key managers can scope service keys to permitted workspaces and assign unrestricted roles.

### LLM Gateway

* The Gateway Credits balance card now explains that credits access models hosted by LangChain, and the Gateway home quickstart notes that running a request costs a trace but no additional LangChain fee.
* Running a request against Gateway Credits (hosted models) in the Gateway home quickstart now offers to set a monthly spend limit, matching the Bring Your Own Key flow.
* The three cards at the top of the Gateway home page; Spend limits, Model fallbacks, and Gateway usage; are now static orientation content instead of clickable shortcuts, so they read as a quick summary of what LLM Gateway does rather than navigation.
* The LLM Gateway now returns 424 Failed Dependency instead of a generic 400 Bad Request when a required provider API key is absent from workspace secrets. The error response also identifies the missing secret and explains how to resolve it.
* The LLM Gateway browser quickstart now lets you create a monthly workspace spend limit inline, right where you're recommended one, instead of opening a separate dialog.
* The API key modal launched from Gateway home now defaults to a personal access token and hides the service key, key type, and default workspace fields that don't apply to a new Gateway user. Expiration is capped at 30 days.
* Gateway Credits balance, policy spend, and Gateway Monitoring's spend stats, chart, and table now show `&lt;$0.01` for a positive amount under a cent instead of rounding it down to `$0.00`, so a small amount of spend no longer looks like nothing happened.
* The LLM Gateway now forwards Claude Code Max OAuth credentials for every organization, without requiring a workspace Anthropic API key.
* LLM Gateway spend controls and data protection policies now open in focused side panes, keeping actions visible in the header and warning before unsaved changes are discarded.
* Gateway traces now carry a `gateway.credential_source` metadata field naming the credential that paid for each upstream LLM call (`credits`, `byok`, `subscription_oauth`, or `platform_managed`), allowing you to filter and chart Gateway Credits usage separately from bring-your-own-key usage, plus a `gateway.provider` field naming the provider route that served the call.
* Default gateway spend and rate limits can track and enforce separate buckets for each value of a configured X-Gateway request header.
* LLM Gateway rate-limit creation and policy editing now use focused side panes with unsaved-change warnings. New policies receive descriptive generated names, and optional custom-header conditions are grouped under an advanced section.
* Gateway spend limit forms can configure custom-header buckets, and cost policy tables show which header separates each default limit.
* The LLM Gateway now supports xAI API keys and Grok models through native and unified Responses and Chat Completions endpoints, with tracing and spend attribution. [Learn more](../../../LLM%20Gateway/Get%20started/LLM%20Gateway.md).
* LLM Gateway fallback policies can now route failed provider-model requests through an ordered chain of native provider models and saved model configurations. Configure which HTTP status codes advance to the next candidate, while successful requests continue directly to the original model.
* The Model Fallbacks tab now lets you create and manage automatic fallback chains for provider models. Choose ordered backup models or saved model configurations, select which HTTP errors trigger fallback, and copy a ready-to-use Gateway request example.
* LLM Gateway model fallback policies can now route between providers that use OpenAI Chat Completions, OpenAI Responses, or Anthropic Messages formats. The gateway translates requests, non-streaming responses, and streaming responses for both unified and direct provider endpoints.

**August 10-17, 2026**

## Observability and evaluations

### Datasets and experiments

* Annotation queue tables now label queue contents as items instead of runs, covering both single-run and pairwise queues.
* Datasets whose input, output, or metadata keys contain a colon can now be exported to CSV. This unblocks datasets built from runs with feedback, where feedback is stored under a `source_run_feedback:<key>` metadata key.
* Managed evaluator configuration no longer shows evaluator tracing controls.
* The Datasets & Experiments table now labels dataset names with a Dataset column header, making the relationship between datasets and experiments clearer.

### Monitoring and alerting

* In dashboards and other surfaces where "All time" is unavailable, clearing both dates in the date picker now disables Apply instead of silently submitting an all-time range that fails to load.
* Opening a run from a dashboard chart's runs table now shows a single trace pane instead of stacking a second, identical pane behind the first.

### Automations

* Online evaluators configured with a saved custom provider model configuration (OpenAI-compatible or Anthropic-compatible) now use that configuration's endpoint and credentials on live traces instead of failing with a permission error.
* Non-admin users can now save evaluator edits from the dataset, tracing project, and thread panes without hitting a retention-permission error.
* Automations grouped by thread can now add one annotation queue item for each matched conversation, so reviewers can inspect the whole thread instead of only one run.
* Thread webhook and annotation-queue automations now show thread filters instead of run filters, and no longer default to `Is Trace = true`.

### Engine

* The Slack channel list now refreshes in the background even when Slack rate-limits the request, so large workspaces no longer lose picker options.
* Engine fix runs no longer push a branch for every code fix. The commit is parked on a hidden ref and the branch is created when you open a pull request, so connected repositories keep a clean branch list.
* Engine now highlights only Slack notifications in its announcement area and continues to honor prior dismissals.
* Unread Engine issues now show a lighter brand pip aligned to the right of the title, so new issues are easier to scan without competing with the title.

### Tracing

* The Turns view in thread detail is deprecated in favor of the Messages or Details view, and LangSmith Cloud removes it on October 31, 2026, while self-hosted removes it in v17.
* Thread annotation-queue and webhook automations now require SmithDB queries.
* LangSmith Chat now offers GPT-5.6 Sol, GPT-5.6 Terra, and GPT-5.6 Luna alongside the existing OpenAI models.
* LangSmith now recognizes older trace links containing timestamp-prefixed run and trace IDs.
* The tracing quickstart now opens with Deep Agents selected and leads with Deep Agents, LangGraph, and LangChain framework guides.
* Trace details now surface LLM Gateway outcomes, policy limits, selected models, and fallback attempts in a dedicated Gateway section. Errored LLM runs blocked by the gateway also show a Blocked badge in the trace tree.

## Deployment

* LangSmith services now accept both IPv4 and IPv6 connections.
* Deployments now resolve the latest agent server version more reliably, preventing slow revision creation and duplicate revisions caused by request timeouts, especially in Asia Pacific.
* LangSmith workers using Microsoft Entra ID authentication for standalone Redis now start successfully and continue refreshing credentials after the event loop starts.

## Sandboxes

* Mounting a git repository into a sandbox no longer fails silently. Clones now trust the sandbox's certificate bundle, so the repository appears at its mount path instead of starting in an empty directory.
* Sandboxes now retain recent CPU, memory, and network usage history, making it easier to understand resource consumption and diagnose performance bottlenecks.
* WebSocket connections through a sandbox service URL now reach your service with their query string intact. Dev servers that authenticate their own WebSocket with a query parameter, such as Vite's HMR token, now connect instead of failing.

## Administration

* The signup page animation stays aligned with the hero content after the confirmation message appears.
* Users with the tag-on-create permission for datasets, projects, or prompts can now see and apply tags when creating those resources, instead of only workspace managers.
* The API Keys page now filters keys across the full paginated list by key, description, and workspace.
* The organization usage dashboard renders its charts again; they previously could appear blank even when usage data was present, showing only the workspace legend.

### LLM Gateway

* Requests to Bedrock models through the unified LLM Gateway now use the API format supported by each model family. Anthropic models use Messages, OpenAI models use Responses, and other Bedrock models use Chat Completions, preventing unsupported API errors for models such as Claude Opus.
* The LLM Gateway can now reach Amazon Bedrock with an assumed IAM role or AWS access keys instead of a static Bedrock API key, and existing Bedrock API keys still take precedence when multiple credential types are configured.
* The LLM Gateway quickstart now hides the Run request action for workspace members without gateway invocation permission.
* LLM Gateway responses now include an `X-LangSmith-Gateway-Metadata` header describing gateway routing, limits, guard activity, and upstream errors, and clients can attach it to their own traces as `ls_gateway_info` metadata.

**August 3-10, 2026**

## Access control

* Access-policy endpoints now report errors as RFC 7807 problem details. Error messages move from the `error` field to `detail`, and semantically invalid request bodies return HTTP 422.
* Set a resource tag key or value description to `null` to clear it through the PATCH API.
* New connections to the hosted LangSmith MCP server failed to register when the client requested a confidential authentication method. Dynamic client registration now issues a public client in that case instead of returning an error, so connecting from Claude and other MCP clients works again.
* Role permission and access policy changes now invalidate cached authorization results reliably, including when an older transaction commits after a newer update.
* LangSmith now refreshes cached role access policies as soon as their permissions change, preventing stale authorization decisions in split-plane deployments.
* The Active, Pending, and Deactivated tabs on the Members settings page now switch on the first click while keeping pagination and sorting in sync.

## Datasets and experiments

* Attachment and object downloads now always declare how the browser should handle the response. Files whose type is unrecognized, or that were stored without a type, are delivered as downloads instead of being rendered in the page.
* Creating a dataset from the Datasets or Home empty state now opens the new dataset instead of briefly showing a Page not found screen.
* Dataset JSON schema descriptions are now safely rendered in editor tooltips.
* Creating or validating an example with a `dataset_id` that is not a well-formed UUID now returns a 422 naming the field instead of a 500.
* Listing or counting examples with an unsupported `filter` expression, an unfilterable attribute, or a `has(...)` comparison whose value is not valid JSON, now returns a 422 naming the `filter` parameter instead of a 500.
* Creating an experiment no longer converts an existing tracing project with the same name. Rename the experiment or choose a new project name when a conflict exists.
* Scrolling through large experiment comparison results no longer re-fetches the first page of examples on every lazy-load, cutting redundant network traffic and reducing load time.

## Monitoring and alerting

* Chart headers on dashboards no longer overflow or wrap when the title or description is long, the description now truncates with a hover tooltip that reveals the full text. The expand-chart action also picks up the standard icon-button hover treatment.
* Alert previews now treat integer metadata and its string representation consistently with alert evaluation.

## Engine

* Disabling Engine for an organization or pausing it for a project now offers a short prompt asking why, with an optional comment. It takes one tap and goes straight to the team building Engine.
* Engine spend controls now explain that new runs pause at the monthly limit while runs already in progress may finish and increase billed spend beyond it.
* The Engine tab is visible again on tracing projects before Engine is turned on, so admins can enable it, members can request access, and personal organizations can upgrade, all from the tab itself.
* Engine GitHub settings now link to setup instructions for LangSmith Cloud and self-hosted deployments, with clearer guidance when a connection fails.
* Engine scans on non-coding-agent boards apply the configured priority chips, user instructions, and trace-scope filter instead of reviewing the whole project.
* Engine issue descriptions now preserve Markdown paragraph boundaries so updates, additional symptoms, and corrections remain easy to scan.

## Feedback and evaluation

* Feedback corrections can now reset a score to its original value, including zero.
* Group by metadata and metadata columns are selectable again in the experiment comparison view.
* A long evaluator name in a feedback card's Source row now truncates instead of extending past the card, and a corrected score keeps its edit control clear of the paging arrows when a key has several entries.
* Switching a feedback value to a different category now saves even when both categories map to the same numeric score. Previously the change was silently dropped on run details and in annotation queue rubrics.
* The pencil for correcting an evaluator score is now hidden unless you have permission to update feedback. Previously it appeared for anyone who could see the score, and saving the correction failed.
* LangSmith now rejects credential-bearing and non-GitHub remote URLs when rendering evaluation commit links.
* Attachments stored on a run now appear when you review it in an annotation queue, including pairwise queues. Previously only media inlined in the run's inputs or outputs was shown.
* The evaluator spend table keeps the All runs filter badge inactive when an evaluator has no filters.
* Daily evaluator spend, weekly totals, and spend limit monitoring on the Evaluators page now respect the currently selected application, instead of showing data across all applications.
* The evaluator spend chart once again keeps its evaluator and project/dataset grouping control in the chart header for easier access.

## Tracing and observability

* Chat model runs sent through the gateway's unified endpoint with provider/model slugs now match model pricing rules, producing accurate trace costs.
* Insights reports only analyze traces, so the "Is Trace" condition in a report's filter is now fixed. Setting it to false previously produced a report that ran successfully but never found any insights.
* LangSmith Chat now respects the Provider API setting on workspace OpenAI model configurations. Models configured for the Responses API no longer fall back to Chat Completions, which made newer reasoning models fail when a reasoning effort was set.
* Large PDF, JSON, and CSV previews on a message now render instead of showing an empty frame, and PDF and JSON previews gained an open-in-new-tab control next to the expand control.
* Trace views now source token and feedback stats from SmithDB without attempting unavailable ClickHouse queries.
* Waterfall filters in thread details now keep deeply nested matches visible and preserve filter controls while newly ingested traces are still appearing.
* LangSmith MCP's `fetch_runs` tool can now include invocation parameters, including the tool and function schemas sent to an LLM, for easier tool-calling diagnosis.
* PDF attachment icons now align consistently with other file types in attachment lists.
* The thread query API now supports trace, run-tree, and thread-level filter expressions through `trace_filter`, `tree_filter`, and `thread_filter`.
* Public shared-trace links now show a 'temporarily unavailable, try again' message when the trace query times out, instead of the misleading 'trace not found, ask the owner to re-share' message.
* Clicking a starter prompt without the selected model's API key configured now shows the add-a-key form, the same as typing a message, instead of failing the request.

## Prompts and playground

* Claude models on Gemini Enterprise Agent Platform now load successfully in the Playground when no credentials secret is configured, matching existing Gemini behavior under GCP Workload Identity or AWS IRSA.
* The Prompts page now supports filtering by prompt type, prompt tags, and commit tags, so you can quickly narrow the list down to the prompts you're looking for.
* Model configurations now show an inline error, instead of a silent save, when a required Bedrock, Azure OpenAI, or Gemini Enterprise Agent Platform provider field is left blank.
* Studio's chat pane no longer shows a 'No data' placeholder between sending a message and the first streamed token. The assistant message now appears once it has content to show.
* The Playground now reports missing AWS credentials and other Bedrock rejections as request errors with the provider's own message, instead of a generic server error.
* Studio chat now shows elapsed response status, preserves complete streamed responses, and follows new output without interrupting readers who scroll up.

## Automations

* Manually triggering an automation rule through the API now works. `POST /runs/rules/{rule_id}/trigger` and the `rule_ids` form of `POST /runs/rules/trigger` previously returned a 500 for every request.
* You can manually trigger any automation in your workspace, including webhook-only, alert-only, and extend-retention rules. Previously the trigger endpoint only recognized a subset of actions and returned not found for the rest.
* Online evaluators configured with an OpenAI-compatible or Anthropic-compatible custom endpoint now use that endpoint's own URL and API key on live traces instead of failing with an authentication error. Evaluators on custom endpoints are not counted toward evaluator spend limits.

## Deployment

* Self-hosted deployment forms now support Redis CPU and memory requests and limits. The configured values are applied to the Redis workload managed by the Kubernetes operator.
* Deployments that use a platform-default LangGraph API version now correctly reuse matching images instead of starting unnecessary rebuilds.
* Managed Deep Agent deployments entering public preview report their normal deployment usage.
* Rolling back a deployment that was created from an uploaded source archive now redeploys that revision's archive instead of the most recent one.
* A Managed Deep Agent deployment's Details sidebar now links to the Context Hub repo holding its deployed instructions, skills, and memories. Archived repos are labelled so it is clear when the context is no longer live.

## Sandboxes

* Resuming a suspended sandbox now checks your organization's real sandbox quota, including plan-specific limits, instead of the default cap. Requests that genuinely exceed quota return 429 with a quota message rather than 502 Bad Gateway.
* Self-hosted LangSmith now enables sandbox API and UI access only when the deployment license includes sandbox access.
* Online self-hosted LangSmith installations now report finalized sandbox uptime and resource usage for billing when phone-home usage reporting is enabled. Offline and opted-out installations do not send sandbox usage.

## Administration

* The organization submenu now opens when you hover over the organization row in the footer menu.
* Self-hosted deployments refresh their license every 5 minutes instead of every 24 hours, so entitlement changes take effect shortly after they are made. A failed refresh no longer restarts the service, it keeps using the last verified license until that license's own expiry. The tuning knob is now LICENSE\_REFRESH\_INTERVAL\_SECONDS (default 300), replacing LICENSE\_REFRESH\_INTERVAL\_HOURS.
* Searching workspaces with Cmd+K now highlights the query in the organization heading, making it clear why a term that matches an organization name returns all of that organization's workspaces.
* The account menu now offers Get help. Enterprise users can submit a support request in LangSmith, while other cloud users are directed to the Support Portal.
* The Plans and pricing page now preserves browser back and forward trackpad gestures and centers the plan cards.

## LLM Gateway

* Requests to moonshotai/kimi-k3 and moonshotai/kimi-k2.6 through gateway credit models in the LLM gateway are now matched against a price map when sent in user-traced code.
* LLM Gateway Usage now provides interactive spend legends, consistent chart layouts, and tooltips that stay visible. Single-series views clearly explain spend that is not affiliated with a user instead of showing an empty chart.
* You can now purchase as little as \$4.50 in Gateway Credits, equivalent to 3 LCUs.
* Bedrock requests through the LLM gateway now use the Amazon Bedrock price map so their costs are calculated correctly.
* The credit balance now shows above the connect card, and the shortcut cards for cost controls, model fallbacks, and spend monitoring stay visible (locked, with an "Upgrade plan" prompt) instead of disappearing for Developer-plan orgs.
* The Cost Controls, Rate Limiting, and Model Fallbacks tabs now explain what isn't in force yet, with a create button and a docs link above the policy tables. Each tab's create button, dialog title, and submit button also share one label, such as "Create spend limit" instead of a generic "Create policy".

**July 27-31, 2026**

## Observability and evaluations

### Datasets and experiments

* LangSmith exposes annotation queue item endpoints for adding, listing, updating, deleting, counting, positioning, and reviewing run or thread queue items through the public API and SDK generation flow.
* Uploading a .csv or .jsonl dataset now works regardless of the Content-Type the browser reports. Windows browsers label .csv files as an Excel type, which previously caused valid uploads to fail. Uppercase filenames such as DATASET.CSV are also accepted.
* Evaluator lists on a dataset or tracing project now show an evaluator's current name instead of the name it had when it was attached. Feedback keys are unchanged by a rename.
* Metadata columns in the experiment comparison grid, including `example.metadata.<key>`, now render their values instead of staying empty.
* LangSmith marks every legacy endpoint replaced by the SmithDB SDK migration guide as deprecated: the v1 runs query and retrieve endpoints, the v1 run sharing and public-run read endpoints, `POST /api/v1/datasets/{dataset_id}/runs`, and the annotation queue run endpoints. All of them now respond with `Deprecation: true`, a `Sunset` date of January 31, 2027, and a `Link` header pointing at the migration guide and, where a single replacement exists, the successor endpoint. [Learn more](../../../Monitor/Reference/SmithDB%20API%20migration/Migrate%20to%20SmithDB-backed%20APIs.md).
* Dataset experiment tables can sort by feedback score when SmithDB queries are enabled and ClickHouse queries are disabled.
* Annotation queue item APIs use project\_id for the tracing project. Request bodies also accept session\_id as an alias.
* Dataset example views restore clear spacing between the example details and tab navigation.
* Pairwise annotation queue runs again include the tracing project id needed to create feedback when ClickHouse query support is disabled.
* Correcting an evaluator score from the experiment results grid now updates the cell and its popover right away instead of requiring a page refresh.
* The Configure Evaluator pane's header and templates navigation again paint the same background as the pane itself in dark mode.
* Dataset and run attachments now resolve relative signed download URLs before previewing, opening, or downloading them in self-hosted deployments.

### Monitoring and alerting

* Adds a reusable ChartCard component to the LangSmith design system, standardizing chart titles, move, expand, and overflow actions, responsive full-width layouts, and chart and legend spacing.

### Engine

* A resolved issue on an Engine Issue Board now returns to Open as soon as Engine links a new matching trace to it. Previously the trace was filed as evidence but the issue stayed closed, so a problem that came back never resurfaced on the board. Dismissed issues stay dismissed.
* The issue detail header now renders category and tag badges on the same line as the title instead of stacking them underneath, tightening the header and reducing wasted vertical space.
* The "Engine failed to complete a run" trigger is no longer offered when configuring a Slack channel or webhook destination on an issue board. Destinations already subscribed to it keep receiving those notifications.
* Engine run webhooks and sandbox links now resolve the externally reachable API base from LANGSMITH\_PUBLIC\_API\_ENDPOINT, falling back to LANGCHAIN\_PLATFORM\_ENDPOINT and then LANGCHAIN\_ENDPOINT. Installs whose chart set only LANGSMITH\_PUBLIC\_API\_ENDPOINT were building relative URLs, which made every non-shadow Engine run fail because the run webhook was rejected as a loopback address.

### Tracing

* Trace detail panes once again use an elevated background that matches their section headers.
* Bulk exports accept a new opt-in `feedbacks` column that carries each run's individual feedback entries, with their key and comment, as a JSON array. Add `feedbacks` to `export_fields` when creating an export; exports that omit `export_fields` keep their existing columns.
* Delete an entire trace from the run details actions menu after confirming the destructive action.
* Negative feedback-key filters now return matching traces correctly when ClickHouse uses optimized runs tables.
* When a project configures a custom output renderer, the trace Output section now offers it as a Custom option alongside Markdown, Plain, JSON, and YAML instead of replacing them. Custom stays the default, and your choice is remembered.
* Tracing project activity and sorting stay up to date for self-hosted deployments using Redis versions before 6.2.
* `POST /api/v1/runs/stats` now returns a 404 when the requested tracing project does not exist in your workspace, and reports other client errors, such as a `start_time` older than the supported lookback window, with their real status and message instead of a generic 500 internal server error.
* Self-hosted deployments now catch up missing tracing project last-run timestamps so project sorting reflects recent historical activity.
* Run filters now support total, prompt, and completion token counts and costs consistently across routed query backends.
* Token Count / Cost filters now default to total tokens / cost instead of input tokens. Input and output token / cost breakdowns remain available in the selector.
* On a tracing project, resetting a view now moves the Threads/Traces/Runs switcher back in step with the rows being shown. Previously the switcher could stay on Runs while the table had already returned to traces.

### Feedback

* The annotation queue item endpoints are now documented at their served path under /api/v1/platform, so the generated SDK methods for listing, adding, updating, counting, deleting, and placing queue items reach the API instead of returning 404.
* PDFs and other documents attached to a message now render in a full-width preview frame with a header control that opens them nearly full screen, instead of collapsing to a thumbnail-sized box.

### Prompts and playground

* When a model provider rejects a playground run, such as a wrong API key or an exhausted quota, the playground now shows the provider's own error message instead of a generic server error, so the cause is clear from the error itself.
* Playground batch and invoke endpoints now sanitize buffered run trees into JSON-safe payloads before responding, so online evaluations no longer fail with opaque 500s when a run graph cannot be serialized.

### Automations

* Forking an evaluator attaches the copy to the project or dataset named in the fork dialog. Previously the copy could be created attached to nothing, leaving the original evaluator running the version you had just edited away from.

## Deployment

* The Create New Deployment form now shows a clear, per-field message when a submitted value fails validation (e.g. an invalid image path) instead of the raw backend error payload.
* Deleting a tracing project whose LangGraph deployment is still within its post-deletion retention window now schedules the project to be removed along with the deployment, and explains that in the error message instead of asking you to delete a deployment you already deleted.
* The delete confirmation for a LangGraph deployment now says that cleanup of the underlying database runs after you confirm, and that a deleted deployment's name stays reserved until that cleanup finishes.

## Sandboxes

* Sandboxes accept a new streaming execute request that returns stdout and stderr as Server-Sent Events, for clients that cannot hold a WebSocket. Passing a command ID reuses a running command, and a separate resume request continues an interrupted stream instead of running the command again.
* Sandboxes now ship with the `langsmith` CLI on PATH, so agents can query traces, runs, and datasets without installing it first.
* Sandbox and snapshot rows now use single-column layouts with actions in context menus, snapshot sources remain available in their menus, and wrapped names stay left-aligned.
* Engine sandbox commands in self-hosted deployments now authenticate over WebSocket with the deployment service key, preventing 401 failures after successful sandbox creation.
* The `langsmith` CLI in sandboxes is updated to v0.2.44. Its requests now resolve on self-hosted deployments that serve the API under `/api`, where commands such as `trace messages` and the project issues commands previously failed.

## Administration

* The LangSmith home page now provides quick access to copy the current organization and workspace IDs.
* On self-hosted installations authenticating with OAuth/SSO, the Remote MCP authorization endpoint returned a 400 because the SSO login route shadowed it. OAuth clients can now complete the authorize step and connect to the Remote MCP server.
* Self-hosted deployments with an online license key (beacon access) now see the monthly organization usage graph automatically, without needing the enable\_monthly\_usage\_charts org config. Offline deployments are now pointed to the Granular usage tab for locally-recorded billable usage.
* Switching workspaces or organizations keeps you on the same page when the route has no workspace-specific resource IDs. Routes that reference a specific resource continue to open the destination workspace home page.
* LangSmith now refreshes expired browser sessions and retries interrupted API requests before asking you to log in again.

### LLM Gateway

* Gateway policies with a blank or whitespace-only name now fall back to showing the policy ID instead of rendering an empty name cell, and the policy update endpoint now rejects blank names the same way creation already does.
* The Gateway usage spend chart now shows the top 12 individual spenders per bucket, rolling the rest into an "Other" series, and its hover tooltip lists every contributor at once with the bucket total pinned beneath them.
* The home page onboarding flow now includes a step for choosing how your agent reaches a model: bring your own provider API key, or use Gateway Credits. Choosing Gateway Credits lets an organization admin pre-purchase prepaid credit and shows the API key and gateway URL needed to start sending traffic, with no provider account required.
* The custom X-Gateway-\* header condition on LLM Gateway spend-cap and rate-limit policies now works with organization-, workspace-, and user-scoped policies too, not just API-key-scoped ones, so you can split a single subject's traffic into separate caps by header value regardless of how the policy is scoped.
* Default spend cap and rate limit policies in LLM Gateway now expand to show the per-user, per-workspace, and per-API-key policies materialized underneath them.
* The Gateway Credits purchase dialog now shows the credit balance your purchase will land you on, and states the fee-inclusive total directly above a single purchase button. Large amounts no longer push the credits readout and total outside the dialog.
* Enterprise organizations without Data Protection now see the tab in the LLM Gateway, greyed out with a link to request access, instead of the tab being hidden entirely.
* The connect card now appears above the Gateway Credits balance on the LLM Gateway Home page, and the generated code snippets list the API key before the base URL to match common convention.
* Generating an API key from the LLM Gateway Home connect card now shows the standard one-time key reveal dialog, and each provider's "Configured" status now reflects the workspace's actual secrets instead of a fixed list.
* The "Purchase Credits" button on LLM Gateway Home now opens the credit purchase dialog instead of showing a "coming soon" message, and the balance bar now shows spend against what's actually purchased instead of against the plan's purchase limit.
* The Cost Controls and Model Fallbacks shortcuts on LLM Gateway Home now read "View cost controls"/"View model fallbacks" for members who can't manage the org, instead of "Manage"/"Configure".
* Gateway Home code samples now use the gateway hostname constructed for each LangSmith region and default to the Responses API where supported. [Learn more](../../../LLM%20Gateway/Get%20started/LLM%20Gateway.md).
* LLM Gateway policy tabs now clarify that policies apply across the organization, while Usage clarifies that spend is scoped to the selected workspace.
* The home onboarding step now states your Gateway Credits balance in US dollars, matching the amount you purchase, instead of converting it to LCUs.
* The prompt you copy into your coding agent during onboarding now states how the agent should reach a model, based on the provider you picked: Gateway Credits, or your own provider API key.
* Homepage spacing and surface tinting now match design review feedback, and several small copy fixes clarify credit limits, provider status, and organization-level purchase limits.
* LLM Gateway Home again includes Google Gemini and generates valid model identifiers for Gemini and Baseten connect samples. [Learn more](../../../LLM%20Gateway/Get%20started/LLM%20Gateway.md).
* LLM Gateway Home now highlights the selected model and lets you switch connect samples between Chat Completions, Messages, and Responses formats.
* The LLM Gateway Usage tab now explains when usage queries aren't available for a deployment instead of showing failed dashboard requests.
* When you select Gateway Credits during onboarding, the prompt copied into your coding agent now includes the correct Gateway URL for your deployment. [Learn more](../../../LLM%20Gateway/Get%20started/LLM%20Gateway.md).
* Gateway Credits checkout now remains on the active purchase step while a free workspace upgrades to the Developer plan, instead of briefly showing the saved-card view before closing.
* Requests that set prompt\_cache\_options (or the deprecated prompt\_cache\_retention) now enable Anthropic prompt caching when the LLM Gateway translates an OpenAI Chat Completions or Responses request to a Claude model, instead of ignoring the field. Anthropic's default cache lifetime applies, and prompt\_cache\_key, prompt\_cache\_retention, and prompt\_cache\_options are all preserved when translating between the Chat Completions and Responses formats.
* Tooltips on disabled LLM Gateway policy controls now read "You need organization admin access to create policies" instead of referencing the raw organization:manage permission string.
* The Gateway Usage tab no longer shows an in-page workspace dropdown. The page is already scoped to your current workspace, and its subtitle now names that workspace directly.

**July 20-24, 2026**

## Observability and evaluations

### Datasets and experiments

* `GET /annotation-queues/{id}/items` now returns THREAD queue items alongside RUN items, with an optional item\_type filter. THREAD list rows expose identity on the item (thread\_id/session\_id/start\_time) and omit nested thread; RUN list still hydrates nested run for now (same omit planned for metadata-only list). Traces and messages load via the v2 threads APIs when reviewing.
* `GET /annotation-queues/{id}/runs` and related size endpoints exclude THREAD queue rows (run\_id is null) so mixed queues no longer return 500. Use GET /items for thread listing.
* Project settings now require a thread idle time of at least two minutes to ensure thread evaluations include all ingested runs.
* Annotation queue item add requests now consistently enforce a 100-item limit for runs and threads. Over-limit errors clearly show the configured limit.
* `GET /annotation-queues/{id}/items` returns Postgres membership metadata for RUN and THREAD items without hydrating nested run or thread payloads from ClickHouse or SmithDB. Orphan queue rows remain listed. The include\_stats query parameter is removed. Annotate payloads load via get-one / review APIs.
* When you bulk-add runs from a tracing project, its default dataset now appears first in the dataset picker.
* Annotation queue review lists now label unnamed run rows as `Run <ID>`, matching thread rows and making mixed queues easier to scan.
* Opening the pairwise experiment comparison from a pairwise annotation queue no longer crashes the page when both compared runs come from the same experiment.

### Tracing

* The Insights reports pane can now be collapsed to give report details more space.
* Insights cluster summary columns can now expand to show more of each summary.
* LangSmith MCP's `fetch_runs` tool now returns `first_token_time` when that value is recorded for fetched runs, making TTFT analysis available without a separate SDK query.
* Legacy run URLs now resolve the run metadata and redirect to the SmithDB trace view instead of showing an error.
* Trace usage limit banners now appear only for workspace members whose user-scoped limit has been exceeded.
* The Deployment button on tracing project pages now opens the deployment page within the app instead of reloading the UI.
* Clicking the already-selected run or trace in a thread's trace tree now keeps it selected instead of deselecting it and scrolling back to the first trace.
* Fixed two frontend call sites that could reach POST /runs/stats with an empty or missing session, preventing spurious 422 errors in the Insights job config and session rules form.
* MCP run query tools now return gateway timeout responses without retrying, reducing duplicate load when a run query times out.
* Pressing Enter to confirm characters from an input method editor (e.g. Pinyin for Chinese, or Japanese/Korean IMEs) in LangSmith Chat now commits the composed text instead of prematurely sending the message.
* LangSmith Chat now surfaces a run's system prompt inline when reading a traced LLM run, so it can explain why a model behaved a certain way without missing the system prompt. It also recognizes system prompts stored as provider-level fields (OpenAI Responses `instructions`, Anthropic `system`).
* LangSmith Chat traces now show the model you configured instead of mislabeling it as GPT-3.5-Turbo when a custom model endpoint is used.
* The Run in Studio button is now hidden on public (shared) run pages, where it previously pointed to an authenticated page that shared viewers cannot open.
* Navigating between traces now clears stale sharing state, so unshared traces no longer appear public.
* The run, trace, and thread detail panels now enforce a minimum width when resized, so their header no longer overflows and forces the view to scroll sideways.
* Restore `is_in_dataset` on trace and run responses when the query is proxied to the V1 backend in ClickHouse-only mode. The V1 select now forwards `in_dataset` so the Python backend computes it and the proxy renames it back to `is_in_dataset` for V2 callers.
* BYOC workspaces now avoid requesting trace table fields that older data planes do not support, preventing invalid request errors when viewing traces.
* Custom dashboard charts can now query summed latency and first-token time metrics through the runs analytics SmithDB path.
* Custom dashboard charts can now query minimum and maximum latency, time-to-first-token, token, and cost values through SmithDB-backed runs analytics.
* Custom dashboard charts can now query P90 and P95 for latency, first token time, tokens, and cost metrics, in addition to the existing P50 and P99.
* Custom dashboard charts can now aggregate feedback scores by sum, P50, P90, P95, and P99, in addition to the existing average, min, and max.
* The LangSmith homepage now provides clearer onboarding steps for coding agents and tracing, including a direct shortcut for creating a tracing project.

### Prompts and playground

* Editing agent and skill metadata in the Context Hub now shows save progress, reports actionable errors without discarding changes, and displays successful updates immediately.
* Prompts with a repo readme now display it in a dedicated Readme section of the prompt view.
* Gemini 3.6 Flash and Gemini 3.5 Flash Lite are now available in Fleet, Agent Builder, and playground model selectors, with usage pricing support.
* Pasting content into rich-text editors, such as the prompt playground and agent chat, now works reliably again.
* Previewing a single dataset row after running a full experiment now resolves the row's evaluator scores instead of showing a feedback cell that loads indefinitely, and the resulting feedback chips render with their proper colors.
* LangSmith no longer keeps system-added top\_p values when switching OpenAI prompts to reasoning models, preventing invalid invocation parameters. Users who still need top\_p can add it as an extra model parameter for supported non-reasoning models.

### Engine

* The organization Engine usage page now lets you switch between a workspaces view and a projects view of month-to-date LCU spend, each ranked by spend. The Engine spend API returns the authoritative total independently of the breakdown.
* Engine no longer shows redundant hover tooltips on issue category badges or the default Fix action. Permission and PR status explanations still appear when they add context.
* Engine opens the Slack or webhook destination form immediately when no destinations are configured.
* Engine issue category labels now appear on a dedicated row below the title for more consistent spacing and readability.
* Engine now shows a warning beside a linked repository when it cannot access it, including failures caused by renamed or deleted repositories and broken GitHub connections.
* On an Engine issue, navigating to the next or previous linked trace now stays in the conversation view for traces that belong to a thread, instead of switching to the single-trace view.
* Engine now shows a clickable Paused status in the issues header when scheduled scanning is paused, so you can see its status and open settings directly.
* Engine now works in supported self-hosted deployments without Eppo rollout configuration, while organization enablement and existing permissions remain enforced.
* Opening the project spend limit from the pause confirmation now scrolls the settings pane to the limit editor.
* Engine Overview now displays the current Engine package version so you can see when the underlying experience changes.

### Monitoring and alerting

* Self-hosted alert webhook delivery now honors `SSRF_ALLOW_K8S_INTERNAL`, so internal Kubernetes service hostnames can be used when that setting is enabled. Metadata endpoints, localhost, and private IP protections remain controlled by their existing SSRF policy settings.

### Automations

* Thread (grouped) evaluators now require a minimum idle time of 120 seconds. Setting a project's thread idle time below 120s is rejected.
* Leaving feedback on a run in a thread now makes the thread eligible for re-evaluation, so thread-level evaluators re-run when new feedback arrives.
* Editing an online evaluator (LLM-as-judge or custom code) no longer intermittently fails when sandbox validation is slow.

## Deployment

* Worker and API server CPU charts now plot a peak (max) series alongside the average, so a single replica with high CPU usage is no longer hidden by the fleet-wide average.
* Worker and API server memory charts now plot a peak (max) series alongside the average, so a single replica approaching its memory limit is no longer hidden by the fleet-wide average.
* Creating a deployment with a name that's already in use within your workspace now returns a 409 Conflict instead of a 500 error.
* Hybrid deployments remain compatible with older listeners during control-plane upgrades, preventing new deployments from remaining queued.

## Sandboxes

* A sandbox proxy configuration can now define environment variables that are applied to every command in the sandbox. This is handy when a tool refuses to run unless a credential env var is present (for example gh needs GH\_TOKEN) even though the egress proxy injects the real credential on the wire. Set a placeholder value so the command starts.
* Attach free-form key/value labels when creating a sandbox or snapshot. Labels are stored and returned on reads; sandboxes inherit their snapshot's labels, and snapshots built from a Docker image inherit the image's labels.
* Sandbox network egress now tries every resolved IP for a destination instead of only the first, so requests to multi-homed hosts (for example apt package mirrors) no longer fail when the first address is unreachable on the requested port.
* Creating a sandbox with only mem\_bytes set now derives a matching CPU allocation automatically, so requests for larger-memory sandboxes no longer need an explicit vcpus value to satisfy the CPU-to-memory ratio.

## Administration

* Selecting All Workspaces on the Granular Billable Usage page now loads usage successfully for organizations with many workspaces.
* The Granular Usage page now shows a notice that long-lived trace usage isn't tracked in self-hosted deployments, so the "Long-lived only" filter is expected to show zero results there.

### LLM Gateway

* Gateway Monitoring now shows spend for the workspace you're viewing rather than the whole organization, with a dropdown to switch workspaces from the page. Spend cards show N/A instead of a repeated error message when a workspace's gateway project can't be resolved.
* The Rate Limiting tab in Gateway Policies now supports creating, editing, deleting, and enabling/disabling request- and token-based rate-limit policies, alongside the existing cost-control and data-protection policy management.
* Editing a materialized LLM Gateway policy now turns it into a standalone override, preventing later default policy changes from overwriting its custom limits.
* You can now call LangChain-managed models through the LLM gateway without configuring your own provider credentials. Usage is metered at cost and bounded by a monthly spend cap based on your plan; once the cap is reached, further requests are blocked until the next month. The cap can be raised on request. [Learn more](../../../LLM%20Gateway/Models%20and%20reliability/Gateway%20Credits.md).
* Selecting an entity filter on the LLM Gateway spend monitoring page no longer flips the breakdown to a different dimension.
* Selecting more than one entity in any Gateway Monitoring breakdown filter (model, user, or API key) now returns spend for all chosen entities instead of no data.
* The Gateway Monitoring spend chart now formats axis labels and tooltip ranges in UTC to match its UTC-anchored buckets, so viewers in non-UTC timezones no longer see off-by-one dates.
* The LLM Gateway spend chart and table now label spend from service keys as "Unaffiliated with any user" instead of showing a blank name, with a tooltip explaining that the spend came from a workspace/org-scoped key rather than an individual.
* API-key-scoped LLM Gateway spend-cap and rate-limit policies can now add a custom X-Gateway-\* header condition, so a single API key can match different limits per header value. For example, a reseller can set separate caps per downstream customer without distributing multiple keys.
* Stat card and table headers in the LLM Gateway monitoring page's Spend tab (e.g. "Total Spend", "Daily Avg", "API Key") now capitalize every word, matching the header style used elsewhere in the product.
* When a specific start/end date is selected in the LLM Gateway monitoring page's date range picker, the button now shows the dates in UTC and appends "(UTC)" so it's clear the range doesn't follow your local timezone. Relative ranges like "Last 7 days" are unaffected.
* The "Spend share" column on the LLM Gateway Monitoring spend dashboard no longer cuts off its header text.
* The LLM Gateway now lives in a dedicated top-level sidebar section instead of under Settings, with a new Home tab listing your custom model configurations and a ready-to-run code snippet for the gateway. Old Settings gateway links redirect automatically.
* A Home banner for LangSmith Cloud orgs with LLM Gateway enabled highlights how Gateway manages costs and improves runtime reliability. [Learn more](../../../LLM%20Gateway/Get%20started/LLM%20Gateway.md).

**July 13-17, 2026**

## Observability and evaluations

### Datasets and experiments

* The legacy feedback formula endpoints (`POST/GET /feedback/formulas` and `GET/PUT/DELETE /feedback/formulas/{feedback_formula_id}`) that back composite scores are deprecated in favor of [composite evaluators](../../../Test/Evaluators/Evaluator%20types/UI/How%20to%20create%20a%20composite%20evaluator.md), which implement a composite score as a code evaluator plus a run rule, and are scheduled for removal on 2026-08-20. Migrate existing feedback formulas to the new composite model.
* Expanding the run tree for repetition runs in [experiment comparison](../../../Test/Datasets%20%26%20Experiments/Analyze%20experiment%20results/How%20to%20compare%20experiment%20results.md) views now works reliably when a repetition root has a project ID but no session ID.
* POST /v2/datasets/{dataset_id}/experiment-runs is the supported public API for paginated experiment comparison. Legacy dataset comparison helpers are removed from the public OpenAPI spec and generated SDKs; existing HTTP routes continue to work for LangSmith UI clients.
* Adds `langsmith evaluator create-llm` to define structured LLM-as-judge evaluator rules from a prompt, schema, and model config file, targeting a project or dataset.
* Creating [dataset examples](../../../Test/Datasets%20%26%20Experiments/Datasets/Manage%20datasets.md) from [source runs](../../../Test/Datasets%20%26%20Experiments/Datasets/Manage%20datasets.md) now correctly fetches run inputs and outputs backed by SmithDB, and no longer fails the whole request if one of several source runs can't be found.
* Multi-turn evaluators now include a Test action that runs the evaluator against a sample thread before you save the rule.
* Add RUN items to a single [annotation queue](../../../Test/Annotation%20Queues/Use%20annotation%20queues.md) with POST /annotation-queues/{queue_id}/items. The server resolves runs via ClickHouse or SmithDB and returns a standards-shaped items envelope; THREAD support follows in a later release.
* The LangSmith CLI now updates existing code evaluator rules in place when `evaluator upload --replace` is used, avoiding a delete-before-create window if the replacement upload fails.
* Split the read datasets into a new download datasets permission.  Enforce this new permission in both the application and in APIs.  The download button is disabled for those users without the download permission. [Learn more](../../Govern/Users%20%26%20access%20control/Organization%20and%20workspace%20operations%20reference.md#datasets).
* Public dataset experiment traces open correctly when experiment runs provide their project identifier through the v2 response shape.
* A run rule with a 0 sampling rate processes no runs, but the scheduler still enumerated it every tick. The scheduler query now skips rules with sampling\_rate 0 (parity with the is\_enabled check), so they are never dispatched.
* Dataset and experiment tables now truncate long input and reference-output text and show detected base64 images as small thumbnails with a delayed larger preview, avoiding oversized hidden DOM content.
* Experiment tables now defer full payload rendering and output diff preparation until those views are requested, improving responsiveness for runs with large agent trajectories.
* Public dataset share links now resolve the sessions list (with stats) from SmithDB when ClickHouse querying is disabled, so shared dataset pages no longer fail to load on SmithDB-only deployments.
* Add conversation threads to a single [annotation queue](../../../Test/Annotation%20Queues/Use%20annotation%20queues.md) with POST /annotation-queues/{queue_id}/items using item\_type THREAD (thread\_id + session\_id). Mixed RUN and THREAD batches are supported; the server resolves threads via ClickHouse or SmithDB.
* Code evaluators now get more time to run each batch, so evaluators that import heavy libraries like scikit-learn are less likely to time out.
* POST /annotation-queues/{queue_id}/items now accepts at most 200 items per request and returns a clear validation error when the limit is exceeded. Requests at the limit continue to succeed.
* Applying an evaluator to an existing experiment could fail with "Failed to start evaluation" on large experiments. It now starts reliably even when the run count is temporarily unavailable.
* Linked runs load correctly from public dataset shares when LangSmith uses the ClickHouse compatibility path.

### Tracing

* The tracing and evaluation onboarding quickstarts now show the correct LANGSMITH\_ENDPOINT for bring-your-own-cloud data plane workspaces instead of the shared multi-tenant endpoint.
* Bulk export compression now defaults to zstandard (zstd) for improved performance. Self-hosted environments retain the gzip default via the FF\_BULK\_EXPORT\_DEFAULT\_COMPRESSION environment variable.
* [LangSmith MCP tools](../../../Monitor/Debug/Viewing%20%26%20managing%20traces/LangSmith%20MCP%20Server.md) that fetch runs or thread history now accept project UUIDs in addition to project names, making trace URL investigations faster and less error-prone.
* OpenTelemetry resource attributes (set via OTEL\_RESOURCE\_ATTRIBUTES) now appear on traces as metadata namespaced under otel.resource.\*, so you can attach details like user IDs without changing how your tracer emits spans.
* LLM spans in the trace view now show the model provider's brand logo (OpenAI, Anthropic, Google/Gemini, Azure, Mistral, DeepSeek, xAI, and speech providers), resolved from the run's ls\_provider metadata.
* Fixed a bug where non-primitive metadata values did not appear in run details.
* Run stats scoped to an explicit run-id list (for example Insights per-cluster stats) now compute on SmithDB, which scopes results to those runs instead of falling back to project-wide totals.
* Organization model settings now let you search pricing rules by model name, match rule, or provider. Paginated loading fetches additional rules as you scroll, making large numbers of model price maps manageable.
* Assistant messages carrying tool calls were rendered twice in the v2 messages view for traces produced by the @anthropic-ai/sdk JavaScript SDK. Dedup now normalizes content-block field order so the same message emitted as an LLM output and replayed as an input on the next turn collapses to a single row.
* Run errors whose stack trace arrived fully escaped (no real line breaks) now render as properly formatted multi-line text instead of one long wrapped line.
* LangSmith MCP's `fetch_runs` tool now accepts `min_start_time` and `max_start_time` arguments, so agents can search traces outside the default recent window.
* Adds a `GET /v2/runs/{run_id}/url` endpoint that returns the LangSmith UI URL for a specific run.

### Engine

* When an [Engine](../../../Engine/LangSmith%20Engine.md) project reaches its monthly spend limit, the Next Run status chip and project spend card now show a clear "Monthly spend limit reached" state with a button that takes you straight to raising the limit.
* LangSmith exposes [Engine](../../../Engine/LangSmith%20Engine.md) issue listing and retrieval through hosted MCP tools and generated SDK methods. Agents and API clients can fetch issue details directly by issue ID or filter issues by project, status, severity, tag, and update time.
* A new [Engine](../../../Engine/LangSmith%20Engine.md) board callout points you to the trace-scope setting, where you can restrict Engine's reviews to runs matching a run name or metadata value.
* The Engine setup screen now shows an estimated monthly cost based on the project's recent trace volume and size, so you know roughly what to expect before starting analysis.
* The Engine issue list now uses a single filter and sort menu with a compact, nested layout for Priority, Status, Tags, and Sort by, replacing the previous two separate popovers.
* The [Engine](../../../Engine/LangSmith%20Engine.md) issue list now shows the active sort order as a removable chip next to your filter chips whenever it differs from the default.
* Engine issues can now be marked Fixing or Watching, and you can get a Slack alert when new traces recur on a watched issue.
* The [Engine](../../../Engine/LangSmith%20Engine.md) issue list no longer shows scan-timing details (next scan countdown, last run time, or a Run now action); a Pause/Resume control remains available in its own section in board settings.
* Engine now verifies concrete claims in agent responses against trace evidence, improving detection of ungrounded artifacts, values, and claimed actions.

### Prompts and playground

* Playground runs now retain evaluator scores and reasoning while backend feedback updates are polled, preventing completed results from appearing blank.
* LangSmith now waits for model preset defaults to finish loading before initializing the Playground, preventing OpenAI from replacing a custom default preset during page load.
* The model configuration default button now switches to a selected state when you make a preset your default.
* Playground model settings now apply typed custom model names when the selector closes, so you no longer need to click the typed option explicitly.
* Custom evaluator errors in the Playground results table now reliably show the failure message, instead of sometimes displaying a blank error indicator.
* Configure workspace-wide HTTPS webhooks for every Context Hub commit, with signed payloads, custom headers, and secret rotation controls.

### Feedback

* Adding runs to an annotation queue via the by-key endpoint now falls back to the ClickHouse run lookup when SmithDB queries are disabled, so the SDK's annotation-queue additions work regardless of whether SmithDB is enabled.
* The POST /feedback/eager endpoint is deprecated in favor of POST /feedback and is scheduled for removal on 2026-08-10. Update any direct integrations calling /feedback/eager to use POST /feedback instead.
* Feedback creation now accepts a thread identifier, enabling feedback to be associated with a conversation thread instead of only an individual run or session.
* GET feedback requests can now filter by a thread ID within a project, making thread-level feedback retrievable without resolving a run first.
* Annotation queue rubric feedback now loads the thread-scoped feedback for thread queue items.
* Annotation queue rubric feedback now saves against the selected thread for thread queue items.

### Monitoring and alerting

* When a custom dashboard chart has no data or would produce too many bins, the empty state now surfaces the active stride (e.g. 1M) and selected range (e.g. Last 12 hours) so it's clear what to adjust.
* When hovering the +N chip in a dashboard chart's legend, the expanded popover now paints above adjacent chart cards instead of being clipped behind them.
* Metadata grouping keys without returned values no longer show a misleading empty value tooltip in dashboards.

### Automations

* Resolved an unbounded memory leak in the SAQ queue worker where croniter objects were rebuilt every second, accumulating cached entries that were never released. The croniter dependency is bumped to 6.2.2+ and croniter objects are now reused across schedule ticks.

## Deployment

* You can now edit an existing cron's schedule, input, and end time from a deployment's Crons tab, instead of deleting and recreating it.
* LangSmith frontend images now install nginx 1.31 packages to pick up the latest Chainguard security fixes.
* Deployment creation now checks free deployment usage with the same backend quota count used during submission, preventing the form from offering a free Serverless or Development option when the organization quota is already used.
* LangSmith Deployment now lets you update compute and database resource tiers independently for supported hosted deployments. The scaling action applies the selected resources and rolls out a new revision.
* Hosted project deployment views now label scale-to-zero development deployments as Serverless, with free deployments shown as Serverless (free).
* The deployment form now shows the free serverless option immediately while checking an organization's remaining deployment allowance.
* Refines error handling when attempting to create a deployment with no GitHub repository selected.
* Serverless deployments can now update compute tiers correctly without requiring an external database tier.
* Self-hosted deployments now authenticate correctly to node-based AWS ElastiCache with IAM in both single-node and cluster configurations.

## Sandboxes

* Sandboxes can now opt into keeping their memory when they stop, so the next start resumes where it left off instead of cold-booting. Set preserve\_memory\_on\_stop when creating a sandbox; it defaults to off.

## Administration

* Workspace switcher labels now show the full workspace name on hover when the visible label is truncated. This makes similarly prefixed workspace names easier to distinguish.
* Some new users could get stuck on the last onboarding step, with a loading spinner that never finished. This is now fixed.
* Organization admins can now rename their organization directly from the organization switcher in settings.
* Organization admins can now generate, view, and delete SCIM bearer tokens directly from Settings > Access and Security, instead of using the API, to set up SCIM provisioning with their identity provider. [Learn more](../../Govern/Users%20%26%20access%20control/User%20management.md#set-up-scim-for-your-organization).

## Other

* When you add runs to an [annotation queue](../../../Test/Annotation%20Queues/Use%20annotation%20queues.md) without specifying `extend_trace_retention`, short-lived traces stay on short-lived retention. Pass `extend_trace_retention=true` to upgrade traces to extended retention.

**July 6-10, 2026**

## Observability and evaluations

### Datasets and experiments

* Model, prompt, and tool chips in the Experiments table config cells now lay out from real measurements for accurate truncation, and the +N overflow badge is a clickable dropdown whose entries expose the same actions (filter, group by, open in playground, and details) as a chip's own menu.
* Evaluators linked to Hub prompts now load correctly for flat and playground-shaped prompt commits, fixing crashes when editing existing evaluators.
* The experiment comparison view now offers an optional, reorderable "Splits (latest)" column that shows each example's current dataset split assignments as chips, reflecting live membership rather than the as-of-run snapshot.
* Evaluator spend charts on project and dataset evaluator tabs keep their desktop layout on narrow screens and scroll horizontally instead of compressing the chart and stat cards.
* The experiment comparison and group-by views now show each example's current dataset split rather than the split it had when the experiment ran, so you can tell whether failures already belong to a split without re-running the experiment.
* Comparison view now loads token and cost stats from SmithDB for root runs, so the stats columns populate again instead of staying blank
* LangSmith now caps reusable evaluators per workspace to prevent unbounded resource growth. Contact support if your workspace needs a higher limit.
* Creating dataset examples from source runs now correctly fetches run inputs and outputs backed by SmithDB, and no longer fails the whole request if one of several source runs can't be found.
* Select multiple rows in an experiment (or select all matching the current filters) and add, replace, or remove their dataset splits in one action, or copy the selected examples to another dataset, instead of editing rows one at a time.
* The `/runs/rules/validate` endpoint now supports [thread evaluators](../../../Monitor/Observe/Online%20evaluators/Set%20up%20multi-turn%20online%20evaluators.md). Pass `test_thread_id` and `session_id` to test a multi-turn evaluator against a real conversation before saving.
* The thread evaluator config preview now shows the thread message formats the evaluator actually maps, instead of listing every available format.
* The evaluator config now shows a locked "Trace count ≥ 2" filter for managed thread evaluators, making it clear they only run on threads with multiple turns.
* Experiment comparison and individual experiment views now load run rows on self-hosted deployments that authenticate the UI via SSO/OAuth session cookies. Previously these views could show 'No results found' even though metrics and feedback loaded.
* Experiment statistics now refresh promptly for recently run experiments while keeping historical experiment scans bounded.
* The Assertions evaluator added via "Add evaluator" now reads assertions from the reference output like the auto-attached version, so it grades against the real assertions instead of always failing.
* Evaluator spend chart y-axes now abbreviate amounts of \$1,000 or more, making high-spend values easier to scan.
* A run rule whose sampling rate was 0 (or unset) sent an out-of-range sample\_rate to the SmithDB query service (which rejected it) and zeroed out ClickHouse thread grouping. Both the flat and grouped fetch paths now fall back to 1.0 (no sampling) so these rules query successfully.
* Exporting a dataset comparison view as CSV now returns a clear "file is too large to export" error instead of a generic server error when the export exceeds internal size limits.
* Each split chip in a row's Splits cell is now interactive in the experiment results and comparison views, with an Edit splits action that opens the single-example split picker so you can reassign splits without leaving the table.

### Tracing

* The batched-run ingestion log now emits run\_verbs as a list of run\_id and verbs objects instead of a map keyed by run UUID, preventing structured-log aggregators from exhausting dynamic field limits.
* Authenticated users viewing public runs now see sidebar navigation for their last selected workspace. Logged-out viewers continue to see the public run without authenticated workspace navigation.
* LangSmith MCP tools that fetch runs or thread history now accept project UUIDs in addition to project names, making trace URL investigations faster and less error-prone.
* OpenTelemetry resource attributes (set via `OTEL_RESOURCE_ATTRIBUTES`) now appear on traces as metadata namespaced under `otel.resource.*`, so you can attach details like user IDs without changing how your tracer emits spans.
* Native OpenTelemetry child spans are no longer dropped when they arrive before an SDK-attributed parent span; they are buffered and correctly nested regardless of arrival order.
* Thread pages now show an explicit access-control message when trace loading is denied by ABAC, instead of a generic retrieval error.
* All time filters in tracing views now query the full retention window instead of falling back to a shorter backend default. This keeps trace, thread, and run results consistent when expanding the time range.
* OpenTelemetry traces from VS Code Copilot Chat now render as one clean nested trace per user turn. Auxiliary title/summary calls and orphaned tool spans are suppressed, message roles are corrected, token counts are de-duplicated, and standardized metadata (integration, agent runtime, thread ID, repo/git details) is attached automatically.
* Insights cluster run stats (run count, latency, tokens, and feedback) now reflect only the runs in each cluster instead of showing the same project-wide totals for every cluster.
* LangSmith Chat now authenticates to Chat LangChain with guest tokens when searching documentation, so docs answers keep working as Chat LangChain tightens authentication.
* The Trace Messages viewer now identifies the "main" conversation for traces that include middleware guardrails or subagent side-conversations, so the message list shows only the primary interaction instead of interleaving middleware/subagent partitions. Correctness is verified by an expanded snapshot suite covering 11 integrations across LangChain, OpenAI Agents SDK, Vercel AI SDK, Claude Agent SDK, deepagents, and raw provider wrappers.
* Custom dashboard charts can now query P50 and P99 for input and output costs without failing runs analytics requests.
* The thread stats API now accepts a `filter` query parameter, letting you scope aggregated stats to traces matching a LangSmith filter expression (e.g. start time or trace ID).
* LangSmith Chat now mints Managed Deep Agent guest tokens from the Chat LangChain LangGraph host (`POST /identity/guest`) when searching documentation, instead of the legacy Chat LangChain frontend guest route.

### Engine

* Upgrades the Redis client to improve recovery from Redis cluster topology changes, fixing cases where cluster reconnects could stall.
* Engine now lets the parent agent recover from model-actionable subtask failures and retries transient provider or network errors before failing a run. This helps issue scans continue through recoverable model errors while preserving hard failures for auth, configuration, and code exceptions.
* LangSmith exposes Engine issue listing and retrieval through hosted MCP tools and generated SDK methods. Agents and API clients can fetch issue details directly by issue ID or filter issues by project, status, severity, tag, and update time.
* Engine-generated examples with assertions now add the Assertions evaluator when saved to a dataset from an annotation queue, matching the direct Add offline examples flow.
* The Engine issue list now uses a single filter and sort menu with a compact, collapsible layout for Priority, Status, Tags, and Sort by, replacing the previous two separate popovers.
* The Engine issue list now shows the active sort order as a removable chip next to your filter chips whenever it differs from the default.
* The Engine issue list no longer shows scan-timing details (next scan countdown, last run time, or a Run now action); a Pause/Resume control remains available in its own section in board settings.

### Prompts and playground

* Self-hosted Playground and evaluator outbound model calls now honor proxy environment variables while preserving SSRF validation on every request.
* Typing a workspace member's name or email in the Context Hub search box now also returns the prompts and resources they created.
* Playground and evaluator calls to Amazon Bedrock using IAM Trusted Entity now resolve the correct LangSmith AWS credentials before assuming customer roles in AWS-hosted LangSmith. This fixes failures that reported "Failed to assume role" before the customer role was assumed.
* Outbound model calls that route through a forward proxy now send the original hostname in the proxy CONNECT tunnel instead of a resolved IP, so proxies that allowlist tunnel targets by domain no longer reject them. This fixes self-hosted Playground and evaluator calls to internal OpenAI-compatible endpoints reachable only through such a proxy.
* Reviewing a prompt commit now displays every extra parameter (such as verbosity) set on the model, not just a fixed subset.

### Feedback

* POST requests to add runs to an annotation queue accept an optional `extend_trace_retention` query parameter. When set to false, short-lived traces are not upgraded to extended retention. The default remains true for backward compatibility.
* Feedback creation resolves run metadata from SmithDB when the client provides session and start time, so SmithDB-only deployments no longer depend on ClickHouse for eager feedback writes.
* The `POST /feedback/eager` endpoint is deprecated in favor of `POST /feedback` and is scheduled for removal on 2026-08-10. Update any direct integrations calling `/feedback/eager` to use `POST /feedback` instead.

### Monitoring and alerting

* Dashboard chart tooltips and axes now show up to eight fractional digits (previously two), so very small costs and rates no longer round down to zero.

## Deployment

* The multi-select dropdown (e.g. Selected Tools) on the Studio assistants page now renders above the configuration dialog instead of behind it, so its options are visible and selectable.
* Redis connections using Microsoft Entra ID (Azure IAM) authentication now re-authenticate automatically before the access token expires, so long-lived connections no longer drop. Clustered Azure Redis is now supported for IAM auth as well.
* The deployment Crons tab now shows each schedule in your local timezone instead of raw UTC, matching the Next Run Date column.
* LangSmith Deployment now supports updating a deployment to a fixed resource tier through the control plane API. The update applies the selected tier's resource configuration, resizes Cloud SQL or RDS, and rolls a new revision.
* You can now rename a deployment from its Settings: give it a friendly display name without recreating it. The deployment's URLs and infrastructure are unchanged.

## Sandboxes

* S3 sandbox mounts now default endpoint\_url to [https://s3.amazonaws.com](https://s3.amazonaws.com) when it is not provided, so the field is no longer required when mounting standard AWS S3 buckets.
* Sandboxes can now burst CPU up to 2x their requested allocation when the host has spare capacity, and you can request fractional (sub-core) vCPU down to 0.05.
* Self-hosted LangSmith installations now show the Sandboxes navigation item and use the instance-level sandbox flag to open the Sandboxes page.
* Shells and tools inside a sandbox now report the sandbox's name as the hostname instead of a generic default, and the name resolves from within the sandbox.
* Self-hosted LangSmith installations can open the Sandboxes page without enabling the Deployments frontend.
* Sandboxes now set common CA-bundle environment variables by default, so Python, Node, Deno, curl, and git tooling automatically trusts the sandbox's egress proxy certificate and no longer fails with TLS certificate-verification errors when its traffic is proxied.

## Administration

* The roles table on the Organization Roles settings page now scrolls correctly when there are more roles than fit on screen.
* You can now fetch a single workspace directly via `GET /api/v1/workspaces/{workspace_id}` instead of listing all workspaces and filtering client-side.
* Organization admins can disable model providers across every workspace from organization settings. Disabled providers are hidden in the playground, evaluators, Fleet, and other model pickers, and workspace admins cannot re-enable them.
* The email confirmation page now shows only the Confirm account step in the sidebar instead of future onboarding steps you have not reached yet.
* Self-hosted deployments now apply explicit DEFAULT\_ORG\_FEATURE\_\* and DEFAULT\_FEATURE\_\* environment variables over stored organization and tenant config values, so operators can enable or disable features and limits globally without editing Postgres.
* The navigation product switcher now shows the configured organization logo alongside the LangSmith or Fleet wordmark instead of repeating the organization logo.
* Organization admins can now toggle role restriction from the Roles settings page. Restricted roles can only be assigned by users with the workspaces:manage permission.
* The organization-wide public sharing toggle now lives on the General settings page alongside the other organization settings, replacing its standalone Configuration section.
* When a user is removed from all mapped SSO groups, the organization and workspace access granted through SSO group sync is revoked on their next sign-in. Access assigned by other means (SCIM, JIT, or manual invitation) is unaffected.
* Workspace invite batch requests are now rate limited per workspace to reduce bulk invitation abuse. [Learn more](../../../Monitor/Trace/Configuration%20%26%20troubleshooting/Usage%20and%20billing.md#workspace-invite-batch-endpoint).
* LangSmith Home now shows a banner promoting Interrupt, our agent conference in London and NYC this fall, with a link to get tickets.

### LLM Gateway

* The LLM gateway now supports `POST /openai/v1/responses/compact` (and the legacy `/responses/compact`), routing it through the chat-shape responses handler.
* When a gateway spend-cap policy targets more than one user, workspace, or API key, the create/edit policy form now explains that the limit applies to the combined spend across the selected entities rather than per entity.
* The LLM gateway now forwards every documented OpenAI API route it does not handle directly (models, files, batches, images, and more) to the upstream provider, so clients can reach the full OpenAI surface through the gateway. Custom OpenAI-compatible providers inherit the same passthrough routes.
* The LLM Gateway policies page now lets you sort each section by spend limit or usage percentage, and filter down to a specific workspace, user, or API key.
* LLM gateway data protection redaction now prepends a short disclaimer to redacted message text so models know SAFE\_TO\_USE placeholders are safe to reuse verbatim.
* The LLM Gateway now proxies Anthropic's Files and Managed Agents endpoints, so you can use them with your gateway-managed workspace key alongside Messages and Models.
* Creating an LLM Gateway spend or data protection policy now applies to the organization you are signed in to, replacing the organization dropdown with a read-only display of the current organization.
* Long selected values, like a user's email in the Gateway Policies filter, now truncate with an ellipsis instead of overlapping the dropdown chevron.
* The LLM Gateway now accepts workspace-scoped LangSmith OAuth bearer tokens across its provider routes, so OAuth clients can invoke configured models without a LangSmith API key.

## Other

* When you add runs to an annotation queue without specifying `extend_trace_retention`, short-lived traces stay on short-lived retention. Pass `extend_trace_retention=true` to upgrade traces to extended retention.

**June 29 - July 3, 2026**

## Observability and evaluations

### Datasets and experiments

* Model, prompt, and tool chips in the [Experiments](../../../Test/Datasets%20%26%20Experiments/Analyze%20experiment%20results/Analyze%20an%20experiment.md) table config cells now lay out from real measurements for accurate truncation, and the +N overflow badge is a clickable dropdown whose entries expose the same actions (filter, group by, open in playground, and details) as a chip's own menu.
* Expanding the run tree for repetition runs in [experiment comparison](../../../Test/Datasets%20%26%20Experiments/Analyze%20experiment%20results/How%20to%20compare%20experiment%20results.md) views now works reliably when a repetition root has a `project ID` but no `session ID`.
* [Evaluators](../../../Test/Evaluators/Manage%20evaluators.md) linked to Hub prompts now load correctly for flat and playground-shaped prompt commits, fixing crashes when editing existing evaluators.
* Code evaluator upload now accepts Python entrypoints annotated with PEP 604 union return types (for example `-> dict | None`).
* `POST /v2/datasets/{dataset_id}/experiment-runs` is the supported public API for paginated experiment comparison. Legacy dataset comparison helpers are removed from the public OpenAPI spec and generated SDKs; existing HTTP routes continue to work for LangSmith UI clients.
* Each example's dataset splits now render as chips in the dataset Examples table, laid out from real measurements with a clickable +N overflow menu when an example belongs to more splits than fit the column.
* The [experiment comparison](../../../Test/Datasets%20%26%20Experiments/Analyze%20experiment%20results/How%20to%20compare%20experiment%20results.md) view now offers an optional, reorderable "Splits (latest)" column that shows each example's current dataset split assignments as chips, reflecting live membership rather than the as-of-run snapshot.
* [Evaluators](../../../Test/Evaluators/Manage%20evaluators.md) spend charts on project and dataset evaluator tabs keep their desktop layout on narrow screens and scroll horizontally instead of compressing the chart and stat cards.
* The [experiment comparison](../../../Test/Datasets%20%26%20Experiments/Analyze%20experiment%20results/How%20to%20compare%20experiment%20results.md) and group-by views now show each example's current dataset split rather than the split it had when the experiment ran, so you can tell whether failures already belong to a split without re-running the experiment.
* LangSmith now caps reusable [evaluators](../../../Test/Evaluators/Manage%20evaluators.md) per workspace to prevent unbounded resource growth. Contact support if your workspace needs a higher limit.
* Creating [dataset examples](../../../Test/Datasets%20%26%20Experiments/Datasets/Manage%20datasets.md) from [source runs](../../../Test/Datasets%20%26%20Experiments/Datasets/Manage%20datasets.md) now correctly fetches run inputs and outputs backed by SmithDB, and no longer fails the whole request if one of several source runs cannot be found.
* Custom code evaluators that time out or fail on a run now record an error on that run instead of silently leaving it without feedback, so partial evaluation failures are visible on the experiment.
* The Open source run action on an example page now reads session and start time from dedicated example fields populated at creation, enabling reliable navigation to the source trace on SmithDB.

### Tracing

* LangSmith now enforces user-defined monthly trace limits scoped to individual projects and users. New traces that exceed a configured limit are rejected, while patches and feedback for already-accepted traces continue to flow through.
* The tracing and evaluation onboarding quickstarts now show the correct `LANGSMITH_ENDPOINT` for bring-your-own-cloud data plane workspaces instead of the shared multi-tenant endpoint.
* Sharing, viewing, or unsharing any run in a trace now operates on the trace root, so every run in a shared trace is publicly viewable, and public run links open the selected run within the shared trace.
* Projects with existing traces no longer incorrectly display the onboarding screen when filtered or scoped to a time window with no recent runs. The project run-count check now looks back 30 days instead of the previous one-hour window.
* Bulk export compression now defaults to zstandard (zstd) for improved performance. Self-hosted environments retain the gzip default via the `FF_BULK_EXPORT_DEFAULT_COMPRESSION` environment variable.
* LangSmith now returns clearer 409 Conflict messages when duplicate run create or update payloads are submitted. The message indicates whether the duplicate was a run create or run update request when possible.
* LangSmith [MCP tools](../../../Monitor/Debug/Viewing%20%26%20managing%20traces/LangSmith%20MCP%20Server.md) that fetch runs or thread history now accept `project UUIDs` in addition to project names, making trace URL investigations faster and less error-prone.
* OpenTelemetry resource attributes (set via `OTEL_RESOURCE_ATTRIBUTES`) now appear on traces as metadata namespaced under otel.resource.\*, so you can attach details like user IDs without changing how your tracer emits spans.
* Vercel AI SDK traces sent over raw OpenTelemetry now render in the Messages view. Previously these traces showed an empty Messages tab because no format adapter claimed them.
* Thread stats requests that opt into streaming now return the main stats first and add feedback stats when they are ready.
* When a runs query times out, the runs table now shows a timeout banner for better responsiveness.
* LangSmith now preserves traces in multipart ingestion batches when one run has oversized inputs or outputs. Oversized input and output fields are replaced with a placeholder instead of rejecting the entire batch.

### Engine

* When an Engine project reaches its monthly spend limit, the Next Run status chip and project spend card now show a clear "Monthly spend limit reached" state with a button that takes you straight to raising the limit.
* LangSmith exposes Engine issue listing and retrieval through hosted [MCP tools](../../../Monitor/Debug/Viewing%20%26%20managing%20traces/LangSmith%20MCP%20Server.md) and generated SDK methods. Agents and API clients can fetch issue details directly by `issue ID` or filter issues by project, status, severity, tag, and update time.
* A new Engine board callout points you to the trace-scope setting, where you can restrict Engine's reviews to runs matching a run name or metadata value.

### Prompts and playground

* Self-hosted [Playground](../../../Deploy/Prompt%20%26%20Context%20Hub/Prompts/Model%20providers.md) and evaluator outbound model calls now honor proxy environment variables while preserving SSRF validation on every request.
* When you save a prompt to an application from the playground, LangSmith keeps the workspace application filter on All Applications instead of switching the rest of the UI to that application.
* Typing a workspace member's name or email in the [Context Hub](../../../Deploy/Prompt%20%26%20Context%20Hub/Prompt%20%26%20Context%20Hub.md#context-hub) search box now also returns the prompts and resources they created.
* The playground now includes Claude Sonnet 5, Claude Fable 5, and Claude Opus 4.8 in the Anthropic, Bedrock, and Gemini Enterprise Agent Platform model selectors. New Anthropic playground sessions default to Claude Sonnet 5.

### Feedback

* Editing the score on evaluator-generated feedback (for example from the experiment comparison view) now saves correctly instead of failing with "Failed to add feedback correction".
* Adding feedback or reviewer notes from the LangSmith UI no longer upgrades short-lived traces to extended retention. Long-lived traces are unchanged.
* Feedback statistics queries now route through the official ClickHouse client, resolving query failures and improving compatibility with ClickHouse 25.x.

### Monitoring and alerting

* Alert chart previews now handle relative date ranges consistently, preventing failures when loading 14-day or 30-day previews.
* [Dashboards](../../../Monitor/Observe/Monitoring%20%26%20alerting/Monitor%20projects%20with%20dashboards.md) chart tooltips and axes now show up to eight fractional digits (previously two), so very small costs and rates no longer round down to zero.
* Time-series charts on custom dashboards now leave gaps for missing data points instead of plotting them as zero, and lines connect across those gaps so trends remain readable.

### Automations

* Applying a prebuilt evaluator without a filter now defaults to running on root runs only, matching manually created evaluators. Previously it ran on every nested run in a trace.
* Turning an online evaluator or automation on or off now saves for any role that can edit rules, instead of silently reverting for members without the retention-configuration permission.

## Deployment

* Self-hosted deployments can now request CPU and memory above the previous Cloud limits of 8/16 cores and 32/16 GB, bounded only by your cluster capacity. Lower bounds, multiple-of-128 granularity, and Redis memory ordering are still enforced.
* Custom Slack app triggers can now opt in to let third-party bots trigger an agent. Enable the allow bot triggers toggle on a registration to accept events from external bots; echoes from your own and other LangSmith-registered bots are still dropped to prevent loops.
* Agents now skip unreachable or misconfigured non-default MCP servers immediately instead of retrying them, removing a slow round-trip from the tool-loading step and cutting time-to-first-token.
* Standby (uptime) minutes for LangGraph Platform deployments could be billed more than once when replicas reported overlapping intervals across separate usage-reporting runs. Reporting now deduplicates each minute across runs so it is billed at most once.

## Sandboxes

* Sandbox command output is now re-chunked into bounded single WebSocket frames, so clients that do not reassemble continuation frames (including the Go SDK) can read large streamed or replayed output without truncated JSON.
* S3 sandbox mounts now default `endpoint_url` to [https://s3.amazonaws.com](https://s3.amazonaws.com) when it is not provided, so the field is no longer required when mounting standard AWS S3 buckets.
* [Sandboxes](../../../Deploy/Sandboxes/LangSmith%20Sandboxes.md) can now burst CPU up to 2x their requested allocation when the host has spare capacity, and you can request fractional (sub-core) vCPU down to 0.05.
* When creating a sandbox, you can now configure Git, S3, and GCS filesystem mounts, including mount paths, Git remotes, bucket settings, and cache options. Configured mounts appear in the sandbox table and detail view.
* The LangSmith SDKs now support creating, listing, updating, and deleting sandbox registries for pulling private container images, alongside the existing sandbox and snapshot operations.
* Sandbox snapshot builds can now request an XFS root filesystem for sandbox-host based environments.
* Sandbox creation no longer fails intermittently with "sandbox not ready" errors when an underlying host is disrupted. Affected capacity now retries the contended resource lock and recovers automatically instead of leaving the pool degraded.
* Sandbox host startup now validates the full version directory before reuse, so a missing initrd no longer causes create-time failures after a partial or stale install.
* Creating a sandbox snapshot from a Docker image now records the image's tag (e.g. ubuntu:24.04 becomes the 24.04 tag), and creating a sandbox from a snapshot name without a tag resolves the latest tag, mirroring Docker.
* Self-hosted LangSmith installations now show the [Sandboxes](../../../Deploy/Sandboxes/LangSmith%20Sandboxes.md) navigation item and use the instance-level sandbox flag to open the Sandboxes page.

## Administration

* A new Project and user limits tab on the enterprise Usage configuration page lets you set monthly trace-count limits scoped to a specific project or user. Add, edit, and delete limits from the page.
* Anonymous organizations now show an "Anonymity mode is on" banner on the members page, and the usage breakdown hides the group-by-user option for non-internal viewers.
* New API keys now default to a finite expiration date instead of requiring a custom value. When an organization enforces a shorter maximum, the form defaults to that maximum instead.
* You can now fetch a single workspace directly via GET /api/v1/workspaces/{workspace_id} instead of listing all workspaces and filtering client-side.
* Org and workspace admins can now edit the role of a pending member invite directly from the Members settings page, without needing to cancel and re-send the invite.
* The Usage limits page now shows each workspace's configured total and extended (long-lived) trace limits, including caps that were previously hidden while the spend limit displayed "Unlimited".
* The batch workspace invite endpoint no longer returns a 409 error when inviting users who are already pending org invitees or active org members. Those users are added directly to the workspace without requiring a new org invite.
* The role selector in the edit pending member invite dialog now uses a scrollable select, matching the invite flow. This ensures all custom roles are accessible when many workspace roles are defined.
* Self-hosted deployments can now encode spaces in the OIDC authorization request as %20 instead of +, so single sign-on works with identity providers that reject the default + encoding of the scope list. Enable it by setting OAUTH\_URL\_ENCODE\_SCOPE\_SPACES=true.
* Billing upgrade dialogs now stay within the viewport and scroll when payment or business details make the form taller than the screen.
* Non-admin callers with manage-members permission can no longer assign restricted roles to workspace members or invite users with restricted roles to the workspace.
* Filter the organization's service keys and personal access tokens by workspace on the API keys settings page.
* Users without workspaces:manage permission cannot use restricted roles for invites, role changes, or user deletions in the UI.
* Adding existing active or pending organization members to a workspace no longer fails when organization-level invites are disabled. Disabled org invites continue to block new organization invitees.
* The Roles settings page now scrolls correctly when an organization has more roles than fit on screen.
* Organization admins can once again edit the role of and remove other organization admins from the Organization Members settings page. Organization Operators, who share the same admin-level permissions but should not manage other admins, are now correctly prevented from editing, removing, or promoting members to Organization Admin.

### LLM Gateway

* LLM gateway data protection policies can now configure whether a guard pipeline timeout allows the request through or blocks it. Existing policies default to allowing requests on timeout.
* The LLM gateway now supports POST /openai/v1/responses/compact (and the legacy /responses/compact), routing it through the chat-shape responses handler.
* Guard policies now let you choose which PII rule categories to detect, with separate faster rule-based and slower model-based detection options, instead of a single on/off PII toggle.
* Gateway guard secret redaction now detects additional token formats, including SendGrid API tokens, Google OAuth access tokens, JWTs, Slack webhook URLs, and legacy LangSmith keys.
* The [LLM Gateway](../../../LLM%20Gateway/Get%20started/LLM%20Gateway.md) policies page now lets you sort each section by spend limit or usage percentage, and filter down to a specific workspace, user, or API key.

**June 15-19, 2026**

## Observability and evaluations

### Automations

* [Automations](../../../Monitor/Observe/Automations/Set%20up%20automation%20rules.md) now let you control trace retention per action, so traces matched by a rule can stay at base retention instead of being upgraded.

### Engine

* The [Engine](../../../Engine/LangSmith%20Engine.md) issue board now shows a Connect GitHub action when GitHub is not connected, so you can set up pull request creation without leaving the board.
* [Engine](../../../Engine/LangSmith%20Engine.md) now has a unified enablement screen with access requests, and organization settings consolidate Engine usage and limits in one place.
* Organization admins now receive [Engine](../../../Engine/LangSmith%20Engine.md) spend emails when spend crosses each configured threshold, and pausing or disabling Engine now asks for confirmation.

### Datasets and experiments

* [Experiments](../../../Test/Datasets%20%26%20Experiments/Analyze%20experiment%20results/Analyze%20an%20experiment.md) now show live loading progress in the header and the Progress column, so you can track completed and evaluated runs in real time.
* [Evaluators](../../../Test/Evaluators/Manage%20evaluators.md) now include a trace-retention toggle in the advanced options, so scored traces can stay at base retention when that fits your workflow.
* [Evaluator](../../../Test/Evaluators/Manage%20evaluators.md) prompt editing now offers an advanced mode for editing Mustache templates directly with separate variable mappings.
* You can now apply resource tags when creating a [dataset](../../../Test/Datasets%20%26%20Experiments/Datasets/Manage%20datasets.md), including from scratch, file upload, or a clone.
* Auto-attached Assertions [evaluators](../../../Test/Evaluators/Manage%20evaluators.md) now read assertions from the reference output, so experiment scores reflect actual pass and fail results.

### Prompts and playground

* [OAuth client credentials](../../Govern/Organization/Workspace%20setup/Manage%20model%20configurations.md#oauth-client-credentials) now support per-workspace setup on model configurations, so workspace admins can self-serve OAuth on saved prompts and models.
* The [Playground](../../../Deploy/Prompt%20%26%20Context%20Hub/Prompts/Model%20providers.md) now exposes a Reasoning Summary option for OpenAI reasoning models on the Responses API.
* The model dropdown no longer suggests OpenAI models for an OpenAI Compatible Endpoint, so you can enter your own [custom model name](../../Govern/Organization/Workspace%20setup/Manage%20model%20configurations.md).

### Tracing

* [Trace query syntax](../../../Monitor/Debug/Viewing%20%26%20managing%20traces/Trace%20query%20syntax.md) now has a full operator reference, field table, and quick examples, so API filtering is easier to discover.
* The [OpenTelemetry guide](../../../Monitor/Trace/Tracing%20setup/Integrations/Agent%20frameworks/Trace%20with%20OpenTelemetry.md) now explains how to link spans to an existing LangSmith SDK trace and what happens when a parent span never arrives, so cross-process traces are easier to debug.

### Monitoring and alerting

* [Dashboards](../../../Monitor/Observe/Monitoring%20%26%20alerting/Monitor%20projects%20with%20dashboards.md) now include a chart builder with chart templates, a create and edit pane, and brush and series controls on time series charts.
* You can now send [alerts](../../../Monitor/Observe/Monitoring%20%26%20alerting/Alerts%20in%20LangSmith.md) to Slack as a native notification target and connect or disconnect the Slack app from the UI.

## Deployment

* Preview [deployments](../../../Deploy/Get%20started/LangSmith%20Agent%20Server.md) now build the image for the preview commit instead of reusing the parent deployment's image.

## Sandboxes

* [Sandbox auth proxy](../../../Deploy/Sandboxes/Sandbox%20auth%20proxy.md) now documents GCP rules and service-account handling, so Google API access through the proxy is clearer.
* [Sandboxes](../../../Deploy/Sandboxes/LangSmith%20Sandboxes.md) now marks AWS US SaaS availability as generally available, so the region table reflects the current rollout.
* [Sandboxes](../../../Deploy/Sandboxes/LangSmith%20Sandboxes.md) now support Git mounts and Google Cloud Storage bucket mounts.

## Admin and billing

### Administration

* [Organization settings](../../Govern/Organization/Overview.md) now clarify that SSO/SCIM group names can omit spaces, so enterprise IdPs that disallow spaces still work cleanly.
* The Vanta MCP integration is now generally available to all workspaces.
* Applying tags when creating datasets, prompts, and projects is now governed by dedicated [tag-on-create permissions](../../Govern/Organization/Overview.md).

### LLM Gateway

* The [LLM gateway](../../../LLM%20Gateway/Get%20started/LLM%20Gateway.md) now supports native Gemini routes for Gemini Enterprise Agent Platform and the OpenAI embeddings endpoint.
* [Gateway guard](../../../LLM%20Gateway/Get%20started/LLM%20Gateway.md) policies now accept a granular PII configuration and a configurable timeout action.

### Usage and billing

* [Granular billable usage](../../Account/Billing%20%26%20usage/Granular%20billable%20usage.md) now clarifies org scoping, so you can interpret usage totals more accurately.

**June 8-12, 2026**

## Observability and evaluations

### Engine

* [Engine](../../../Engine/LangSmith%20Engine.md) now shows only project-level spend in project view, so org-wide spend stays in the org settings surface.
* [Engine](../../../Engine/LangSmith%20Engine.md) now keeps the Slack issue-alert deck pinned above the scrolling issues list, so the callout stays visible as you browse.

### Datasets and experiments

The experiments table now displays loading progress bars showing the number of runs completed and evaluated, and experiments that predate this feature show a placeholder progress bar.

* [Dashboards](../../../Monitor/Observe/Monitoring%20%26%20alerting/Monitor%20projects%20with%20dashboards.md) now support time series bar and line charts backed by the v2 chart API, so monitored metrics can use the newer chart type.
* Categorical feedback now shows derived percentages in experiment tables, so pass/fail metrics are easier to scan.

### Prompts and playground

* [Playground](../../../Deploy/Prompt%20%26%20Context%20Hub/Prompts/Model%20providers.md) now mints OAuth bearers end to end for OAuth-enabled presets, so long-running batches and streams keep working.

## Sandboxes

* [Sandbox auth proxy](../../../Deploy/Sandboxes/Sandbox%20auth%20proxy.md) now supports GCP auth flows, so sandbox workloads can reach Google APIs through the proxy.

## Fixes

* The Engine trial modal no longer shows the rough-math LCU bullet, so the pricing copy is less misleading.

**June 1-5, 2026**

## Observability and evaluations

### Automations

* [Run rule](../../../Monitor/Observe/Automations/Set%20up%20automation%20rules.md) webhook payloads now include a trace deep link for each run, so downstream systems can jump straight back to the trace.

### Engine

* Per-workspace [Engine](../../../Engine/LangSmith%20Engine.md) spend is now generally available: you can view LCU and USD spend directly on the Engine settings page, including session-level spend.
* The Engine settings page now surfaces additional Engine details in one place.
* You can rotate [Engine issue-board webhook](../../../Engine/LangSmith%20Engine%20notifications.md) signing secrets from both the API and the webhook settings UI.
* The Engine issues list adds a sort option by trace count.

### Datasets and experiments

* A new out-of-the-box [Assertions evaluator](../../../Test/Annotation%20Queues/Use%20assertions.md) scores outputs against an explicit list of criteria specified in the reference output, and an Assertions rule is auto-attached when you add assertion-style examples to a dataset.
* Evaluator metrics are improved in the experiment detail, [comparison](../../../Test/Datasets%20%26%20Experiments/Analyze%20experiment%20results/How%20to%20compare%20experiment%20results.md), and global experiments tables.

### Prompts and playground

* The [Playground](../../../Deploy/Prompt%20%26%20Context%20Hub/Prompts/Model%20providers.md) supports Amazon Bedrock API key authentication, letting you authenticate with a bearer token instead of AWS credentials.

### Tracing

* The [trace view](../../../Monitor/Debug/Viewing%20%26%20managing%20traces/View%20traces.md) now shows an unread indicator on a run's actions menu when the run has reviewer notes you have not seen yet.
* The waterfall view is now full-height with sticky turn headers, so you keep your place while scrolling through long traces.
* Global search now includes context and sandboxes

## Deployment

* You can now trigger a LangSmith Deployment from the [Studio](../../../Test/Test%20from%20Studio/LangSmith%20Studio.md) page.
* LangSmith Deployment now supports [deploying Google Agent Development Kit (ADK) agents](../../../Deploy/Get%20started/Frameworks%20and%20platforms/Deploy%20Google%20ADK%20agents.md).

## Sandboxes

* [Sandbox proxy rules](../../../Deploy/Sandboxes/Sandbox%20auth%20proxy.md) now support configuring AWS authentication, so sandboxes can reach AWS services through the proxy with signed requests.
* Sandboxes can create [snapshots](../../../Deploy/Sandboxes/Sandbox%20snapshots.md) from a Dockerfile build source.

## Admin and billing

### Administration

* Organization admins can now disable personal access token creation from the [organization settings](../../Govern/Organization/Overview.md) page.

### Usage and billing

* [Granular billable usage](../../Account/Billing%20%26%20usage/Granular%20billable%20usage.md) now supports filtering and grouping by retention tier, separating long-lived from short-lived traces.
* The Granular Billable Usage page now surfaces LangSmith Deployment usage, including nodes executed, agent runs, and agent uptime, alongside trace usage.

## Fixes

* Performance improvements for the loading of large traces.
* Filter values for metadata are now preserved when you reopen a filter dropdown to edit it.
* Dataset creation now uses a multi-select dropdown for choosing CSV fields.

**February 16-20, 2026**

## Observability and evaluations

### Insights

* The [Insights Agent](../../../Monitor/Observe/Monitoring%20%26%20alerting/Discover%20errors%20and%20usage%20patterns%20with%20Insights.md) now supports scheduled reports on daily, weekly, or custom cron intervals, so report generation runs without manual triggering. Time ranges compute dynamically, so a "last 24 hours" report always reflects the most recent window when it runs, not when you configured it.

### Datasets and experiments

* You can now pin any experiment as a baseline. The pinned experiment stays at the top of the [Experiments](../../../Test/Datasets%20%26%20Experiments/Analyze%20experiment%20results/How%20to%20compare%20experiment%20results.md) view and serves as the automatic comparison point for later runs, surfacing performance deltas across every column so improvements and regressions are immediately clear.

**February 2-6, 2026**

## Observability and evaluations

### Cost tracking

* [Cost tracking](../../../Monitor/Trace/Configuration%20%26%20troubleshooting/Cost%20tracking.md) now extends beyond LLM calls. Submit custom cost metadata for any run, such as an expensive tool call, a third-party API, or a retrieval step, to monitor, debug, and optimize spend across your entire agent stack from a single dashboard.

### Tracing

* You can now [configure which parts of a trace's inputs and outputs](../../../Monitor/Debug/Viewing%20%26%20managing%20traces/Configure%20run%20input%20and%20output%20preview.md) appear in the tracing table, so teams working with custom trace formats can surface the most relevant fields, reduce clutter, and identify traces that need a closer look faster.

**December 15-19, 2025**

## Observability and evaluations

### Annotation and human feedback

* New pairwise [annotation queues](../../../Test/Annotation%20Queues/Use%20annotation%20queues.md) let reviewers compare two runs side by side and choose whether option A is better, option B is better, or the two are equal across rubric items. LangSmith automatically pairs runs between two experiments and manages queues, reviewer assignments, and trace access, so you can run A/B evaluations across agents, prompts, and models, including for subjective dimensions like tone, correctness, usefulness, or style.

**December 8-12, 2025**

## Observability and evaluations

### Tracing

* LangSmith Fetch, a new command-line tool, brings LangSmith traces directly into your terminal, coding environment, or IDE. Install it with `pip install langsmith-fetch`, then retrieve traces with filters such as `--limit`, `--after`, and `--last-n-minutes`, or bulk-export traces and threads to files for analysis, scripting, or dataset creation.

**December 1-5, 2025**

## Observability and evaluations

### Cost tracking

* [Cost tracking](../../../Monitor/Trace/Configuration%20%26%20troubleshooting/Cost%20tracking.md) now automatically records token usage and derived costs for major model providers, and you can submit custom cost data for tools, retrieval steps, and other operations. Costs appear across trace trees, project stats, and dashboards, with an editable price map for non-standard pricing.

**November 17-21, 2025**

## Admin and billing

### Administration

* LangSmith is now on the Okta Integration Network, so enterprise teams can provision and deprovision users with SCIM and configure SSO through Okta's guided setup. See the [administration overview](../../Govern/Organization/Overview.md) for access control options.

**October 20-24, 2025**

## Observability and evaluations

### Insights

* The [Insights Agent](../../../Monitor/Observe/Monitoring%20%26%20alerting/Discover%20errors%20and%20usage%20patterns%20with%20Insights.md) is now generally available for Plus and Enterprise plans. It analyzes production traces to surface usage patterns, agent behaviors, and failure modes, with usage-pattern clustering, poor-interaction analysis, and custom grouping and filtering.

### Datasets and experiments

* [Multi-turn evals](../../../Monitor/Observe/Online%20evaluators/Set%20up%20multi-turn%20online%20evaluators.md) measure end-to-end agent conversations across multiple exchanges, scoring semantic intent, semantic outcomes, and agent trajectory, including tool calls and decisions.

**October 13-17, 2025**

## Observability and evaluations

### Datasets and experiments

* [Dataset creation](../../../Test/Datasets%20%26%20Experiments/Datasets/Manage%20datasets.md) now infers schema automatically from uploaded CSV and JSONL files, supports adding metadata fields during upload, supports column mapping and renaming, and supports bulk additions to existing datasets from new uploads.

## Deployment

* LangGraph Platform is now [LangSmith Deployment](../../../Deploy/Get%20started/LangSmith%20Agent%20Server.md) and LangGraph Studio is now [LangSmith Studio](../../../Test/Test%20from%20Studio/LangSmith%20Studio.md). LangSmith now spans three services: Observability, Evaluation, and Deployment. Existing deployments, APIs, workflows, pricing, and contracts are unchanged, and no action is required.

**October 6-10, 2025**

## Observability and evaluations

### Datasets and experiments

* You can now write custom code [evaluators](../../../Test/Evaluators/Manage%20evaluators.md) in JavaScript in addition to Python, so TypeScript teams can stay in their ecosystem end to end.

**September 22-26, 2025**

## Observability and evaluations

### Datasets and experiments

* [Composite evaluators](../../../Monitor/Observe/Online%20evaluators/Set%20up%20composite%20online%20evaluators.md) combine multiple evaluator scores into a single metric using a weighted average or weighted sum, with customizable weights.

**September 8-12, 2025**

## Admin and billing

### Administration

* You can now create service keys at the [organization level](../../Govern/Organization/Overview.md), scoped to multiple workspaces or the entire organization, and assign roles, including custom roles, for granular permissions.

**August 25-29, 2025**

## Deployment

* [LangSmith Deployment](../../../Deploy/Get%20started/LangSmith%20Agent%20Server.md) now queues revisions automatically, processing each new revision only after the current one finishes to prevent overlapping deployments and conflicts.

**August 11-15, 2025**

## Deployment

* [Studio](../../../Test/Test%20from%20Studio/LangSmith%20Studio.md) now includes Trace Mode, which shows your LangSmith traces directly in Studio and supports annotating runs and adding them to datasets for evaluation.

**July 28 - August 1, 2025**

## Observability and evaluations

### Datasets and experiments

* Align Evals provides a playground-like interface for iterating on [evaluator](../../../Test/Evaluators/Manage%20evaluators.md) prompts and comparing human-graded scores side by side with LLM-generated scores to surface misaligned cases.

## Deployment

* LangSmith now links traces to the server logs in [LangSmith Deployment](../../../Deploy/Get%20started/LangSmith%20Agent%20Server.md), so you can open user and system logs directly from a trace.

**July 21-25, 2025**

## Observability and evaluations

### Tracing

* [Data export](../../../Monitor/Debug/Bulk%20export%20trace%20data/Bulk%20export%20trace%20data.md) now supports scheduled exports of traces, so external systems such as data warehouses, monitoring platforms, and dashboards stay in sync without custom infrastructure.

**July 7-11, 2025**

## Deployment

* A new Monitoring tab shows [deployment](../../../Deploy/Get%20started/LangSmith%20Agent%20Server.md) metrics, including CPU and memory usage, API request latency, and active run counts, over a customizable time range.

**June 30 - July 4, 2025**

## Observability and evaluations

### Datasets and experiments

* You can now create custom views of [evaluation results](../../../Test/Datasets%20%26%20Experiments/Analyze%20experiment%20results/Analyze%20an%20experiment.md) by breaking fields from inputs, outputs, and reference outputs into their own columns, hiding or reordering columns, and adjusting decimal precision on feedback scores.

## Admin and billing

### Administration

* LangSmith [API keys](../../Govern/Organization/Overview.md) now support expiration dates, so you can scope access for temporary tasks or team members.

**June 16-20, 2025**

## Observability and evaluations

### Prompts and playground

* The [Playground](../../../Deploy/Prompt%20%26%20Context%20Hub/Prompts/Model%20providers.md) now supports calling built-in tools from OpenAI and Anthropic, such as web search and MCP, so you can verify tool selection and argument passing.

## Deployment

* [Studio](../../../Test/Test%20from%20Studio/LangSmith%20Studio.md) now lets you run agent evaluations in the UI without code, comparing against reference outputs and grading responses with custom criteria.

**June 2-6, 2025**

## Observability and evaluations

### Cost tracking

* [Cost tracking](../../../Monitor/Trace/Configuration%20%26%20troubleshooting/Cost%20tracking.md) now accounts for cached tokens, multiple token modalities such as text and image, and reasoning tokens, and supports tracking costs for arbitrary token types.

**May 26-30, 2025**

## Observability and evaluations

### Prompts and playground

* [Prompts](../../../Deploy/Prompt%20%26%20Context%20Hub/Prompt%20%26%20Context%20Hub.md#prompts) now support webhook triggers that sync a prompt to external systems such as GitHub, databases, or CI/CD pipelines when it is updated.

**May 19-23, 2025**

## Deployment

* Every agent deployed on [LangSmith](../../../Deploy/Get%20started/LangSmith%20Agent%20Server.md) now exposes its own Model Context Protocol (MCP) endpoint, so the agent can be used as a tool in any client that supports streamable HTTP for MCP, with no custom code or infrastructure.

## Admin and billing

### Usage and billing

* SaaS customers can now view monthly [usage charts](../../Account/Billing%20%26%20usage/Granular%20billable%20usage.md) that track all billable metrics in one place.

**May 12-16, 2025**

## Observability and evaluations

### Monitoring and alerting

* [Agent observability](../../../Monitor/Overview/LangSmith%20Observability.md) surfaces tool calls and run stats, including the most-used tools and runs, their latency, and which generate the most errors.

## Deployment

* LangGraph Platform, now [LangSmith Deployment](../../../Deploy/Get%20started/LangSmith%20Agent%20Server.md), reached general availability for deploying and managing long-running, stateful agents at scale, with one-click GitHub-to-production deployment, integrated memory and persistence, scalable APIs, and an agent registry across cloud, hybrid, self-hosted, and developer deployment options.
* [Studio](../../../Test/Test%20from%20Studio/LangSmith%20Studio.md) v2 runs locally without the desktop app, supports editing prompts and configuration in the UI, integrates with the Playground, and lets you download production traces to debug them locally.

**May 5-9, 2025**

## Observability and evaluations

### Tracing

* LangSmith now supports [multimodal content](../../../Monitor/Trace/Configuration%20%26%20troubleshooting/Advanced%20tracing%20techniques/Log%20multimodal%20traces.md) for images, PDFs, and audio across the playground, annotation queues, and datasets, including attaching files to dataset examples without base64 encoding and visualizing the content in the app.

**April 21-25, 2025**

## Observability and evaluations

### Monitoring and alerting

* [Alerts](../../../Monitor/Observe/Monitoring%20%26%20alerting/Alerts%20in%20LangSmith.md) send real-time notifications on error rates, run latency, and feedback scores, so you can catch production failures proactively.

**March 31 - April 4, 2025**

## Observability and evaluations

### Prompts and playground

* The [Playground](../../../Deploy/Prompt%20%26%20Context%20Hub/Prompts/Model%20providers.md) now lets you create datasets inline and add examples to existing datasets without leaving the Playground.

**March 24-28, 2025**

## Observability and evaluations

### Tracing

* LangSmith now has end-to-end native [OpenTelemetry support](../../../Monitor/Trace/Tracing%20setup/Integrations/Agent%20frameworks/Trace%20with%20OpenTelemetry.md) for LangChain and LangGraph applications, including distributed tracing across microservices.

### Datasets and experiments

* You can now define [evaluators](../../../Test/Evaluators/Manage%20evaluators.md) for datasets and tracing projects directly in the UI with no code, including LLM-as-a-judge evaluators with prebuilt templates, customizable prompts, variable mapping, scoring, and few-shot support.

**March 17-21, 2025**

## Deployment

* [Studio](../../../Test/Test%20from%20Studio/LangSmith%20Studio.md) now lets you view and edit node logic in the UI by tagging configuration fields with `langgraph_nodes`, edit prompts without code changes, and sync Playground experiments back to the graph.

**March 10-14, 2025**

## Observability and evaluations

### Tracing

* LangSmith now supports tracing [OpenAI Agents SDK](../../../Monitor/Trace/Tracing%20setup/Integrations/Agent%20frameworks/Trace%20with%20the%20OpenAI%20Agents%20SDK.md) applications with two lines of code, for step-by-step observability of agent execution and reasoning.

### Datasets and experiments

* You can now rename an [experiment](../../../Test/Datasets%20%26%20Experiments/Analyze%20experiment%20results/Analyze%20an%20experiment.md) in the UI, either from the Playground table header after a run or with the pencil icon in the Experiments view.

**February 24-28, 2025**

## Observability and evaluations

### Datasets and experiments

* You can now group [experiment results](../../../Test/Datasets%20%26%20Experiments/Analyze%20experiment%20results/Analyze%20an%20experiment.md) by metadata to analyze evaluation performance across segments such as user groups or subject areas.

## Fixes

* A new ingest-backend service separates trace ingestion from frontend request handling, improving average request processing and high-traffic response times.

**February 17-21, 2025**

## Observability and evaluations

### Prompts and playground

* The [Playground](../../../Deploy/Prompt%20%26%20Context%20Hub/Prompts/Model%20providers.md) can now use workspace secrets saved in LangSmith, for consistent credential management across environments.

**February 3-7, 2025**

## Observability and evaluations

### Datasets and experiments

* A new [experiment view](../../../Test/Datasets%20%26%20Experiments/Analyze%20experiment%20results/Analyze%20an%20experiment.md) gives each feedback key its own column and adds filtering, sorting, and a heat map to spot patterns and performance areas.

## Deployment

* You can now open LLM runs from [Studio](../../../Test/Test%20from%20Studio/LangSmith%20Studio.md) in the LangSmith Playground for debugging, visualization, and prompt experimentation within threads.

**January 27-31, 2025**

## Observability and evaluations

### Tracing

* [Traces](../../../Monitor/Debug/Viewing%20%26%20managing%20traces/View%20traces.md) now include a waterfall graph that highlights latency bottlenecks and shows which components run in parallel versus sequentially.

**January 20-24, 2025**

## Observability and evaluations

### Prompts and playground

* The [Playground](../../../Deploy/Prompt%20%26%20Context%20Hub/Prompts/Model%20providers.md) adds a streamlined prompt settings UI, a default model configuration, an enhanced tool management modal, and improved side-by-side comparison.

### Datasets and experiments

* New [Pytest and Vitest integrations](../../../Test/Evaluators/Frameworks%20%26%20integrations/How%20to%20run%20evaluations%20with%20pytest.md) let you run evaluations using familiar testing frameworks, with debugging, metrics tracking, and built-in evaluation functions.

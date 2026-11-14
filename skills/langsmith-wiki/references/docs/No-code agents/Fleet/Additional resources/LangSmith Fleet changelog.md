# LangSmith Fleet changelog

> Weekly updates to LangSmith Fleet

Weekly updates to [LangSmith Fleet](../../../Additional%20documentation/No-code%20agents%20with%20LangSmith%20Fleet.md).

**Subscribe**: This changelog includes an [RSS feed](https://docs.langchain.com/langsmith/fleet/changelog/rss.xml) that can integrate with [Slack](https://slack.com/help/articles/218688467-Add-RSS-feeds-to-Slack), [email](https://zapier.com/apps/email/integrations/rss/1441/send-new-rss-feed-entries-via-email), Discord bots like [Readybot](https://readybot.io/) or [RSS Feeds to Discord Bot](https://rss.app/en/bots/rssfeeds-discord-bot), and other subscription tools.

**November 2-9, 2026**

## Fleet

* Org admins can lock a Fleet agent, which stops new runs, threads, and crons for it and ends any run that calls a tool. A locked agent cannot be deleted or cloned, and its agent response shows `locked`, `locked_at`, and `locked_by`.
* Subagents now show the root agent's model when no model is set for them. You can select a different model for a subagent or clear the override to inherit the root model again. Subagents with no root model show "Root model unavailable" instead of a model.
* Choose a connection format when you create an agent from a template. Templates now default to Per-user, and you can pick Shared before you create the agent. The format cannot be changed after the agent is created.
* Agents with up to 50 MiB of files can be loaded, renamed, and edited again. Saves that grow an agent's files past 25 MiB return 422 `agent_files_too_large`, but deleting or shrinking files always works.
* Fleet agents now send an agent access token that names the agent and the user behind each request to custom MCP servers, model providers, and sandboxes, so your egress gateway can attribute those calls.
* Channel actions now return Slack's own error code and message when Slack refuses a post or reaction, such as `not_in_channel` when the bot is not in the channel or `missing_scope` with the scope Slack needs. The error also appears in scheduled deliveries through the deployment channel action route, which keeps its `detail` field and adds `provider_error`.
* Deployments with a Slack channel can now be redeployed and deleted with a service key, so CI deploy jobs no longer need a user-scoped key. Setting up or changing a LangSmith-managed Slack app still requires a personal key, and setup returns a 403 that says so.

## Fixes and improvements

> [accordion] Show all fixes
>
> * Fleet agents now show their full answer on newer Claude models (Opus 5.5, Sonnet 5.5) instead of only the suggestion pills, so the email or reply you asked for appears in the chat.
> * Approving a Managed Tools tool call in Fleet now works when the tool asks for approval by default. Previously, approving failed with "Unknown or already-consumed interrupt" because the thread state did not show the pending approval.
> * Scheduled and triggered agent runs now honor the memory auto-approve setting. Your agent writes to memory without asking for approval when auto-approve is on.
> * Agent runs no longer fail when a sandbox is missing a file that the agent reads, such as `/memories/AGENTS.md`. The agent now continues without that file instead of stopping before the model is called.
> * Google Workspace tools, including Gmail, Calendar, Drive, Docs, Sheets, Slides, and Meet, now send their requests through your configured `HTTPS_PROXY`, so calls no longer bypass your forward proxy.
> * Creating a Slack app in a workspace at its app limit now returns a clear 422 error that tells you to remove unused apps or ask a Slack admin to raise the limit, instead of a 502 server error.
> * Slack file tools, such as **slack\_send\_file**, now work through Managed Tools. Previously, they failed because the Slack connection did not request the `files:write` scope. If you connected Slack before this fix, reconnect it to grant the new scope.
> * Slack approval cards for tool servers in search mode now name the tool you are approving, such as **gmail\_send\_email**, instead of the proxy tool `call_tool`.
> * Creating a Slack app no longer fails when your agent description contains emoji or curly quotes. Descriptions are now capped at 139 bytes, and Slack's validation message appears when Slack rejects a manifest.
> * Fixed an issue where the dropdowns and text inputs in the access profile editor opened from Configure did not respond. The editor now opens in a centered dialog, and you can use its dropdowns, search, and text inputs.
> * Sandbox requests that use a Slack connection no longer fail with a 500 error when Slack returns nested user details during authentication.

**October 26-November 2, 2026**

## Fleet

* Workspace skill deletion in Agent Builder is now limited to skill owners with the `fleet-skills:delete` permission, and an open deletion confirmation closes if that permission is removed.
* Workspace webhooks can now be run by users who have the Fleet agent create permission, not only workspace admins, when Fleet RBAC is enabled. Create-only users can run a webhook from the Configure panel and the Settings menu, and users without the permission see a message that they cannot run these webhooks.
* You can now create, edit, and delete access profiles through `/v1/fleet/access-profiles`, with an optional `description` on each profile and `created_by` and `updated_by` fields that record who made each change. Deleting a profile that a live computer environment uses returns a 409 that lists those environments, and only workspace admins signed in as a user can make these changes.
* Computer environments now refuse access profiles that mix an allow network with a deny or block\_all network, and access profile network changes are refused when they would mix a live environment that uses them, so runs no longer fail on a mixed network.
* Sandboxes for v2 enterprise agents now inject OAuth tokens from the agent's own connections instead of the creator's personal tokens. If the agent is not connected to a provider, its sandbox requests get a 403 for that provider.
* Crons stay paused when Fleet is disabled for your organization. They no longer resume automatically when limits reset, and you can resume them from the Fleet API or the agent's trigger settings.
* The Executive Assistant template now creates a Per-user agent, which can connect your own Gmail and Outlook inboxes in addition to Slack. Email the agent handles runs as you, using your own Google account. Teams remains available only for Shared agents.
* Removing an MCP server from the workspace is now only available from **Integrations**. Removing an MCP connection from an agent no longer removes the server from your workspace, so it stays installed and can be added to other agents.
* Integration cards and detail dialogs now show the icon that your MCP server advertises, loaded directly from its HTTPS URL. Bundled provider logos still take precedence, and the default icon appears when no valid icon is available.
* Scheduled posts can now start a thread that your agent follows: when you set `follow_thread` to `true` on a post action, replies in the new thread without a mention reach your agent, starting with the input posted after the scheduled message.

## Fixes and improvements

> [accordion] Show all fixes
>
> * Failed model calls that showed only "The model request failed. Please try again or contact support." now name the model and the cause, such as provider credits, a model that was not found, or denied access, and say what to do next.
> * Agents now explain which configured MCP tools are unavailable and why, while healthy tools keep working. Authentication failures show guidance to reconnect or check credentials, and Retry refreshes only the affected server.
> * Azure Fleet now loads, lists agents and threads, and sends chat messages instead of failing with the `No deployment URL specified` error or HTTP 500 responses.
> * Slack messages posted by incoming webhooks now start your agent instead of failing with a `missing channel identity_context` error.
> * Saved custom models with OAuth enabled now start chats and show credential requirements without asking for a static provider key, and token acquisition failures return actionable guidance.
> * Agents that use your own Anthropic API key in a HIPAA-configured organization no longer fail on every model call with "The model request failed." Long threads now keep full tool results until summarization runs, so those calls may send more input tokens.
> * Agents that use saved Anthropic model configs no longer fail with "The model request failed" on **claude-opus-5** and **claude-sonnet-5**. Requests with a `temperature` setting now complete as expected.
> * Fleet renews the LLM auth proxy JWT during a run, so model calls made more than about 6 minutes into a run no longer fail with an auth proxy error. If a renewal fails, Fleet keeps using a JWT that is still valid, and once it expires the call fails with an auth proxy error instead of `[INVALID_API_KEY]`.
> * Runs on a thread now show the reason Fleet refused to create its computer, such as an idle timer that is not a multiple of 60 seconds, instead of "An internal error occurred." Refused creates return their own status, and retryable failures still return 503.
> * Connecting Gmail, Google Calendar, or Google Docs no longer fails with an upstream error when your Google account previously granted the managed Google app access to Calendar or Gmail through Fleet.
> * Changing a Slack channel's trigger mode to or from **mention** now reinstalls the Slack app automatically, so new messages start runs without a manual reinstall. If your workspace requires admin approval, the deploy shows the approval link and retries the reinstall on each deploy until it succeeds.
> * Renaming an empty Fleet memory file with Enter now keeps the new name instead of reverting to untitled.md.
> * Opening **/v1/fleet/docs** in your browser now loads the Fleet API reference instead of showing a fetch error in Swagger UI.
> * Resuming a pending question or tool approval with a response that is missing the required `decisions` field now returns an actionable error instead of `KeyError: 'decisions'`. Refresh the conversation and submit your response again.
> * Fleet run usage is no longer billed twice when the usage report to LangSmith is slow to respond. Your runs are reported once, even when the response takes longer than 2 seconds.

**October 19-26, 2026**

## Highlights

* **Reconnect OAuth accounts that stopped working**: When an OAuth token can no longer refresh, Fleet now shows a **Needs reconnect** badge and a **Reconnect** button instead of **Connected**. In the accounts dialog, **Reconnect** re-authorizes the same account rather than adding a second one, and agent connections are kept so they work again after you reconnect. Agent runs also skip servers whose tokens are not active, and token and connection responses include `status` and `status_reason`. [Learn more](../Tools%20and%20automation/Remote%20MCP%20servers.md).

## Fleet

* Slack channel runs now show Slack's native Stop button while the agent works in a thread, so you can stop a run started from Slack. Stopping a run posts "Stopped by" with your name in the thread and clears the working state.
* Slack now shows a run's progress while it works: a streaming message next to the Stop button, with a Thinking step, a card for each tool call, and the reply text as it is written, so Slack agent-session apps no longer show only a bare "Working..." for the whole run.
* You can now connect a Slack app that you create and own to self-hosted deployments. Deploy with your app's bot token and signing secret, and Trigger Server keeps them stored and keeps the channel active on redeploy without resending them. Agent view with the Stop button is available for customer-owned apps that hold the `assistant:write` scope.
* You can now select a computer environment for an agent when you create it, or leave the selection out to use the workspace default. The selection is kept through reads, clones, and edits, and a PATCH to the agent can change it or return it to the workspace default.
* The **Per-user** connection option is now marked **Recommended** in agent creation and in the configure panel, and imported agents keep the connection format they were saved with.
* Custom workspace MCP servers now appear in the **Managed Tools** tab and in the **Add connection** picker alongside LangSmith built-in servers, so you can connect them to your agents from either place.
* Agents that post Slack feedback buttons now receive thumbs up and thumbs down clicks on their replies, so your agent can act on ratings. Slack's verification token is no longer included in the event your deployment receives.
* When an agent behind a Slack bot is archived, deleted, unlinked, or temporarily unreachable, the bot now replies to the sender in an ephemeral message that says what is wrong and who can fix it, instead of staying silent. In channels, the bot only replies when mentioned.
* You can now filter the user usage report by email. Pass an `email` query parameter to `GET /v1/fleet/usage/users` to return only the matching user, so you no longer need to page through every user in your workspace. Matching ignores letter case and surrounding spaces, and an email longer than 254 characters returns a 400 error.
* Agent Auth apps can now be a Linear OAuth app: create one with provider `linear` and source `existing`, passing `client_id`, `client_secret`, and `scopes`, and install it through a session on the app's connection.

## Fixes and improvements

> [accordion] Show all fixes
>
> * Agent Builder now shows recovery actions such as Retry, setup navigation, and reconnect in Chat, connection rows, and the clone dialog when a provider connection check fails, instead of only a Connect button.
> * Fixed an issue where stopping a Fleet run left tool calls shown as pending. Tool calls that did not finish now show as interrupted once streaming stops, and the canceled run notice appears after the run ends.
> * Shared skills now save from their configuration dialog: select **Edit**, change the skill, and click **Save skill** to update it for every agent that uses it, or confirm before discarding unsaved changes when you close the dialog.
> * Agent zip exports now include the connection format, so importing a Shared or Per-user agent from the sidebar restores the same format in the setup dialog instead of falling back to the default.
> * Saving a manual OAuth MCP server now requires an OAuth provider, and a rejected save shows an inline error while keeping your entered values instead of failing silently.
> * Slack channel setup now shows Slack's reason when it fails, such as `no_permission` or `invalid_manifest` with the field that was rejected, instead of a generic 502 error.
> * Threads stuck with a sandbox marked as still being created can now be deleted, both singly and in bulk. Delete previously returned `409 thread sandbox provisioning is in progress` and kept failing on retry; it now returns `204` and removes the thread.

**October 12-19, 2026**

## Highlights

* **Connect MCP clients to Fleet agents**: Every Fleet agent is now an MCP server, so clients such as Claude Code and Cursor can hand it a task at `/v1/fleet/agents/{agent_id}/mcp` using your API key and workspace headers. The endpoint exposes `send_message`, `respond_to_interrupt`, `get_thread`, and `cancel_run`, so a client can start a conversation, answer interrupts, check on long runs, and stop a run. The Fleet API reference now documents the endpoint and its request body. [Learn more](../Advanced/Use%20Fleet%20agents%20in%20code.md).
* **Call Fleet agents over A2A**: Each Fleet agent is now available as an A2A server at `POST /v1/fleet/agents/{agent_id}/a2a`, with an agent card at `GET /v1/fleet/agents/{agent_id}/.well-known/agent-card.json`. Point any A2A client at `/v1/fleet/agents/{agent_id}` as its base URL, and use `SendStreamingMessage` for long-running agents. Messages without a `contextId` start a new Fleet thread, and shared agents see the identity of the person who invokes them. [Learn more](../Advanced/Use%20Fleet%20agents%20in%20code.md).

## Fleet

* Slack agents can now answer follow-up replies in a thread without an @-mention: set `triggerMode` to `thread` when you create the channel, or change an existing Slack channel's mode in place, and the app updates its event subscriptions without being reinstalled. The default for new Slack channels stays `mention`, and existing channels keep their current mode until you change it.
* Chat models that need an API key now show whether the key is configured, stay visible but disabled when it is missing, and open a **Configure API keys** dialog from the model menu so you can add the key without losing your chat selection.
* Fleet customers can now fetch estimated USD costs by user and by agent from the new `/v1/fleet/usage/users` and `/v1/fleet/usage/agents` endpoints, with cursor pagination (`page_size` up to 100) and sorting by cost, runs, or first and last use; the endpoints require the `fleet:read-admin-config` permission.
* Secret MCP servers now show a link to enter your API key when no key is stored, so a tool call returns a sign-in-style link to add it instead of a dead end; the same link also lets you replace a rotated or revoked key, and saved values are sent as their headers on the next request.
* Free workspaces now create new Fleet agents and Build agents with state storage instead of a sandbox, and new general chats on free plans keep attached files in graph state. Computer access stays available as an upgrade option, and paid plans keep their existing backend choices.
* The agent configuration panel is now a modal drawer that covers the chat, with **Save changes** always visible in the footer; it closes after a successful save, and closing with unsaved edits asks you to confirm before discarding them.
* Slack-triggered threads in the web UI now show a Slack card with the sender's name, the message text, and an "Open in Slack" link, instead of the raw channel IDs and user IDs the agent receives. Mentions of users in the message display as their names. Threads created before this change still open with a card, but show the sender's raw ID and no link.
* Access profiles now live under a new **Computers** item at the end of the Explore section in Fleet, and the old Integrations > Computer links redirect to the new page.
* Fleet schedules now require a minute interval of at least five minutes, so every-minute and wildcard steps below five such as `*/3` are rejected with a message that suggests `*/5 * * * *`.
* New Build agents now default to Per-user connections and record trace inputs and outputs, so their runs include request and response payloads unless you turn tracing off.
* Build generation now requires the selected model's API key. The Generate button stays disabled until the key is saved in the workspace or organization, and existing keys satisfy the requirement without re-entry.
* Tool kits replace MCP gateways in the Tools page, API routes, and audit events, and existing `/gateways` URLs and `?view=gateways` links keep working. You can now refresh a tool kit's tools on request with `POST /v1/managed-tools/kits/{kit_id}/tool-refresh`.
* Workspace admins can now create tool credential profiles in **Workspace tools** > **Profiles**, connect OAuth and API-key servers once for a profile, and have agents call those tools by sending the `X-LangSmith-Profile` header instead of acting as a user.
* The agent builder now always passes your original request to the new agent: when you click **Create agent**, the request is prefilled as the new agent's first message, so you no longer need to restate it.
* Thread reads that time out now return a 504 Gateway Timeout instead of a generic 500, and threads known to be too large return a 422 immediately instead of timing out again.
* The Pylon integration now includes a `pylon_get_issue_messages` tool, so agents can read the full message thread on an issue, including customer replies and internal notes, instead of only the opening message.
* Failed agent runs in Slack now include a footnote under the error message that links to that run's LangSmith trace. The link works for people with access to the workspace, and everyone else in the thread still sees the error as before.
* Fleet runs in OIDC SSO organizations now receive your identity provider access token, including scheduled and triggered runs with no user present, and the token renews automatically when it expires.

## Fixes and improvements

> [accordion] Show all fixes
>
> * Shared agents now name the user who runs them instead of the agent's creator, so the model prompt and run metadata show the invoker's name and email, including for runs started through the SDK proxy.
> * Scheduled Fleet runs no longer fail with expired credentials errors. Each cron run now gets fresh credentials when it starts, so runs created before this fix succeed without being recreated.
> * Subagents paused for approval, a reply, or sign-in now show what they need in Fleet chat, such as "Needs approval", instead of "Failed".
> * Clicking **Input** in the Fleet Studio trace panel no longer clears the selected conversation, and reopening a thread from **Threads** keeps it loaded.
> * Skills you create in chat now stay attached to the conversation after you reopen it, and sharing a skill to the workspace reports success only once the workspace copy is saved, with a clear error when it fails.
> * AI setup now lets self-serve workspaces generate configurations with Fleet models such as Default, Fast, Pro, and Max, so the model picker is no longer empty.
> * Custom MCP servers registered with a trailing slash in their URL now load their tools and send their configured headers, instead of showing "Could not load tools" or dropping every tool as invalid.
> * Connecting an account now disables both the Connect new account button and the Add button until the connection finishes, so repeated clicks no longer create duplicate accounts; both buttons re-enable after a cancelled, failed, or completed connection, and a failed connection now shows a "Failed to connect account" error message.
> * Slack channel setup for agents on AWS now completes instead of returning a 404 error after the agent deploys.
> * Reauthorizing an OAuth connection that was created before login IDs changed no longer fails with a forbidden error; the existing token and agent connection are kept and reauthorization completes for the original user.
> * OAuth providers that use HTTP Basic client authentication now accept client IDs and secrets containing reserved characters such as colons, percent signs, and plus signs, so token requests no longer fail with an invalid client error.
> * Built-in tools such as Parallel and Exa now work with MCP clients that use the 2026-07-28 protocol revision, including Managed Deep Agents in its default auto mode, which previously failed on `tools/list` with a missing `resultType` error.

**October 5-12, 2026**

## Fleet

* Fleet agents can now be called from MCP clients such as Claude Code and Cursor: each agent exposes its own MCP server, so a client can send it a task, continue the conversation, approve or answer its interrupts, check a thread, or cancel a run.
* Fleet now offers Claude Sonnet 5.5 and Opus 5.5, GPT-6.1 Sol, and Gemini 3.8 Flash as built-in models you can select for your agents.
* Slack bots from other registered agents can now trigger your agent when the receiving channel enables bot triggers and the message mentions its bot user, and turning bot triggers on or off now takes effect when you redeploy the Slack channel.
* SharePoint download and upload tools now handle PDFs: `sharepoint_download_file` saves a SharePoint file into your workspace at `/downloads/<filename>`, and `sharepoint_upload_file` accepts workspace files up to 25 MiB as well as text content.
* Creating an agent with a computer, or starting a thread with one, now returns a clear 403 error explaining that computer access is not enabled for your organization when the setting is off. Agents without a computer continue to save normally.
* Scheduled agent runs that are rejected for exceeding your monthly quota or weekly spend limit now disable their cron schedule automatically, so they stop retrying until you re-enable them.
* Slack app setup now works in bring-your-own-cloud (BYOC) workspaces: you can create an agent with a new Slack app using the manual Slack app wizard, and the trigger server's public URL is set to your data-plane URL with `/v1` for the setup flow.

## Fixes and improvements

> [accordion] Show all fixes
>
> * Fixed MCP OAuth setup failing with a 403 for users who have only MCP server permissions; you can now discover an MCP server's OAuth provider and bind it to a workspace without deployment permissions.
> * Workspace admins who sign in with OIDC can now list, create, update, and delete workspace secrets, including the secrets used for MCP server headers, instead of getting a 401 error.
> * Saving an agent with linked skills no longer fails with a missing Prompt permission error when you have Fleet skill read access; the agent saves with your Fleet permissions alone.
> * Fixed an issue where Fleet OAuth sign-in redirects failed with a blocked-request error at the callback page; the callback page now loads, so you can complete OAuth sign-in for Fleet.
> * Fleet integrations in customer-hosted (BYOC) workspaces now use the workspace's data plane for OAuth connections and the LangSmith MCP server, instead of falling back to the SaaS endpoint. Existing integration registrations are not migrated, so reconnect any that were created before this change.
> * Configure no longer replaces an agent's saved shared account when a teammate opens the editor. The saved account now stays selected, and teammates see owner guidance when it needs additional permissions.
> * Sharing or importing a skill with a name already used in the workspace now shows a clear message asking you to choose a different name, and chat skill sharing stays open instead of reporting success.
> * Slack invocation now works for agents whose editor access was cleared to no editors. Previously, Slack invocation stopped after acknowledging the event, and it now runs as expected for the owner and users with Can use access.
> * Attaching a personal OAuth token to an agent now requires that you own the token; requests that reference another user's token are rejected with a 400 error and existing connections are left unchanged.

**September 28-October 5, 2026**

## Fleet

* You can resume an individual Fleet schedule after a weekly spend or monthly usage limit pauses it. If the limit still applies, the next scheduled run pauses it again.
* Schedule cards explain when weekly spend or monthly agent usage limits automatically pause a schedule. Other system pauses also appear on the affected schedule.
* Kimi K2.6 is no longer offered when choosing a model for a Fleet agent. Agents already using it keep working, and workspaces with Kimi K2.6 as their default model start new agents on GPT-5.4 Mini instead.
* The agent hover card shows **Delete** only when you have permission to delete that agent.

**September 21-28, 2026**

## Fleet

* Organization admins can grant separate Fleet agent and skill permissions when configuring custom roles.
* Sandbox-backed Fleet agents provide file browsing, uploads, workspace file mentions, and file counts for every user.
* Fleet agents send Slack replies as standard Markdown, so tables, headers, and task lists render as native Slack content instead of code blocks.
* The beta Fleet feedback API requires both `thread_id` and `run_id` when submitting a rating, so ratings stay attached to the selected reply.
* `GET /v1/fleet/feedback` lets workspace admins list any user's ratings during beta. It returns up to 100 recent feedback records, with an `is_truncated` flag when older records are excluded.
* Setting or clearing a rating through `POST` and `DELETE /v1/fleet/feedback` records a workspace audit log entry, including the rating ID.
* External OIDC users can submit thread-level ratings through the Fleet feedback API.
* Parallel tool calls share a monthly allowance across an organization's workspaces. When the allowance is exhausted, calls return a limit error with the next reset time.
* Fleet shows actionable guidance for missing or invalid API keys and malformed request headers.

**September 14-21, 2026**

## Fleet

* Fleet now displays supported schedules in your browser's local time while storing and evaluating them in UTC. Custom cron expressions and unsupported monthly schedules are explicitly labeled as UTC.
* Fleet agents on Amazon Bedrock no longer fail on every turn after a truncated tool call or a response containing only thinking is saved to the conversation. Affected conversations resume with the next message.
* Fleet usage charts now show date labels based on the available chart width, keeping longer time ranges readable without overlapping labels.
* Fleet thread updates now preserve system-managed ownership metadata across typed, bulk, and LangGraph proxy requests.
* Fresh general-purpose chats and new agents prefer the available admin-configured default model over the last-used model. Users can still choose a different model for a chat, and the last-used model remains a fallback when no admin default is available.
* Agent updates reject changes to the backend type or sandbox scope, matching the existing UI behavior. Create a new agent to use a different backend; other sandbox settings remain editable.

**September 7-14, 2026**

## Fleet

* New managed Fleet sandboxes inherit the platform retention policy when you omit delete\_after\_stop\_seconds. Explicit zero and positive values remain unchanged.
* Threads that stop for an approval or a question now receive their title while they wait, so scheduled runs no longer sit in the inbox untitled until someone opens them. The inbox shows the title loading indicator only while a title is actually on its way.
* Opening a workspace skill just added to an agent in Fleet no longer shows an empty modal before the agent is saved. The skill detail now opens with its full file tree, the Add to agent button waits for the skill's files to load, and a failed load can be retried.
* Agent owners can trigger a workspace webhook against an agent again from the Configure panel's Advanced settings. The rows were missing since the Configure panel replaced the standalone agent editor, and each run packages the agent's saved files rather than unsaved edits.
* Fleet provisions sandboxes correctly when you start a new conversation or retry interrupted sandbox creation.
* Fleet background runs reconnect to the agent's existing sandbox using its saved name. Older UUID-named sandboxes continue to work, and files persist across chats and sandbox restarts.
* Fleet now creates an empty /workspace when it provisions a sandbox, so the files API and file browsers list it right away instead of returning 404 until the agent's first run.
* Fleet preserves Amazon Bedrock reasoning metadata when you abandon a pending interrupt, preventing unsupported content block errors on the next turn.

**August 31-September 7, 2026**

## Fleet

* Fleet now provisions agent-scoped sandboxes during agent creation and returns the sandbox ID and status in the response.
* Repeated outbound channel actions with the same action ID return the original provider response without posting another message.
* Fleet agent responses now include the server-generated slug for addressing agent-scoped sandboxes through the sandbox API.
* Fleet clients can activate the sandbox referenced by a thread and receive its ready status in the response.
* Fleet agents now support saved Databricks model configurations, using your configured workspace URL, serving endpoint, and workspace credentials. You can connect through Databricks Model Serving or AI Gateway routes.
* Self-hosted deployments can now forward a REST caller's `X-Fleet-Forward-*` headers to the custom MCP servers an agent calls, so a policy gateway in front of those servers can see per-invocation context such as an end-user identity. Off by default; enable with `FLEET_MCP_FORWARD_CALLER_HEADERS=true`. Values are asserted by the caller and are not verified by LangSmith.
* Streaming or awaiting a thread run through the Fleet API no longer closes the connection at a fixed deadline; the request stays open until the run finishes or the client disconnects.

**August 24-31, 2026**

## Fleet

* Fleet sandbox APIs now work with external OIDC auth.
* Fleet computers keep uploaded Excel workbooks locally.
* Check Outlook calendar availability.

**August 17-24, 2026**

## Fleet

* Files shared with a Fleet agent in Slack are no longer turned away by type. Spreadsheets, documents, presentations, archives, and other binaries now reach the agent the same way they already do in the Fleet chat UI.
* Fleet computer access now follows the deployment's existing sandbox enablement setting. Self-hosted deployments without sandbox support remain disabled by default.
* Outlook tools can send emails or create drafts with files from the agent workspace, including StateBackend and sandbox-backed agents.
* Saved schedules now display a text Active or Paused badge alongside the icon, making a schedule's state clearer and more accessible.
* Claude Sonnet 5 is now available as a directly selectable Anthropic model in Fleet and Agent Builder, with adaptive thinking enabled.
* GET /v1/fleet/users lists and searches the members of your workspace by email or name, returning the user ID that agent sharing takes. API-only Fleet clients no longer need a user ID from elsewhere before sharing an agent.
* Managed Deep Agent channel setup now accepts LangSmith API keys and bearer tokens while enforcing workspace secret and deployment permissions before provisioning.
* Deployments can now have the general-purpose agent build a new agent directly in the chat, writing its name, description, tools, triggers, and instructions, instead of showing a Create agent button that hands setup to the new agent. Set FLEET\_INLINE\_AGENT\_GENERATION on the Fleet API server, the Fleet queue, and the platform backend to turn it on. Off by default.
* POST /v1/fleet/sandboxes creates a sandbox from a snapshot and returns it ready to use, so a headless client on external OIDC can provision one without reaching for the platform sandboxes API. Choose the boot image with snapshot\_id or a name:tag reference, or omit both for the workspace default.
* DELETE /v1/fleet/sandboxes/ removes one sandbox, so a headless client on external OIDC can clean up a sandbox without reaching for the platform sandboxes API. It is idempotent; deleting a sandbox that is already gone still returns 204; and the sandbox is torn down in the background, so a read taken right after shows it in a deleting state rather than absent.
* GET /v1/fleet/sandboxes//files/content returns the raw bytes of a file in a sandbox. Byte ranges are supported via the Range header, and HEAD reports a file's size without transferring it.
* POST /v1/fleet/sandboxes//files writes a file into a sandbox from a multipart/form-data body, completing the Fleet file API alongside the existing list and read endpoints. The path query parameter names the destination on its own, so the upload no longer depends on reaching a sandbox's dataplane URL directly. Files are streamed rather than buffered, and files larger than 100 megabytes are refused with 413.
* GET /v1/fleet/sandboxes//files returns the files under a path in a sandbox, matched by a glob pattern and paged with page\_size and an opaque cursor. Paging replaces the silent result cap the sandbox glob applied, so a large directory can be read in full instead of stopping partway.
* DELETE /v1/fleet/sandbox-snapshots/ removes a sandbox snapshot, which pairs with snapshot creation for the delete-then-recreate retry after a failed build. It is idempotent, and returns 409 while any sandbox is still booted from the snapshot, including a stopped one.
* GET /v1/fleet/sandbox-snapshots/ returns one sandbox snapshot, so a client can watch a snapshot's build status without re-reading the whole list. The path parameter accepts a snapshot id or a Docker-style reference, where a bare name means name:latest.
* Fleet usage charts now display spend, tool, and model data instead of appearing blank.
* GET /v1/fleet/users now works for Fleet deployments authenticating through an external OIDC provider, not only for API-key callers. Headless clients on OIDC can resolve a colleague's user ID for agent sharing.
* Self-hosted Fleet can attach access profiles whose callback URLs use Kubernetes-internal service names when the deployment enables internal Kubernetes destinations.

**August 10-17, 2026**

## Fleet

* Models in Fleet usage reports now sort correctly by cost, including models with no recorded cost.
* Read-only agents now keep the Configure entry point available after the panel is closed, so users can return to agent details and cloning.
* The Teams reply to channel tool now asks for approval by default, matching the other Teams write tools. Agents that already set this tool to run automatically keep their current behavior, and you can switch it back to Auto per agent.
* Agent Builder now shows actionable workspace-secret loading failures with retry guidance while preserving existing missing-key prompts.
* Fleet agents can browse their OneDrive files, download and update documents, upload files, rename files, and create sharing links.
* Fleet agents can list direct Outlook attachments and discover linked OneDrive or SharePoint files in message bodies.
* Fleet agents can forward an email to new recipients with an optional comment, and move a message into another folder. Both ask for approval first.
* Fleet agents can list a mailbox's folders, including nested ones, and scope an email search to a single folder instead of the whole mailbox.
* Deleting an agent completes cleanly and removes the agent's files along with it. Previously the delete could return a permission error after the agent had already disappeared from the agent list.
* Fleet can now load agent Prompt Hub directories up to 25 MiB, allowing agents with larger memory and file trees to remain accessible.
* Self-hosted deployments can set `FLEET_SCHEDULES_ENABLED=false` to disable recurring runs, unbind the schedule tools, and remove scheduling prompts from agents.
* Runs started through the Fleet API are attributed to the user whose credential invoked them, instead of grouping together under a blank user in the usage breakdown.
* OneDrive tools now return exact drive-relative item paths and reuse them for downloads and updates. This reduces file-not-found errors caused by opaque item references.
* Fleet validates Word, PowerPoint, and Excel files before uploading them to OneDrive or SharePoint, and automatically repairs valid base64-encoded Office files so they upload without corruption.
* Fleet skill get, create, and update operations now resolve external OIDC users correctly while preserving workspace permissions.

**August 3-10, 2026**

## Fleet

* Connecting Google now grants Fleet agents access to your own Docs, Sheets, and Slides, not only files the agent created itself. Existing connections keep working unchanged; reconnect Google from the Integrations page to grant the wider access.
* You can now attach .docx, .xlsx, and .pptx files in chat without giving the agent a sandbox. Models that accept document input, such as OpenAI and Gemini, read the file directly.
* Sandbox-backed Fleet agents now treat PPT requests as PowerPoint deliverables and create .pptx files instead of HTML presentations.
* Sandbox-backed Fleet agents can create spreadsheets, revise existing workbooks, and answer questions about .xlsx and .xlsm files without installing spreadsheet tooling first. A built-in skill guides safe openpyxl usage and validates each workbook before delivery.
* While an agent works on a turn, the chat now shows a live elapsed-time count that appears after a couple of seconds and picks up a rotating status label on longer waits, so a slow turn reads as in progress rather than stalled. Models that stream reasoning still collapse to the time they spent thinking once the answer arrives.
* Fleet agents can now work with Google Drive, searching, organizing, sharing, and inspecting files, and gain additional Sheets, Slides, Docs, Calendar, Gmail, and Meet actions such as replying to and forwarding email, responding to invitations, and checking free/busy times.
* Fleet now uses the selected user identity for GitHub requests that are not tied to a specific repository.
* Custom Slack apps can optionally subscribe to all new channel messages instead of only @mentions. When enabled, the agent receives each message and replies only when helpful.
* Fleet now displays selected artifact elements as feedback chips while messages are queued during an active run.
* Sandbox-backed Fleet agents can convert legacy Office, OpenDocument, RTF, EPUB, and text-based PDF files to Markdown for reading and extraction. A built-in skill guides modern Office files and directly supported PDFs to their existing workflows.
* When an agent reads a file its model cannot accept as an attachment, Fleet now substitutes a short explanation instead of failing the request. Conversations that previously became stuck recover on their next message.
* Create a Fleet skill from a local folder while preserving its SKILL.md and supporting files.
* Skill folder uploads now accept up to 500 files, matching what the API supports, and report progress while reading. Folders that are too large or contain non-text files are rejected up front with the specific files named.

**July 27-31, 2026**

## Fleet

* Fleet agents can use a built-in configuration-hardening skill to selectively separate trust boundaries, minimize tools, require approval for sensitive actions, and review access.
* Open chat files in an edge-to-edge workspace, then collapse them back to the Files side panel without losing your place.
* Self-hosted Fleet agents can use sandbox-backed computer access without requiring a cloud billing plan tier.
* Files attached to Slack messages are now available under /workspace/uploads for sandbox-backed agents, matching files uploaded from Fleet.
* Clicking + New Agent from Workspace Agents now opens the same New agent dialog used elsewhere in Fleet, instead of the old draft editor.
* Navigating to agent chat with an agent selected no longer crashes while the agent details are still loading. The chat shows a loading state until the agent is ready, then renders normally.
* Sandbox-backed Fleet agents can create or revise downloadable DOCX files without installing an authoring package during the task. A built-in skill guides document authoring and structural validation.
* The Configure panel is now enabled for everyone, so it always shows up beside the chat when you open an agent.
* Fleet now resolves AWS IAM roles only for Bedrock models, so loading OpenAI and other provider secrets no longer waits on AWS STS.
* The new agent creation experience is now enabled for everyone. Asking the assistant for an agent surfaces the Create agent button, and the new agent runs its own setup conversation instead of being built inline.
* A conversation whose stored state grew past the API's usual single-response size limit now loads in full, up to 32 MiB, instead of failing. The response marks the conversation as oversized, and updates to it still fail until its state shrinks.
* Sandbox-backed Fleet agents can build a new deck, revise an existing one, and answer questions about the contents of a .pptx file without installing presentation tooling first. A built-in skill guides authoring and validates the file before delivery.
* Fleet agents can send workspace files to Slack channels, threads, and direct messages using slack\_send\_file and slack\_send\_file\_to\_user.
* Fleet agents now correctly route sandbox creation and org config requests to the Go platform-backend service on self-hosted deployments where the Go and Python services run on separate addresses, eliminating the need for a reverse-proxy workaround.

**July 20-24, 2026**

## Fleet

* Reopening or reloading an agent chat thread while a run is still in progress no longer crashes the chat view. The chat shows a loading state until the agent is ready, then resumes streaming the active run.
* The Fleet usage dashboard now shows a meter for orgs with a monthly LangChain Unit (LCU) spend limit, comparing month-to-date consumption against the limit and any overage.
* Arcade MCP gateways configured with Arcade Headers (API-key) authentication can no longer be added to a Fleet workspace, because LangSmith connects to Arcade gateways over OAuth. These gateways now explain how to reconfigure them with Arcade Auth or a User Source instead of failing when you try to connect.
* Fleet now labels the agent card action as Configure, matching the action in the chat view.
* When a Google Docs, Sheets, Drive, or Slides tool can't open a file (a 403 or 404), the agent now explains it can only access files it created itself with its connected Google account, instead of wrongly saying the file doesn't exist.
* Fleet now shows a warning (inline above the failing tool call in chat, and as a message in Slack) when a Google Docs, Sheets, Drive, or Slides tool hits a 403 or 404, explaining the agent can only access files it created itself with its connected Google account.
* Fleet's configure panel now shows the connection format selector so you can choose whether an agent uses shared or per-user accounts.
* Agents connected to Slack can now send a file from their workspace into a Slack channel using the new slack\_send\_file tool, for example a report, export, or chart the agent has generated. The file is uploaded server-side and the agent never sees the Slack token.
* Fleet agents retain DeltaChannel conversation history when thread state is updated, including when users continue trigger-started conversations in chat.
* Fleet thread APIs can now include the current agent's ID and name, making thread lists and details easier to display without fetching full agent records.
* Fleet agents with Slack file tools can now send files from thread-scoped and agent-scoped sandbox workspaces.

**July 13-17, 2026**

## Fleet

* You can now add any agent to [Slack](../Tools%20and%20automation/Integrate%20Slack%20with%20an%20agent.md) in one click. After you authenticate with Slack once, Fleet automatically creates a Slack app configured with the agent's name, description, and icon, and maps each agent to a single Slack app.
* When an agent is first added to a Slack workspace, it sends the creator a direct message with tips for inviting it to channels and mentioning it.
* Agents now raise tool approvals directly in [Slack](../Tools%20and%20automation/Integrate%20Slack%20with%20an%20agent.md), with Approve and Deny buttons in the thread, so you no longer need to switch to the Fleet UI to respond.
* When an agent encounters an error during a run, it now replies in the Slack thread instead of going silent. Authentication errors and some other error types include more detail.
* Agents can now read file attachments in [Slack](../Tools%20and%20automation/Integrate%20Slack%20with%20an%20agent.md) messages.
* The agent editor is now a sidebar built into the agent chat page, which organizes configuration into Channels, Connections, Knowledge, Schedule, and Advanced settings drawers.
* The agent creation experience now starts from a blank-slate agent that configures itself and pauses at key points to bring you into the process.
* The load previous conversations tool now writes conversation files into the attached Computer sandbox when one is enabled, so agents can inspect the downloaded history with their normal file tools.
* Creating a new agent no longer fails with a contentBlocks.push error when the chat stream returns string message content.
* Reloading an agent chat page no longer flashes the thread list through loading and loaded states multiple times. The sidebar now waits for agent scope to finish loading before fetching threads, so the list settles once.
* Fleet agents now discover tools with find\_tools or an /tools listing before opening a tool's reference doc, so they no longer waste a turn reading guessed tool filenames that do not exist.
* The Fleet Fast model tier (`gpt-5.4-mini`) now runs at medium reasoning effort instead of low, improving response quality on harder tasks.
* The [templates](../Get%20started/Templates.md) gallery now features the Executive Assistant and Software Engineer templates as large cards with a hero illustration, each showing the agent's own icon.
* Each tool inside a connection in the agent Configure panel now has a remove action (a trash button revealed on hover, matching the connection remove) instead of an on/off switch. The switch implied a reversible toggle, but turning a tool off actually removed it from the agent, so the control now reflects what it does.
* Sending a chat message while clarifying questions were pending could fail the run and leave the thread stuck. Free-text now correctly dismisses the pending request before continuing.
* In the Agent Builder chat, the Skills block's "Add skill" menu now opens the browse-workspace, create-skill, and import-from-URL dialogs. Previously choosing an option changed the URL but nothing appeared.
* Opening an agent in Fleet now always starts a new chat instead of jumping into a recent thread. Past conversations remain available in the thread sidebar.
* When an agent created from a template introduces itself, it writes what it learns straight to its own memory instead of pausing for approval on every file. Memory writes in your other threads still ask first.
* Skill descriptions containing quotes, colons, or multiple lines are now parsed and stored correctly, and importing or editing a skill preserves all of its frontmatter instead of dropping fields like license or allowed-tools.
* The Add connection dialog now groups Arcade MCP servers under a dedicated Arcade section, so they are easy to find instead of being listed under Other.
* The Fleet model picker now groups served, LCU-billed models (Fast, Pro, Max) separately from bring-your-own models billed per run, making the pricing model for each option clearer.
* The compact Fast/Pro/Max model picker in Agent Builder now shows the model icon on its closed trigger, matching the full model picker.
* When an organization reaches its monthly Fleet usage limit, the error now directs users to upgrade their plan to continue.

**July 6-10, 2026**

## Fleet

* In the Agent Builder view, the footer workspace and tenant list is sourced from the Fleet API so you can switch between your Fleet workspaces.
* The Access Profiles dialog in chat now includes a Create an access profile link that opens the sandboxes create flow, so you can add a profile when a workspace has none configured instead of hitting a dead end.
* Fleet now completes OAuth for MCP servers whose authorization server requires client-secret authentication at the token endpoint, so connecting these servers no longer fails after the consent step.
* Creating an agent from a Fleet template now skips the setup wizard and opens the agent editor with the template onboarding card.
* Fleet now sends the MCP protocol version a server negotiates during the handshake, both when loading tools and when the agent calls them, so MCP servers that require a newer version no longer return zero tools or fail tool calls.
* Fleet agents can now read files shared with them in Slack. Attach an image, PDF, audio, video, or text file in a mention or DM and the agent ingests it into the conversation.
* On the Agent Builder Integrations page, searching now selects the All tab so results span every category, and switching category tabs clears the search.
* When registering an integration OAuth provider for headless connections, `http://` redirect URIs are now accepted only for the loopback IP literals `127.0.0.1` or `[::1]`. The localhost hostname is no longer accepted over `http`; use the loopback IP literal or `https`.
* The [MCP servers settings page](../Tools%20and%20automation/Remote%20MCP%20servers.md) now scrolls when the pointer is over the servers list.
* The Executive Assistant template can now deliver its daily brief and answer @mentions in Slack after you connect a Slack workspace, and both the Executive Assistant and Software Engineer templates received configuration fixes.
* You can now type and send a message in agent chat while a human-in-the-loop prompt is pending. Sending a new message dismisses the pending request and continues the conversation instead of leaving the composer locked.
* Empty sections in the agent configuration panel (Channels, Connections, Skills, Schedules, Instructions, and Subagents) now explain what each one is for and what you can add before you connect anything.
* Opening an agent in the chat inbox no longer issues repeated duplicate background requests while choosing which thread to open, reducing flicker.
* Fleet agents now load your workspace's private skills. Previously, in workspaces with fine-grained access controls, an agent could start with only public skills available.
* GitHub App installations now sync through the authenticated LangSmith session after installation completes, keeping workspace linking aligned with the active user.
* OAuth providers now accept an optional default redirect URI (`default_redirect_uri`). When set, headless OAuth flows for that provider return the authorization code to it instead of the LangSmith callback, without passing a redirect on every request. The value is validated against the provider's allowed redirect URIs.

**June 29 - July 3, 2026**

## New features

* The Access Profiles dialog in chat now includes a Create an [access profile](../Configure/Computer%20use.md) link that opens the sandboxes create flow, so you can add a profile when a workspace has none configured instead of hitting a dead end.
* Fleet agents can now delete files from their memory and [skills](../Tools%20and%20automation/Skills.md) using the new delete tool, including files in linked workspace skills. Core agent files and read-only system skills remain protected.
* Fleet now completes OAuth for [MCP servers](../Tools%20and%20automation/Remote%20MCP%20servers.md) whose authorization server requires client-secret authentication at the token endpoint, so connecting these servers no longer fails after the consent step.
* First-time Fleet users now see a streamlined welcome modal with two clear paths (describe an agent to build with AI, starting from a prompt in Chat, or start from a curated template), replacing the previous multi-step setup wizard.
* Creating an agent from a Fleet [template](../Get%20started/Templates.md) now skips the setup wizard and opens the agent editor with the template onboarding card.
* Fleet now sends the MCP protocol version a server negotiates during the handshake, both when loading tools and when the agent calls them, so [MCP servers](../Tools%20and%20automation/Remote%20MCP%20servers.md) that require a newer version no longer return zero tools or fail tool calls.
* Fleet agents receive the day of week alongside the current date (for example "Monday, June 29th 2026"), so scheduling and date reasoning no longer relies on the model inferring the weekday from the ISO date.
* File edits in Fleet agent chat now render as syntax-highlighted, line-by-line diffs, making changes easier to review.
* When you connect a custom Slack bot to a Fleet agent, Fleet sends the installer a direct message with quick setup tips, including how to add the bot to channels and mention it with @.
* Fleet agents now have a Slack tool for listing channels the connected bot is a member of, making it easier to discover the right channel before posting or reading messages.
* Fleet OAuth provider and integration responses now include an `owner` field (`workspace` or `platform`) so you can tell your own resources apart from built-in, platform-managed ones. The platform manager organization can now create and modify built-in OAuth providers.
* Setting up a schedule is now clearer: choose a preset (daily, weekly, monthly, or every few minutes) or enter a custom cron expression, with a live human-readable preview and inline validation as you go.
* When registering an integration OAuth provider for headless connections, `http://` redirect URIs are now accepted only for the loopback IP literals `127.0.0.1` or `[::1]`. The localhost hostname is no longer accepted over http; use the loopback IP literal or https.

## Fixes

* On the Agent Builder [Integrations](../Tools%20and%20automation/Tool%20integrations.md) page, searching now selects the All tab so results span every category, and switching category tabs clears the search.
* When a Fleet agent's subagent calls a tool that requires human approval, the approval prompt now appears in the chat instead of the run completing without it.

**June 15-19, 2026**

## New features

* [Fleet tools](../Tools%20and%20automation/Tool%20integrations.md) now include Salesforce OAuth provider setup for self-hosted users, so you can configure the provider end to end.
* Agent sharing is redesigned around two choices, who can use and who can edit an agent, plus a Publish as template option that lets others fork their own editable copy.
* Fleet agents now post a notification to the originating thread, such as Slack, when they pause at a human-in-the-loop interrupt, with a link back to the agent chat.
* You can now complete Fleet integration OAuth through your own callback URL, so headless setups can finish authentication without the LangSmith UI.
* Agent cards now show the agent owner.
* New first-party [templates](../Get%20started/Templates.md), Brand Copywriter and Applicant Screening, are available in the gallery.

## Fixes

* Switching threads in the agent chat now clears the previous thread immediately and shows a loading state instead of stale messages.
* The [skills](../Tools%20and%20automation/Skills.md) list now degrades gracefully when one skill fails to load, so the remaining skills still appear.

**June 8-12, 2026**

## New features

* [Templates](../Get%20started/Templates.md) now show “by Fleet” with the Fleet logo, so curated templates match Fleet branding.

## Fixes

* The Fleet list-threads endpoint now returns `items` instead of `threads`, so the response shape matches the rest of the API.
* Fleet thread requests now return a clearer error when a large response would have triggered a 5xx, so long lists fail gracefully.

**June 1-5, 2026**

## New features

* [Skills](../Tools%20and%20automation/Skills.md) load faster: the skills list fetches lightweight metadata first and loads file contents only when you open a skill.
* The agent creation menu adds a [Templates](../Get%20started/Templates.md) entry.
* The [remote MCP](../Tools%20and%20automation/Remote%20MCP%20servers.md) authorization screen now shows the connecting application's name, logo, and homepage, terms, and privacy links instead of its raw `client ID`.
* [Slack integration](../Tools%20and%20automation/Integrate%20Slack%20with%20an%20agent.md) available in AWS and APAC regions.

## Fixes

* [Scheduled (cron) execution](../Tools%20and%20automation/Schedules.md) is restored for enterprise Fleet agents.
* Long-running agent runs and agent-builder generations are no longer cut off after 60 seconds.
* The Gmail read-emails [tool](../Tools%20and%20automation/Tool%20integrations.md) now returns results when you search sent mail with an `in:sent` query.
* Scrolling is improved for long toolbox, skill, and sub-agent lists in the agent editor, and webhook dialogs now scroll within the viewport.

**March 16-20, 2026**

## New features

* Agent Builder is now [LangSmith Fleet](../../../Additional%20documentation/No-code%20agents%20with%20LangSmith%20Fleet.md). The new name reflects Fleet's focus on building and managing agents for your whole team: creating them, sharing them, managing their tasks, and controlling agent access and identity. All existing agents, configurations, integrations, plans, and contracts continue to work unchanged, with no action required on your end.

**February 16-20, 2026**

## New features

* A central Chat agent connects to all of your workspace [tools](../Tools%20and%20automation/Tool%20integrations.md), including Slack, Gmail, Linear, and MCP servers, so you can ask questions and take actions without setting up a dedicated agent first.
* Turn a useful conversation into a recurring agent with one click, with no prompt engineering or conditional logic required.
* Upload files directly into chat, including CSVs, images, documents, and style guides, for the agent to act on immediately.
* A central tool registry lets workspace admins connect [tools](../Tools%20and%20automation/Tool%20integrations.md), manage authentication, and control access across the organization.

**October 27-31, 2025**

## New features

* LangSmith Agent Builder launched in private preview as a no-code way for non-developers to build agents, with conversational setup, built-in memory, MCP integrations, automated triggers, and subagent support. Agent Builder later became [LangSmith Fleet](../../../Additional%20documentation/No-code%20agents%20with%20LangSmith%20Fleet.md).

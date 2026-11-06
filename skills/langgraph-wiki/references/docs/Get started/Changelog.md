# Changelog

> Log of updates and improvements to our Python packages

**Subscribe**: Our changelog includes an [RSS feed](https://docs.langchain.com/oss/python/releases/changelog/rss.xml) that can integrate with [Slack](https://slack.com/help/articles/218688467-Add-RSS-feeds-to-Slack), [email](https://zapier.com/apps/email/integrations/rss/1441/send-new-rss-feed-entries-via-email), Discord bots like [Readybot](https://readybot.io/) or [RSS Feeds to Discord Bot](https://rss.app/en/bots/rssfeeds-discord-bot), and other subscription tools.

**Oct 22, 2026**

## `langchain-core` v1.7.0

In [event streaming](https://docs.langchain.com/oss/python/langchain/event-streaming.md), tool-call arguments now stream as `tool-call-delta` events. Each event carries only the new part of the arguments, as `text-delta` does for text. Earlier versions sent `block-delta` events that repeated all of the arguments so far.

### Upgrade clients before the server

Clients older than the versions below do not handle `tool-call-delta`. For example, earlier versions of `@langchain/react` can stop updating a `useMessages` view. The [Agent Server](https://docs.langchain.com/langsmith/agent-server.md) passes events through unchanged, so the `langchain-core` version on the server decides which events clients receive.

1. Upgrade every client that reads the stream:
   * In JavaScript, upgrade `@langchain/react`, `@langchain/vue`, `@langchain/svelte`, or `@langchain/angular` to 1.2.6 or later.
   * In Python, upgrade `langchain-core` to 1.6.13 or later. `langgraph-sdk` uses it to read the stream.
2. Upgrade `langchain-core` on the server to 1.7.0 or later, together with `langchain` 1.4.7 or later.

`langchain` and `deepagents` accept any `langchain-core` 1.x, so upgrading either one can pull in 1.7.0. To hold the server back until you upgrade every client, pin `langchain-core<1.7.0`.

### Breaking changes

Starting in `langchain-core` 1.6.13, iterating `message.tool_calls` yields only the new part of each tool call's arguments, with the call's `id` and `name`. Earlier versions yielded all of the arguments so far. A call's chunks concatenate into its full arguments, and `message.tool_calls.get()` still returns the parsed tool calls.

**Oct 14, 2026**

## `langchain` v1.4.6

`HumanInTheLoopMiddleware` can now pause once per tool call. Set `interrupt_mode="per_call"` and each gated call raises its own interrupt, which you answer by interrupt ID. Batched mode is still the default.

```python
HumanInTheLoopMiddleware(interrupt_on={...}, interrupt_mode="per_call")
```

### Features

* **Typed answers**: each interrupt carries a `response_schema` listing the decisions that call allows, so a client can build its form from the schema. See [Read the response schema](https://docs.langchain.com/oss/python/langchain/human-in-the-loop.md#read-the-response-schema).
* **Checked before saving**: LangGraph rejects an invalid answer before it is saved, so you can correct it and answer the same interrupt again. See [Correct an invalid answer](https://docs.langchain.com/oss/python/langchain/human-in-the-loop.md#correct-an-invalid-answer).
* **Edits stay on the called tool**: an `edit` can't switch tools, and its arguments are checked against the tool's own schema.

Use per-call mode for new agents. LangChain plans to make it the default in the next major release. See [Pause once per tool call](https://docs.langchain.com/oss/python/langchain/human-in-the-loop.md#pause-once-per-tool-call) and the [human-in-the-loop overview](https://docs.langchain.com/oss/python/concepts/human-in-the-loop.md).

**Sep 1, 2026**

## `langchain` v1.4.0

MCP support now ships inside LangChain in the `langchain.mcp` namespace, built on [FastMCP](https://gofastmcp.com). It replaces the standalone `langchain-mcp-adapters` package. Install it with the `mcp` extra:

```bash pip
pip install "langchain[mcp]"
```

```bash uv
uv add "langchain[mcp]"
```

> [!NOTE]
>
> The `langchain.mcp` namespace is in beta. Importing from it raises a `LangChainBetaWarning`.

### Features

* **One adapter, any transport**: `MCPAdapter` infers the transport from its target — a URL, a local script over stdio, an in-process server, an `MCPConfig` dict for [multiple servers](https://docs.langchain.com/oss/python/langchain/mcp/connections.md#multiple-servers), or a pre-built `fastmcp.Client`. `await adapter.list_tools()` returns LangChain tools ready for `create_agent`. See the [MCP overview](https://docs.langchain.com/oss/python/langchain/mcp.md).
* **Interrupt-driven elicitation**: when a server asks for input mid-call, `MCPAdapter` surfaces the question as a LangGraph `interrupt()`, so a human answers and the run resumes. See [Elicitation](https://docs.langchain.com/oss/python/langchain/mcp/tools.md#elicitation).
* **Authentication through FastMCP**: bearer tokens, full OAuth 2.1 with dynamic client registration, or any `httpx.Auth`, including [per-user authentication](https://docs.langchain.com/oss/python/langchain/mcp/auth.md#per-user-authentication) in a deployment. See [Authentication](https://docs.langchain.com/oss/python/langchain/mcp/auth.md).
* **Richer tool metadata**: each tool carries its MCP provenance under an `mcp` namespace on its metadata, including annotations such as `destructive_hint` for [gating destructive tools behind approval](https://docs.langchain.com/oss/python/langchain/mcp/tools.md#human-in-the-loop). See [Tool metadata](https://docs.langchain.com/oss/python/langchain/mcp/tools.md#tool-metadata).

### Migrating

Moving from `langchain-mcp-adapters`? `MultiServerMCPClient` is replaced by `MCPAdapter`, and several features have changed or been removed. See the [migration guide](https://docs.langchain.com/oss/python/migrate/langchain-mcp-adapters.md).

**Jul 24, 2026**

## `deepagents` v0.7.0

A leaner, more configurable harness by default. On a default-agent turn, input tokens drop **65%** (5,395 → 1,895), validated against our [revamped evaluation suite](https://www.langchain.com/blog/how-we-benchmark-deep-agents) with no quality regression.

### Optimizations

* **Lean prompts by default**: The authored base prompt starts empty and tool-usage prose that duplicated tool schemas has been trimmed. Isolated to the default agent's tool schemas, total description tokens drop **43%** (4,005 → 2,302); combined with the empty base prompt and opt-in todos, a default-agent turn's input tokens drop **65%** (5,395 → 1,895). Tool behavior is unchanged. ([#4859](https://github.com/langchain-ai/deepagents/pull/4859), [#4979](https://github.com/langchain-ai/deepagents/pull/4979), [#5009](https://github.com/langchain-ai/deepagents/pull/5009))

### Features

* **[Override a default middleware instance](https://docs.langchain.com/oss/python/deepagents/customization.md#middleware)**: A `middleware=` (or subagent `middleware`) instance whose `.name` matches a built-in now replaces that default in place, rather than erroring on a duplicate. For example, pass your own `SummarizationMiddleware(...)` to change the token trigger or summary model without disabling the built-in default. ([#4251](https://github.com/langchain-ai/deepagents/pull/4251))
* **Filesystem tools**: New [`delete`](https://docs.langchain.com/oss/python/deepagents/tools#built-in-harness-tools) tool removes a file or recursively removes a directory ([#3659](https://github.com/langchain-ai/deepagents/pull/3659), [#3851](https://github.com/langchain-ai/deepagents/pull/3851)); `write_file` now overwrites an existing file instead of erroring ([#4109](https://github.com/langchain-ai/deepagents/pull/4109)); `FilesystemMiddleware` accepts a [tool allowlist](https://docs.langchain.com/oss/python/deepagents/overview.md#virtual-filesystem-access) to expose only selected built-in tools ([#4325](https://github.com/langchain-ai/deepagents/pull/4325), [#4698](https://github.com/langchain-ai/deepagents/pull/4698)); and reads and searches are tuned for open models — paginated `read_file` reports total and remaining lines plus the next `offset` ([#4540](https://github.com/langchain-ai/deepagents/pull/4540)), `grep`/`glob` return partial results with a `truncated` flag instead of hanging on large trees ([#4063](https://github.com/langchain-ai/deepagents/pull/4063)), and `grep` gains a 1,000-match cap with streamed output and optional context lines ([#4570](https://github.com/langchain-ai/deepagents/pull/4570), [#4706](https://github.com/langchain-ai/deepagents/pull/4706)).
* **More prompt-caching support**: Bedrock prompt caching via the `deepagents[aws]` extra ([#4108](https://github.com/langchain-ai/deepagents/issues/4108)), and automatic Fireworks prompt-cache session affinity ([#4598](https://github.com/langchain-ai/deepagents/pull/4598)).
* **NVIDIA support**: A built-in Nemotron 3 Ultra harness profile plus NIM app-origin attribution. ([#4192](https://github.com/langchain-ai/deepagents/pull/4192), [#4455](https://github.com/langchain-ai/deepagents/pull/4455))

### Breaking changes

* **Planning todos are opt-in**: `create_deep_agent` no longer includes `TodoListMiddleware` by default, so the `write_todos` tool, `todos` state channel, and todo-planning prompt are absent unless restored with `middleware=[TodoListMiddleware()]`. (The OpenAI Codex harness profile still opts in automatically.) ([#4929](https://github.com/langchain-ai/deepagents/pull/4929))
* **Backend compatibility shims removed**: Pass concrete `BackendProtocol` instances instead of factories, configure `StoreBackend` with an explicit `namespace`, and use the current `ls` / `glob` / `grep` / `ReadResult` APIs. Removed symbols include `BackendFactory`, `BACKEND_TYPES`, `FileFormat`, and `Unset`. New files store string `FileData.content`; older `list[str]` content stays readable and converts on next write. ([#4541](https://github.com/langchain-ai/deepagents/pull/4541))
* **Output format changes**: Empty `ls` / `glob` output is now `No files found` instead of `[]`, and `read_file` no longer renders a fixed-width `cat -n`-style gutter — update any parsers of raw tool output. ([#4561](https://github.com/langchain-ai/deepagents/pull/4561))

Copy the following prompt into your AI coding assistant to migrate a codebase for these breaking changes:

Migrate a deepagents codebase from v0.6.x to v0.7.

Migrate this codebase from `deepagents` v0.6.x to v0.7 to account for the following breaking changes:

1. `create_deep_agent` no longer includes `TodoListMiddleware` by default. If this codebase relies on the `write_todos` tool, the `todos` state channel, or the todo-planning prompt, restore it by importing `TodoListMiddleware` from `langchain.agents.middleware` (not `deepagents`) and passing it to `create_deep_agent`:

   ```python
   from langchain.agents.middleware import TodoListMiddleware
   from deepagents import create_deep_agent

   agent = create_deep_agent(middleware=[TodoListMiddleware()])
   ```

2. Backend compatibility shims were removed: `BackendFactory`, `BACKEND_TYPES`, `FileFormat`, and `Unset` no longer exist. Replace any backend factories with concrete `BackendProtocol` instances, and add an explicit `namespace` to every `StoreBackend` configuration:

   ```python
   from deepagents import create_deep_agent
   from deepagents.backends import StoreBackend

   # Before (v0.6.x): factory callable, and StoreBackend with no explicit namespace
   agent = create_deep_agent(backend=lambda rt: StoreBackend())  # [!code --]

   # After (v0.7): concrete backend instance with an explicit namespace
   agent = create_deep_agent(backend=StoreBackend(namespace=lambda rt: (rt.server_info.user.identity,)))  # [!code ++]
   ```

   Also update calls to use the current `ls`, `glob`, `grep`, and `ReadResult` APIs.

3. Tool output formats changed: empty `ls` / `glob` output is now the string `No files found` instead of `[]`, and `read_file` no longer renders a fixed-width `cat -n`-style line-number gutter. Update any code that parses these tool outputs.

Search the codebase for usages of the removed symbols and for parsing logic that depends on the old output formats, apply the necessary changes, and flag anything that needs manual review.

**May 12, 2026**

## `deepagents` v0.6.0

* **[`CodeInterpreterMiddleware`](https://docs.langchain.com/oss/python/deepagents/interpreters)**: (experimental) `deepagents` now supports code execution and programmatic tool calling through a scoped QuickJS runtime.
* Supports `version="v3"` in `stream_events` / `astream_events`. Refer to the [event streaming](https://docs.langchain.com/oss/python/deepagents/event-streaming.md) guide for details.
* **[`DeltaChannel`](../Advanced/LangGraph%20runtime.md#deltachannel) (beta)** ([blog](https://www.langchain.com/blog/delta-channels-evolving-agent-runtime)): Deep Agents now uses `DeltaChannel` for message history and agent files. Rather than re-serializing the full accumulated value into every checkpoint, only the incremental delta written at each step is stored — keeping checkpoint sizes small as threads grow long.

> [!WARNING]
>
> **Rolling back from v0.6.0 is not supported once threads have persisted.** Deep Agents v0.6.0 changes persisted message history and agent files to `DeltaChannel`, which writes checkpoints in a new format that earlier versions cannot read. Downgrading to an earlier Deep Agents version switches these channels back to non-delta channels, leaving existing delta checkpoints unreadable and causing incomplete or incorrect state reconstruction. If you need to roll back, use the [delta-channel-dump recovery script](https://github.com/langchain-ai/langgraph/tree/main/examples/delta-channel-dump) to migrate affected threads, or discard them, before downgrading. More generally, avoid switching a persisted channel between delta and non-delta representations. See [Version compatibility and channel changes](../Advanced/LangGraph%20runtime.md#version-compatibility-and-rollbacks).

* **[Harness profiles](https://docs.langchain.com/oss/python/deepagents/profiles.md)**: Register per-provider or per-model configuration bundles (`HarnessProfile`) that `create_deep_agent` applies automatically when a model is selected — system-prompt tweaks, tool overrides, middleware changes, and subagent defaults — without modifying the call site.
* **[`ContextHubBackend`](https://docs.langchain.com/oss/python/deepagents/backends#contexthubbackend)** ([blog](https://www.langchain.com/blog/introducing-context-hub)): A new filesystem backend backed by LangSmith Hub. Agent files — skills, memories, and other persisted context — are stored as Hub commits, giving you version history on every write and LangSmith-native durability without provisioning a separate LangGraph store.

**May 12, 2026**

## `langchain` v1.3.0

This release adds support for `version="v3"` in `stream_events` / `astream_events` for `langchain` agents. Refer to the [event streaming](https://docs.langchain.com/oss/python/langchain/event-streaming.md) guide for details.

**May 12, 2026**

## `langgraph` v1.2.0

This release adds finer-grained control over node execution (timeouts, error recovery, and graceful shutdown), a new channel type that cuts checkpoint overhead for long-running threads, and a new content-block-centric streaming API (v3) with typed, per-channel projections.

* **[`DeltaChannel`](../Advanced/LangGraph%20runtime.md#deltachannel) (beta)**: A new channel type that stores only the incremental delta at each step rather than re-serializing the full accumulated value. Most useful for channels that grow large over time, for example a message list in a long-running thread. Use `snapshot_frequency=K` to write a full snapshot every K steps and bound read latency.

* **[Per-node timeouts](../Capabilities/Fault%20tolerance.md#timeouts)**: Pass `timeout=` to [`add_node`](https://reference.langchain.com/python/langgraph/graph/state/StateGraph/add_node) to cap how long a single attempt may run. Set a hard wall-clock limit (`run_timeout`), an idle limit that resets on progress (`idle_timeout`), or both via [`TimeoutPolicy`](https://reference.langchain.com/python/langgraph/types/TimeoutPolicy). When the limit fires, LangGraph raises [`NodeTimeoutError`](https://reference.langchain.com/python/langgraph/errors/NodeTimeoutError), clears writes from that attempt, and hands off to the retry policy. Async nodes only.

* **[Node-level error handlers](../Capabilities/Fault%20tolerance.md#error-handling)**: Pass `error_handler=` to [`add_node`](https://reference.langchain.com/python/langgraph/graph/state/StateGraph/add_node) to run a recovery function after all retries are exhausted. The handler receives a typed [`NodeError`](https://reference.langchain.com/python/langgraph/errors/NodeError) and can return a [`Command`](https://reference.langchain.com/python/langgraph/types/Command) to update state and route to a different node, useful for Saga/compensation patterns.

* **[Graceful shutdown](../Capabilities/Fault%20tolerance.md#graceful-shutdown)**: Stop an in-flight run cooperatively after the current superstep completes, and save a resumable checkpoint. Create a [`RunControl`](https://reference.langchain.com/python/langgraph/runtime/RunControl) and call `request_drain()` from any thread; the run raises `GraphDrained` and can be resumed later with the same config.

* **New event streaming API (beta)**: Pass `version="v3"` to `stream_events()` / `astream_events()` for a content-block-centric protocol with typed, per-channel projections (`run.values`, `run.messages`, `run.lifecycle`, `run.subgraphs`) plus opt-in transformers for updates, custom events, checkpoints, tasks, and debug. `run.messages` yields one `ChatModelStream` per LLM call with typed sub-projections for text, reasoning, tool calls, and usage. `version="v1"` and `version="v2"` are unchanged.

Timeouts and error handlers are Python-only; retry policies continue to work in both Python and TypeScript.

**Apr 7, 2026**

## `deepagents` v0.5.0

* **[Async subagents](https://docs.langchain.com/oss/python/deepagents/async-subagents.md)**: Deep Agents can launch non-blocking background tasks, so users can continue interacting with the agent while subagents work concurrently. Requires [LangSmith Deployment](https://docs.langchain.com/langsmith/deployment.md) for sub-agents.

* **Multi-modal support**: The `read_file` tool now supports PDFs, audio, and video files in addition to images.

* **Backend changes**: We've made backward-compatible changes to the Deep Agents [backend protocol](https://github.com/langchain-ai/deepagents/blob/main/libs/deepagents/deepagents/backends/protocol.py):
  * Updated the file format stored in [State and Store backends](https://docs.langchain.com/oss/python/deepagents/backends.md) to support binary files.
  * Improved error propagation from backends to tools.
  * You can now instantiate `StateBackend()` and `StoreBackend()` directly. Specifying with a factory (e.g., `backend=(lambda rt: StateBackend(rt))`) is deprecated.

* **Anthropic prompt caching improvements**: We've made some improvements to improve prompt caching performance for Anthropic models.

**Mar 10, 2026**

## `langgraph` v1.1.0

* **Type-safe streaming (`version="v2"`)**: Pass `version="v2"` to `stream()` / `astream()` for unified `StreamPart` output with `type`, `ns`, and `data` keys on every chunk. Each mode has its own `TypedDict`, all importable from `langgraph.types`. See [streaming docs](../Capabilities/Streaming.md#stream-output-format-v2).

* **Type-safe invoke (`version="v2"`)**: Pass `version="v2"` to `invoke()` / `ainvoke()` to get a `GraphOutput` object with `.value` and `.interrupts` attributes. See [invoke docs](../Capabilities/Streaming.md#v2-invoke-format).

* **Pydantic and dataclass coercion**: With `version="v2"`, `invoke()` and `values`-mode stream output are automatically coerced to your declared Pydantic model or dataclass type.

* **Fixed time travel with interrupts and subgraphs**: Replays no longer reuse stale `RESUME` values, and subgraphs correctly restore the checkpoint for the parent's historical state.

* **Fully backwards compatible**: `version="v2"` is opt-in. `GraphOutput` supports deprecated dict-style access for gradual migration.

**Feb 10, 2026**

## `deepagents` v0.4.0

* New integration packages for pluggable sandboxes: [`langchain-modal`](https://pypi.org/project/langchain-modal/), [`langchain-daytona`](https://pypi.org/project/langchain-daytona/), and [`langchain-runloop`](https://pypi.org/project/langchain-runloop/). See [sandboxes guide](https://docs.langchain.com/oss/python/deepagents/sandboxes.md) and example [data analysis tutorial](https://docs.langchain.com/oss/python/deepagents/data-analysis.md).
* Changes to [conversation history summarization](https://docs.langchain.com/oss/python/deepagents/context-engineering.md#summarization):
  * Summarization now happens in the model node via `wrap_model_call` events. Due to this we retain the full message history in the graph state.
  * More accurate token counting.
  * Summarization will now automatically trigger if a chat model raises a [`ContextOverflowError`](https://reference.langchain.com/python/langchain-core/exceptions/ContextOverflowError) (defined in `langchain-core`). Currently `langchain-anthropic` and `langchain-openai` support this.
* We now default to the Responses API for model strings prefixed with `"openai:"`.
  > [accordion] Disable data retention with the Responses API
  >
  > ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
  > from langchain.chat_models import init_chat_model
  >
  > agent = create_deep_agent(
  >     model=init_chat_model(
  >         "openai:...",
  >         use_responses_api=True,
  >         store=False,
  >         include=["reasoning.encrypted_content"],
  >     )
  > )
  > ```

**Dec 15, 2025**

## `langchain` v1.2.0

* [`create_agent`](https://docs.langchain.com/oss/python/langchain/agents): Simplified support for provider-specific tool parameters and definitions via a new [`extras`](https://reference.langchain.com/python/langchain/tools) attribute on [tools](https://docs.langchain.com/oss/python/langchain/tools.md). Examples:
  * Provider-specific configuration such as Anthropic's [programmatic tool calling](https://docs.langchain.com/oss/python/integrations/chat/anthropic#programmatic-tool-calling) and [tool search](https://docs.langchain.com/oss/python/integrations/chat/anthropic#tool-search).
  * Built-in tools that are executed client-side, as supported by [Anthropic](https://docs.langchain.com/oss/python/integrations/chat/anthropic#built-in-tools), [OpenAI](https://docs.langchain.com/oss/python/integrations/chat/openai#responses-api), and other providers.
* Support for strict schema-adherence in agent `response_format` (see [`ProviderStrategy`](https://docs.langchain.com/oss/python/langchain/structured-output#provider-strategy) docs).

**Dec 8, 2025**

## `langchain-google-genai` v4.0.0

We've re-written the Google GenAI integration to use Google's consolidated Generative AI SDK, which provides access to the Gemini API and Gemini Enterprise Agent Platform under the same interface. This includes minimal breaking changes as well as deprecated packages in `langchain-google-vertexai`.

See the full [release notes and migration guide](https://github.com/langchain-ai/langchain-google/discussions/1422) for details.

**Nov 25, 2025**

## `langchain` v1.1.0

* [Model profiles](https://docs.langchain.com/oss/python/langchain/models.md#model-profiles): Chat models now expose supported features and capabilities through a `.profile` attribute. These data are derived from [models.dev](https://models.dev), an open source project providing model capability data.
* [Summarization middleware](https://docs.langchain.com/oss/python/langchain/middleware/built-in.md#summarization): Updated to support flexible trigger points using model profiles for context-aware summarization.
* [Structured output](https://docs.langchain.com/oss/python/langchain/structured-output.md): `ProviderStrategy` support (native structured output) can now be inferred from model profiles.
* [`SystemMessage` for `create_agent`](https://docs.langchain.com/oss/python/langchain/middleware/custom#dynamic-prompt): Support for passing `SystemMessage` instances directly to `create_agent`'s `system_prompt` parameter, enabling advanced features like cache control and structured content blocks.
* [Model retry middleware](https://docs.langchain.com/oss/python/langchain/middleware/built-in.md#model-retry): New middleware for automatically retrying failed model calls with configurable exponential backoff.
* [Content moderation middleware](https://docs.langchain.com/oss/python/integrations/middleware/openai#content-moderation): OpenAI content moderation middleware for detecting and handling unsafe content in agent interactions. Supports checking user input, model output, and tool results.

**Oct 20, 2025**

## v1.0.0

### `langchain`

* [Release notes](https://docs.langchain.com/oss/python/releases/langchain-v1.md)
* [Migration guide](https://docs.langchain.com/oss/python/migrate/langchain-v1.md)

### `langgraph`

* [Release notes](https://docs.langchain.com/oss/python/releases/langgraph-v1.md)
* [Migration guide](https://docs.langchain.com/oss/python/migrate/langgraph-v1.md)

If you encounter any issues or have feedback, please [open an issue](https://github.com/langchain-ai/docs/issues/new?template=01-langchain.yml) so we can improve. To view v0.x documentation, [go to the archived content](https://github.com/langchain-ai/langchain/tree/v0.3/docs/docs) and [API reference](https://reference.langchain.com/v0.3/python/).

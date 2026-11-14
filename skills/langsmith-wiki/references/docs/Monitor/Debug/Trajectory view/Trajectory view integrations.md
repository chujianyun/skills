# Trajectory view integrations

> Frameworks and SDKs that render in the LangSmith Trajectory view and the metadata each one sets.

The [Trajectory view](../Viewing%20%26%20managing%20traces/View%20traces.md#trajectory-view) renders the [traces](../../Trace/Observability%20concepts.md#traces) of a [thread](../../Trace/Observability%20concepts.md#threads) as a [trajectory](../../Trace/Observability%20concepts.md#trajectories): user prompts, model responses, tool calls, and tool results, in order. The Trajectory view needs two pieces of run metadata to render a trajectory:

* **Thread grouping**: `thread_id` on each run tells LangSmith that a set of runs belongs to the same conversation.
* **Run classification**: `ls_agent_type: "root"` on the top-level run of a turn marks that run as part of the main conversation. Runs marked as subagent appear as a subagent action in the thread while runs marked as middleware or compaction are currently filtered out.

For most LangSmith integrations, both are set for you. When you need to set metadata manually, the following examples cover the [OpenAI Responses API in chaining mode](#openai-responses-api-with-chaining) and tagging custom middleware or guardrails.

## Supported integrations

The following integrations set both `thread_id` and `ls_agent_type` automatically:

* [Claude Code](../../Trace/Tracing%20setup/Integrations/Developer%20tools/Trace%20Claude%20Code%20sessions.md)
* [Claude Agent SDK](../../Trace/Tracing%20setup/Integrations/Agent%20frameworks/Trace%20with%20the%20Claude%20Agent%20SDK.md)
* [OpenAI Codex](../../Trace/Tracing%20setup/Integrations/Developer%20tools/Trace%20OpenAI%20Codex%20sessions.md)
* [Cursor](../../Trace/Tracing%20setup/Integrations/Developer%20tools/Trace%20Cursor%20sessions.md)
* [Pi](../../Trace/Tracing%20setup/Integrations/Developer%20tools/Trace%20Pi%20coding%20agent%20sessions.md)
* [OpenCode](../../Trace/Tracing%20setup/Integrations/Developer%20tools/Trace%20OpenCode%20sessions.md)
* [GitHub Copilot](../../Trace/Tracing%20setup/Integrations/Developer%20tools/Trace%20Visual%20Studio%20Code%20Copilot%20Chat%20sessions.md)
* [Deep Agents](../../Trace/Tracing%20setup/Integrations/Agent%20frameworks/Trace%20Deep%20Agents.md)
* [LangChain](../../Trace/Tracing%20setup/Integrations/Agent%20frameworks/Trace%20LangChain%20agents%20%28Python%20and%20JS-TS%29.md)
* [LangGraph](../../Trace/Tracing%20setup/Integrations/Agent%20frameworks/Trace%20LangGraph%20agents.md)
* OpenAI Chat Completions (`wrap_openai`)
* OpenAI Responses API, single call (`wrap_openai`)

The **OpenAI Responses API in chaining mode** (`previous_response_id`) sets `ls_agent_type` automatically, but you set `thread_id` yourself. For more details, refer to the [OpenAI Responses API with chaining](#openai-responses-api-with-chaining) example.

For the full `ls_agent_type` schema and the other values (`subagent`, `middleware`, `compaction`) that official integrations set on non-root runs, see the [Coding agent metadata contract](../../Trace/Tracing%20setup/Integrations/Developer%20tools/Coding%20agent%20metadata%20contract.md). For the underlying thread-grouping mechanism, see [Configure threads](../Configure%20threads.md).

## OpenAI Responses API with chaining

When you chain calls to the OpenAI Responses API by passing `previous_response_id`, OpenAI stores conversation state server-side and the LangSmith wrapper has no natural key to group calls into a thread. Set `thread_id` yourself, either per call or at wrapper init time.

> [!NOTE]
>
> Use a [UUID v7](https://datatracker.ietf.org/doc/html/rfc9562) for `thread_id`. LangSmith's SDK exports a `uuid7` helper, and UUID v7 sorts by creation time so threads stay ordered in list views.

### Per-call metadata

Set `thread_id` on each call. Use this when one wrapped client serves multiple threads (for example, one client per process, many concurrent conversations).

```python Python
import openai
from langsmith import uuid7
from langsmith.wrappers import wrap_openai

client = wrap_openai(openai.Client())
thread_id = str(uuid7())

res1 = client.responses.create(
    model="gpt-5.6",
    input="What is the capital of France?",
    store=True,
    langsmith_extra={"metadata": {"thread_id": thread_id}},
)

res2 = client.responses.create(
    model="gpt-5.6",
    input="And its population?",
    previous_response_id=resp1.id,
    store=True,
    langsmith_extra={"metadata": {"thread_id": thread_id}},
)
```

```typescript TypeScript
import OpenAI from "openai";
import { uuid7 } from "langsmith";
import { wrapOpenAI } from "langsmith/wrappers";

const client = wrapOpenAI(new OpenAI());
const threadId = uuid7();

const res1 = await client.responses.create({
  model: "gpt-5.6",
  input: "What is the capital of France?",
  metadata: { thread_id: threadId },
  store: true,
});

const res2 = await client.responses.create({
  model: "gpt-5.6",
  input: "And its population?",
  previous_response_id: res1.id,
  metadata: { thread_id: threadId },
  store: true,
});
```

### Init-time metadata

Set `thread_id` once when wrapping the client. Every call made through this wrapper is tagged with the same thread. Use this when a wrapped client serves exactly one thread for its lifetime (for example, a per-conversation worker).

```python Python
import openai
from langsmith import uuid7
from langsmith.wrappers import wrap_openai

thread_id = str(uuid7())

client = wrap_openai(
    openai.Client(),
    tracing_extra={"metadata": {"thread_id": thread_id}},
)

res1 = client.responses.create(
    model="gpt-5.6",
    input="What is the capital of France?",
    store=True,
)

res2 = client.responses.create(
    model="gpt-5.6",
    input="And its population?",
    previous_response_id=resp1.id,
    store=True,
)
```

```typescript TypeScript
import OpenAI from "openai";
import { uuid7 } from "langsmith";
import { wrapOpenAI } from "langsmith/wrappers";

const threadId = uuid7();

const client = wrapOpenAI(new OpenAI(), { metadata: { thread_id: threadId } });

const res1 = await client.responses.create({
  model: "gpt-5.6",
  input: "What is the capital of France?",
  store: true,
});

const res2 = await client.responses.create({
  model: "gpt-5.6",
  input: "And its population?",
  previous_response_id: res1.id,
  store: true,
});
```

## Hide custom middleware or guardrails

When you write your own guardrail, policy check, or middleware function around an LLM or tool call, wrap it in `@traceable` and set `ls_agent_type: "middleware"` on the metadata. The Trajectory view filters these runs out of the main conversation.

```python Python
from langsmith import traceable

@traceable(
    run_type="llm",
    metadata={"ls_agent_type": "middleware"},
)
def entry_guardrail(prompt: str) -> dict:
    # Your guardrail logic
    return {"decision": "allow"}
```

```typescript TypeScript
import { traceable } from "langsmith/traceable";

const entryGuardrail = traceable(
  async (prompt: string) => {
    // Your guardrail logic
    return { decision: "allow" };
  },
  { run_type: "llm", metadata: { ls_agent_type: "middleware" } },
);
```

## Exclude runs from the Trajectory view

Setting `LS_MESSAGE_VIEW_EXCLUDE` on a run's metadata tells the Trajectory view to skip that run. The key's presence is what matters; `True` is the conventional value. The filter runs before any extraction strategy sees the trace, so an excluded LLM or tool run never affects detection, message extraction, or tool-call pairing.

`LS_MESSAGE_VIEW_EXCLUDE` is a top-level constant exported from `langsmith` (Python and JS) whose value is the string `"ls_message_view_exclude"`. Prefer the constant to avoid typos; the literal string still works.

Use it for LLM subspans that are not conversational turns, such as classification calls, embedding lookups, safety filters, or routing/guardrail decisions, that you still want visible elsewhere in LangSmith but do not want cluttering the conversation transcript.

> [tab] Python
>
> **1. On a `@traceable` decorator**: exclude a whole function's run.
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from langsmith import LS_MESSAGE_VIEW_EXCLUDE, traceable
>
> @traceable(run_type="llm", metadata={LS_MESSAGE_VIEW_EXCLUDE: True})
> def classify_intent(query: str) -> str:
>     # This LLM call is internal routing, not part of the chat
>     return llm.predict(f"Classify the intent of: {query}")
> ```
>
> **2. Via the `trace` context manager**: exclude an ad-hoc span.
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from langsmith import LS_MESSAGE_VIEW_EXCLUDE, trace
>
> with trace(
>     "safety_check",
>     run_type="llm",
>     metadata={LS_MESSAGE_VIEW_EXCLUDE: True},
> ) as run:
>     result = safety_model.score(text)
>     run.end(outputs={"score": result})
> ```
>
> **3. From inside a running function**: set the key on the current run tree at any point before the run is patched.
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from langsmith import LS_MESSAGE_VIEW_EXCLUDE, get_current_run_tree, traceable
>
> @traceable(run_type="llm")
> def maybe_internal(query: str) -> str:
>     result = llm.predict(query)
>     if _looks_like_routing(query):
>         rt = get_current_run_tree()
>         if rt is not None:
>             rt.add_metadata({LS_MESSAGE_VIEW_EXCLUDE: True})
>     return result
> ```
>
> **4. Per-call when using `wrap_openai` / `wrap_anthropic`**: pass `langsmith_extra` through to the wrapped client call.
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import openai
> from langsmith import LS_MESSAGE_VIEW_EXCLUDE
> from langsmith.wrappers import wrap_openai
>
> client = wrap_openai(openai.Client())
>
> resp = client.chat.completions.create(
>     model="gpt-5.6",
>     messages=[{"role": "user", "content": "Classify: ..."}],
>     langsmith_extra={"metadata": {LS_MESSAGE_VIEW_EXCLUDE: True}},
> )
> ```
>
> **5. LangChain `RunnableConfig`**: exclude a single invocation of a chain or chat model.
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from langchain_openai import ChatOpenAI
> from langsmith import LS_MESSAGE_VIEW_EXCLUDE
>
> llm = ChatOpenAI(model="gpt-5.6")
> result = llm.invoke(
>     "Classify this query",
>     config={"metadata": {LS_MESSAGE_VIEW_EXCLUDE: True}},
> )
> ```

> [tab] TypeScript
>
> **1. On a `traceable` wrapper**: exclude a whole function's run.
>
> ```typescript theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import { LS_MESSAGE_VIEW_EXCLUDE } from "langsmith";
> import { traceable } from "langsmith/traceable";
>
> const classifyIntent = traceable(
>   async (query: string) => {
>     return await llm.predict(`Classify the intent of: ${query}`);
>   },
>   {
>     name: "classify_intent",
>     run_type: "llm",
>     metadata: { [LS_MESSAGE_VIEW_EXCLUDE]: true },
>   },
> );
> ```
>
> **2. From inside a running function**: mutate the current run tree.
>
> ```typescript theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import { LS_MESSAGE_VIEW_EXCLUDE } from "langsmith";
> import { traceable, getCurrentRunTree } from "langsmith/traceable";
>
> const maybeInternal = traceable(
>   async (query: string) => {
>     const result = await llm.predict(query);
>     if (looksLikeRouting(query)) {
>       const rt = getCurrentRunTree();
>       rt.extra = rt.extra ?? {};
>       rt.extra.metadata = { ...rt.extra.metadata, [LS_MESSAGE_VIEW_EXCLUDE]: true };
>     }
>     return result;
>   },
>   { run_type: "llm" },
> );
> ```
>
> **3. Per-call with `wrapOpenAI`**: pass `langsmithExtra` on the call.
>
> ```typescript theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import { LS_MESSAGE_VIEW_EXCLUDE } from "langsmith";
> import { wrapOpenAI } from "langsmith/wrappers";
> import OpenAI from "openai";
>
> const client = wrapOpenAI(new OpenAI());
>
> const resp = await client.chat.completions.create(
>   {
>     model: "gpt-5.6",
>     messages: [{ role: "user", content: "Classify: ..." }],
>   },
>   { langsmithExtra: { metadata: { [LS_MESSAGE_VIEW_EXCLUDE]: true } } },
> );
> ```
>
> **4. Vercel AI SDK middleware**: pass the key via `lsConfig.metadata` on `wrapAISDK`. The middleware merges this onto every emitted LLM run.
>
> ```typescript theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import * as ai from "ai";
> import { LS_MESSAGE_VIEW_EXCLUDE } from "langsmith";
> import { wrapAISDK } from "langsmith/experimental/vercel";
>
> const { generateText } = wrapAISDK(ai, {
>   metadata: { [LS_MESSAGE_VIEW_EXCLUDE]: true },
> });
> ```
>
> To exclude only some calls and not others, wrap with `wrapAISDK` normally and instead mutate `getCurrentRunTree()` from inside a parent `traceable` that calls into the AI SDK, or use a child `RunTree` with `createChild({ extra: { metadata: { [LS_MESSAGE_VIEW_EXCLUDE]: true } } })`.
>
> **5. Manual `RunTree.createChild`**: when you are building runs by hand.
>
> ```typescript theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import { LS_MESSAGE_VIEW_EXCLUDE } from "langsmith";
> import { RunTree } from "langsmith/run_trees";
>
> const parent = new RunTree({ name: "agent", run_type: "chain" });
> const child = parent.createChild({
>   name: "safety_check",
>   run_type: "llm",
>   extra: { metadata: { [LS_MESSAGE_VIEW_EXCLUDE]: true } },
> });
> ```

### Notes

* The filter checks for the **presence of the key**, not truthiness. `{LS_MESSAGE_VIEW_EXCLUDE: false}` still excludes the run. Omit the key entirely to include the run.
* Child runs that execute inside a `@traceable` (Python) or `traceable` (JS) parent inherit the exclusion through the shared tracing context: Python's `_METADATA` `ContextVar` and JS's `AsyncLocalStorage`. The child's own decorator-time metadata layers on top of the inherited values.
* Excluded runs still appear in the regular trace view, runs explorer, and metrics. Only the Trajectory view filters them out.

## Manual instrumentation

If you trace without one of the wrappers in [Supported integrations](#supported-integrations) (for example, emitting runs through `RunTree`, the REST API, or a custom wrapper around a provider SDK), set `ls_message_format` on each LLM run's metadata to route the trace to the correct extractor:

| Trace shape | Set on metadata |
| - | - |
| LangChain messages (constructor envelope) | `ls_message_format: "langchain"` |
| OpenAI Chat Completions | `ls_message_format: "completions"` |
| OpenAI Responses API | `ls_message_format: "responses"` |
| Anthropic Messages API | `ls_message_format: "anthropic"` |

## Related

* [Configure threads](../Configure%20threads.md): how `thread_id` groups runs across LangSmith.
* [Coding agent metadata contract](../../Trace/Tracing%20setup/Integrations/Developer%20tools/Coding%20agent%20metadata%20contract.md): the full `ls_agent_type` schema.
* [View traces](../Viewing%20%26%20managing%20traces/View%20traces.md#trajectory-view): what the Trajectory view shows and how to customize it.

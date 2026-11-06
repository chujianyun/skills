# Interpreters

> Run lightweight code inside Deep Agents to compose tools, orchestrate subagents, and transform structured data

Interpreters give agents a programmable, **in-memory** workspace inside the agent loop. The agent writes code to complete a task, and the runtime executes it and returns only the relevant results. Intermediate results do not become part of the model context.

Where [sandboxes](Sandboxes.md) are a code-first way for acting on an environment (such as running commands, installing dependencies, and editing files), interpreters are a code-first way for composing tools, preserving state, and deciding what information should return to the model.

> [!WARNING]
>
> Interpreters are in [**beta**](https://docs.langchain.com/oss/python/versioning.md). APIs and lifecycle behavior may change between releases.

> [!NOTE]
>
> Interpreters require `langchain-quickjs>=0.3.0` and Python 3.11 or later.

## Why use interpreters?

Most agent work alternates between model reasoning and tool calls. A model can fire several tool calls in one turn, but that batch is fixed the moment it is emitted. Nothing can loop, branch on a result, retry a failure, or feed one call's output into the next without another model turn, and every result returns to the model's context. The model also decides how many calls to issue, so asking it to dispatch work across hundreds of items is unreliable, and it tends to cover a sample rather than every item.

Interpreters move that orchestration into code so the model reasons about *what* to do, not every intermediate step.

> [card] [Programmatic tool calling (PTC)](#programmatic-tool-calling-ptc)
>
> Call selected tools from interpreter code, including loops, retries, branching, and parallel batches.

> [card] [Dynamic subagents](#dynamic-subagents)
>
> Dispatch subagents from code for fan-out, verification, and recursive workflows over large inputs.

> [card] [Stateful work](#how-interpreters-work)
>
> Keep intermediate values in runtime state without overloading the model context.

> [card] [Deterministic transforms](#how-interpreters-work)
>
> Sort, group, parse, validate, score, and aggregate structured data without another model turn.

## Choose a pattern

Use interpreters for code inside the agent loop: composing tools, preserving state, and controlling what returns to the model.

Use [sandboxes](Sandboxes.md) for code against an environment: shell commands, package installs, tests, filesystem edits, and OS-level execution.

| Need | Use |
| - | - |
| One or two simple external calls | Normal tool calling |
| Pure in-memory JavaScript: loops, branches, retries, or data transforms (no external tools) | Interpreter |
| Many external tool calls orchestrated from code (requires [PTC](#programmatic-tool-calling-ptc)) | Interpreter with [programmatic tool calling (PTC)](#programmatic-tool-calling-ptc) |
| Many independent units of work, multiple perspectives, or recursive analysis over large inputs | Interpreter with [dynamic subagents](../Delegation/Dynamic%20subagents.md) |
| Shell commands, package installs, tests, or full OS filesystem access | [Sandboxes](Sandboxes.md) |

## Quickstart

Install the QuickJS middleware package, then pass interpreter middleware using the `middleware` argument on `create_deep_agent`.

```bash pip theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
pip install -U "deepagents[quickjs]"
```

```bash uv theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
uv add "deepagents[quickjs]"
```

```python Google theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from langchain_quickjs import CodeInterpreterMiddleware

agent = create_deep_agent(
    model="google_genai:gemini-3.6-flash",
    middleware=[CodeInterpreterMiddleware()],
)
```

```python OpenAI theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from langchain_quickjs import CodeInterpreterMiddleware

agent = create_deep_agent(
    model="openai:gpt-5.5",
    middleware=[CodeInterpreterMiddleware()],
)
```

```python Anthropic theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from langchain_quickjs import CodeInterpreterMiddleware

agent = create_deep_agent(
    model="anthropic:claude-sonnet-5",
    middleware=[CodeInterpreterMiddleware()],
)
```

```python OpenRouter theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from langchain_quickjs import CodeInterpreterMiddleware

agent = create_deep_agent(
    model="openrouter:z-ai/glm-5.2",
    middleware=[CodeInterpreterMiddleware()],
)
```

```python Fireworks theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from langchain_quickjs import CodeInterpreterMiddleware

agent = create_deep_agent(
    model="fireworks:accounts/fireworks/models/glm-5p2",
    middleware=[CodeInterpreterMiddleware()],
)
```

```python Baseten theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from langchain_quickjs import CodeInterpreterMiddleware

agent = create_deep_agent(
    model="baseten:zai-org/GLM-5.2",
    middleware=[CodeInterpreterMiddleware()],
)
```

```python Ollama theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from langchain_quickjs import CodeInterpreterMiddleware

agent = create_deep_agent(
    model="ollama:north-mini-code-1.0",
    middleware=[CodeInterpreterMiddleware()],
)
```

## How interpreters work

The middleware adds an `eval` tool to the agent. When useful, the agent writes JavaScript and calls `eval`; you do not call the interpreter directly. The tool runs code in a QuickJS context whose variables can persist between `eval` calls, depending on the persistence `mode`. It captures `console.log`, `console.warn`, and `console.error`, and returns the result of the last expression.

The agent can write code like this:

```ts theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
const rows = [
  { team: "alpha", score: 8 },
  { team: "beta", score: 13 },
  { team: "alpha", score: 21 },
];

const totals = rows.reduce((acc, row) => {
  acc[row.team] = (acc[row.team] ?? 0) + row.score;
  console.log(`${row.team} score: ${acc[row.team]}`);
  return acc;
}, {});

totals;
```

By default (`mode="thread"`), interpreter state persists across turns in the same thread. See [Persistence](#persistence) for `mode` options and the snapshot lifecycle.

Code runs against [**QuickJS**](https://github.com/quickjs-ng/quickjs), a lightweight JavaScript runtime. By default, interpreter code has no access to the host filesystem, network, shell, package manager, or clock. It can compute, hold state, and write to `console.log`, `console.warn`, or `console.error`, and nothing more.

Two explicit bridges extend that reach:

* **Tools**, through [programmatic tool calling (PTC)](#programmatic-tool-calling-ptc). Provide an allowlist of tools as async functions under the `tools` namespace. These can be the agent's own tools or standalone tools you define and pass in.
* **Subagents**, through [dynamic subagents](../Delegation/Dynamic%20subagents.md). When the agent has subagents configured, the interpreter exposes a `task()` global for dispatching them from code.

Programmatic tool calling is off until you [enable it](#enable-ptc). Subagent dispatch through `task()` is on by default whenever the agent has subagents, and you can turn it off. Nothing else crosses the QuickJS boundary.

## Programmatic tool calling (PTC)

Programmatic tool calling (PTC) exposes selected agent tools inside the interpreter under the global `tools` namespace. Instead of asking the model to issue one tool call, wait for the result, and then decide the next call, the agent can write code that calls tools in loops, branches, retries, or parallel batches.

This helps when intermediate results are only inputs to the next step: the interpreter filters or aggregates them before anything returns to the model, keeping multi-step workflows token-efficient. It is model-agnostic, implemented by middleware rather than a provider-specific tool-calling API.

The middleware exposes each allowlisted tool as an async function under `tools`. The agent calls it with `await`, processes the result in code, and the model sees only the final interpreter output, not every intermediate value. Tool names are converted to camelCase while the input object still follows the tool's schema, so a tool named `web_search` becomes `tools.webSearch(...)`:

```ts theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
const result: string = await tools.webSearch({
  query: "deepagents interpreters",
});
```

### Enable PTC

Enable PTC with an explicit allowlist:

```python Google theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from langchain_quickjs import CodeInterpreterMiddleware

agent = create_deep_agent(
    model="google_genai:gemini-3.6-flash",
    middleware=[CodeInterpreterMiddleware(ptc=["web_search"])],
)
```

```python OpenAI theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from langchain_quickjs import CodeInterpreterMiddleware

agent = create_deep_agent(
    model="openai:gpt-5.5",
    middleware=[CodeInterpreterMiddleware(ptc=["web_search"])],
)
```

```python Anthropic theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from langchain_quickjs import CodeInterpreterMiddleware

agent = create_deep_agent(
    model="anthropic:claude-sonnet-5",
    middleware=[CodeInterpreterMiddleware(ptc=["web_search"])],
)
```

```python OpenRouter theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from langchain_quickjs import CodeInterpreterMiddleware

agent = create_deep_agent(
    model="openrouter:z-ai/glm-5.2",
    middleware=[CodeInterpreterMiddleware(ptc=["web_search"])],
)
```

```python Fireworks theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from langchain_quickjs import CodeInterpreterMiddleware

agent = create_deep_agent(
    model="fireworks:accounts/fireworks/models/glm-5p2",
    middleware=[CodeInterpreterMiddleware(ptc=["web_search"])],
)
```

```python Baseten theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from langchain_quickjs import CodeInterpreterMiddleware

agent = create_deep_agent(
    model="baseten:zai-org/GLM-5.2",
    middleware=[CodeInterpreterMiddleware(ptc=["web_search"])],
)
```

```python Ollama theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from langchain_quickjs import CodeInterpreterMiddleware

agent = create_deep_agent(
    model="ollama:north-mini-code-1.0",
    middleware=[CodeInterpreterMiddleware(ptc=["web_search"])],
)
```

After PTC is enabled, the agent can call the allowlisted tool from interpreter code. This example searches several topics in parallel and combines the results before returning to the model:

```ts theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
const topics = ["retrieval", "memory", "evaluation"];

const results = await Promise.all(
  topics.map((topic) =>
    tools.webSearch({ query: `${topic} best practices 2025` }),
  ),
);

results.join("\n\n");
```

> [!WARNING]
>
> PTC calls currently execute through the interpreter bridge and do not go through the normal tool calling path. As a result, `interrupt_on` approval workflows are not enforced per PTC-invoked tool call.

## Dynamic subagents

The following overview below covers when to use dynamic subagents and a minimal `task()` pattern. For configuration, orchestration examples, workflow triggers, and safety notes, see [Dynamic subagents](../Delegation/Dynamic%20subagents.md).

Dynamic subagents let the interpreter dispatch configured [subagents](../Delegation/Subagents.md) from code using the built-in `task()` global. A task that spans many independent units, such as reviewing every file in a directory or triaging a batch of tickets, becomes a loop that fans out work and synthesizes the results.

Use dynamic subagents for:

* **Fan-out and synthesize**: Run the same kind of work across many items in parallel, then combine the results.
* **Verification**: Send findings to independent verifier subagents and keep only confirmed results.
* **Recursive workflows**: Keep a working set in interpreter variables, select slices, call subagents, and refine the result.

```ts theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
const paths = ["src/auth.ts", "src/routes/api.ts"];

const reviews = await Promise.all(
  paths.map((path) =>
    task({
      description: `Review ${path} for authentication issues`,
      subagentType: "reviewer",
    }),
  ),
);

reviews.join("\n\n");
```

## Persistence

Control cross-turn state with the `mode` parameter on `CodeInterpreterMiddleware`:

* **`"thread"`** (default): State persists across `eval` calls and across agent turns. The middleware snapshots interpreter state after each agent turn and restores it before the next turn.
* **`"turn"`**: State persists across multiple `eval` calls within one agent turn, then resets on the next turn.
* **`"call"`**: Each `eval` call runs in a fresh REPL with no carry-over from prior calls.

With `mode="thread"`, a snapshot is a serialized copy of the interpreter's in-memory JavaScript state, including globals, variables, functions, and imported modules that exist when the agent finishes running code. Across conversation turns, the lifecycle is:

1. A turn starts, and the middleware restores the latest interpreter snapshot for the thread.
2. The agent calls `eval` one or more times. Those calls share one live context; the middleware does not snapshot between them.
3. The turn finishes, and the middleware writes an updated snapshot to graph state.
4. The next turn resumes from that snapshot instead of an empty runtime.

> [!NOTE]
>
> Snapshots retain serializable data only. Functions, classes, and other unserializable runtime objects become inaccessible artifacts after restore. Accessing one throws an error like `Value for 'fn' was not restored because it is not serializable (type: function).`

Snapshots preserve interpreter memory, not outside-world effects. If interpreter code calls a tool through PTC, restoring a prior interpreter snapshot does not undo side effects from that tool call. It only restores the interpreter variables that recorded or processed the result.

Cross-turn persistence does not require a checkpointer:

```python Google theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from langchain_quickjs import CodeInterpreterMiddleware

agent = create_deep_agent(
    model="google_genai:gemini-3.6-flash",
    middleware=[
        CodeInterpreterMiddleware(
            mode="thread",  # Default
        )
    ],
)
```

```python OpenAI theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from langchain_quickjs import CodeInterpreterMiddleware

agent = create_deep_agent(
    model="openai:gpt-5.5",
    middleware=[
        CodeInterpreterMiddleware(
            mode="thread",  # Default
        )
    ],
)
```

```python Anthropic theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from langchain_quickjs import CodeInterpreterMiddleware

agent = create_deep_agent(
    model="anthropic:claude-sonnet-5",
    middleware=[
        CodeInterpreterMiddleware(
            mode="thread",  # Default
        )
    ],
)
```

```python OpenRouter theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from langchain_quickjs import CodeInterpreterMiddleware

agent = create_deep_agent(
    model="openrouter:z-ai/glm-5.2",
    middleware=[
        CodeInterpreterMiddleware(
            mode="thread",  # Default
        )
    ],
)
```

```python Fireworks theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from langchain_quickjs import CodeInterpreterMiddleware

agent = create_deep_agent(
    model="fireworks:accounts/fireworks/models/glm-5p2",
    middleware=[
        CodeInterpreterMiddleware(
            mode="thread",  # Default
        )
    ],
)
```

```python Baseten theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from langchain_quickjs import CodeInterpreterMiddleware

agent = create_deep_agent(
    model="baseten:zai-org/GLM-5.2",
    middleware=[
        CodeInterpreterMiddleware(
            mode="thread",  # Default
        )
    ],
)
```

```python Ollama theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from langchain_quickjs import CodeInterpreterMiddleware

agent = create_deep_agent(
    model="ollama:north-mini-code-1.0",
    middleware=[
        CodeInterpreterMiddleware(
            mode="thread",  # Default
        )
    ],
)
```

Because interpreter snapshots are stored in graph state, a [checkpointer](https://docs.langchain.com/oss/python/langgraph/checkpointers.md) also captures them in checkpoint history. Add one when you need durable threads or [time travel](https://docs.langchain.com/oss/python/langgraph/use-time-travel.md):

```python Google theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from langchain_quickjs import CodeInterpreterMiddleware
from langgraph.checkpoint.memory import MemorySaver

agent = create_deep_agent(
    model="google_genai:gemini-3.6-flash",
    checkpointer=MemorySaver(),
    middleware=[CodeInterpreterMiddleware(mode="thread")],
)
```

```python OpenAI theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from langchain_quickjs import CodeInterpreterMiddleware
from langgraph.checkpoint.memory import MemorySaver

agent = create_deep_agent(
    model="openai:gpt-5.5",
    checkpointer=MemorySaver(),
    middleware=[CodeInterpreterMiddleware(mode="thread")],
)
```

```python Anthropic theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from langchain_quickjs import CodeInterpreterMiddleware
from langgraph.checkpoint.memory import MemorySaver

agent = create_deep_agent(
    model="anthropic:claude-sonnet-5",
    checkpointer=MemorySaver(),
    middleware=[CodeInterpreterMiddleware(mode="thread")],
)
```

```python OpenRouter theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from langchain_quickjs import CodeInterpreterMiddleware
from langgraph.checkpoint.memory import MemorySaver

agent = create_deep_agent(
    model="openrouter:z-ai/glm-5.2",
    checkpointer=MemorySaver(),
    middleware=[CodeInterpreterMiddleware(mode="thread")],
)
```

```python Fireworks theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from langchain_quickjs import CodeInterpreterMiddleware
from langgraph.checkpoint.memory import MemorySaver

agent = create_deep_agent(
    model="fireworks:accounts/fireworks/models/glm-5p2",
    checkpointer=MemorySaver(),
    middleware=[CodeInterpreterMiddleware(mode="thread")],
)
```

```python Baseten theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from langchain_quickjs import CodeInterpreterMiddleware
from langgraph.checkpoint.memory import MemorySaver

agent = create_deep_agent(
    model="baseten:zai-org/GLM-5.2",
    checkpointer=MemorySaver(),
    middleware=[CodeInterpreterMiddleware(mode="thread")],
)
```

```python Ollama theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from langchain_quickjs import CodeInterpreterMiddleware
from langgraph.checkpoint.memory import MemorySaver

agent = create_deep_agent(
    model="ollama:north-mini-code-1.0",
    checkpointer=MemorySaver(),
    middleware=[CodeInterpreterMiddleware(mode="thread")],
)
```

Set `mode="turn"` to persist interpreter state only within a turn, or `mode="call"` for a fresh REPL on every `eval`.

## Security

Interpreters use QuickJS to run untrusted JavaScript with strict default isolation. Treat that as a scoped interpreter runtime, not a full production sandbox backend.

Every tool you expose through PTC is an outside capability that interpreter code can use. Treat the PTC allowlist as a permission boundary: expose only the tools the agent needs, and avoid bridging broad tools that can access sensitive systems, spend money, mutate data, or call unrestricted networks unless that behavior is intentional.

| Capability | Available by default | How to expose it |
| - | - | - |
| JavaScript execution | Yes | Add interpreter middleware |
| Top-level `await` | Yes | Use promises in interpreter code |
| `console.log`, `warn`, `error` capture | Yes | Disable with `capture_console=False` |
| Agent tools | No | Add a PTC allowlist |
| Filesystem access | No | Add the [built-in filesystem tools](../Deep%20Agents%20overview.md#virtual-filesystem-access) via the PTC allowlist |
| Network access | No | Expose a specific network tool through PTC |
| Wall-clock or datetime access | No | Expose an explicit time tool if needed |
| Shell commands, package installs, tests, OS-level execution | No | Use a [sandbox backend](Sandboxes.md) |

> [!NOTE]
>
> **How code execution works**
>
> Interpreter code runs in QuickJS compiled to WebAssembly, provided by [`quickjs-rs`](https://github.com/langchain-ai/quickjs-rs). The WebAssembly sandbox is the isolation boundary: JavaScript executes in the guest's linear memory and cannot read or write the host process's memory. Each LangGraph thread gets its own WebAssembly instance, so interpreter state on one thread cannot reach another.
>
> The sandbox runs inside the host process on [wasmtime](https://wasmtime.dev/), so a wasmtime vulnerability is the remaining path out of the sandbox. Keep `wasmtime` updated. For hostile multi-tenant workloads, also run agents in isolated worker processes or containers. For details, see the `quickjs-rs` [Security guide](https://github.com/langchain-ai/quickjs-rs#security).
>
> The sandbox contains the engine, not the capabilities you give it. Interpreter code can call every tool bridged into it, so keep the PTC allowlist narrow.

## Configuration

`CodeInterpreterMiddleware` accepts the following options:

| Kwarg | Default | Purpose |
| - | - | - |
| `memory_limit` | `64 * 1024 * 1024` (64 MB) | Cap QuickJS heap memory per thread. |
| `timeout` | `5.0` | Timeout limit in seconds for each `eval` call. |
| `tool_name` | `"eval"` | Name of the interpreter tool exposed to the model. |
| `capture_console` | `True` | Capture `console.log`, `console.warn`, and `console.error` in the tool response. Set to `False` to discard console output. |
| `max_result_chars` | `4000` | Truncate result, error, and stdout text returned to the model to a maximum character count. |
| `ptc` | `None` | Allowlist of tool names or `BaseTool` instances exposed as `tools.*` inside the interpreter. Omit to disable. See [Enable PTC](#enable-ptc). |
| `max_ptc_calls` | `256` | Maximum `tools.*` calls allowed per `eval`. Set to `None` only in trusted environments. See [Programmatic tool calling (PTC)](#programmatic-tool-calling-ptc) and [Security](#security). |
| `subagents` | `True` | Expose the built-in `task()` global when the agent has subagents. Set to `False` to require dispatch through the normal `task` tool. See [Dynamic subagents](#dynamic-subagents). |
| `mode` | `"thread"` | Control interpreter persistence: `"thread"` (across turns), `"turn"` (within one turn), or `"call"` (fresh REPL per `eval`). See [Persistence](#persistence). |
| `max_snapshot_bytes` | `None` | Drop snapshots larger than this byte limit. Defaults to `memory_limit`. See [Persistence](#persistence). |

***

[Connect these docs](https://docs.langchain.com/use-these-docs.md) to your agent of choice via MCP for real-time answers.

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/deepagents/interpreters.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).

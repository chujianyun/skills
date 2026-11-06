# Backends

> Choose and configure filesystem backends for Deep Agents. You can specify routes to different backends, implement virtual filesystems, and enforce policies.

Deep Agents expose a filesystem surface to the agent via tools like `ls`, `read_file`, `write_file`, `edit_file`, `delete`, `glob`, and `grep`. These tools operate through a pluggable backend. The `read_file` tool natively supports image files (`.png`, `.jpg`, `.jpeg`, `.gif`, `.webp`) across all backends, returning them as multimodal content blocks.

Sandboxes and the [`LocalShellBackend`](https://reference.langchain.com/python/deepagents/backends/local_shell/LocalShellBackend) also provide an `execute` tool.
This page explains how to:

* [Choose a backend](#specify-a-backend)

* [Route different paths to different backends](#route-to-different-backends)

* [Implement a custom backend](#custom-backends)

* [Set permissions](#permissions) on filesystem access

* [Comply with the backend protocol](#protocol-reference)

> [!TIP]
>
> When you deploy on [LangSmith Deployment](https://docs.langchain.com/langsmith/deployment.md), a store is provisioned automatically. Use [LangSmith](https://docs.langchain.com/langsmith/observability.md) tracing to debug file paths, permission denials, and cross-thread storage. Follow the [observability quickstart](https://docs.langchain.com/langsmith/observability-quickstart.md) to get set up.
>
> We recommend you also set up [LangSmith Engine](https://docs.langchain.com/langsmith/engine.md), which monitors your traces, detects issues, and proposes fixes.

> [!TIP]
>
> To generate a durable repository wiki that agents can read through filesystem tools, see [OpenWiki](../Context%20management/OpenWiki.md).

## Quickstart

Here are a few prebuilt filesystem backends that you can quickly use with your deep agent:

| Built-in backend | Description |
| - | - |
| [Default](#statebackend) | `agent = create_deep_agent(model="google_genai:gemini-3.6-flash")`  Thread-scoped. The default filesystem backend for an agent is stored in `langgraph` state. Files persist across turns within a thread (via your checkpointer) and are not shared across threads. |
| [Local filesystem persistence](#filesystembackend-local-disk) | `agent = create_deep_agent(model="google_genai:gemini-3.6-flash", backend=FilesystemBackend(root_dir="/Users/nh/Desktop/"))` This gives the deep agent access to your local machine's filesystem. You can specify the root directory that the agent has access to. Note that any provided `root_dir` must be an absolute path. Typically, wrap in a [CompositeBackend](#compositebackend-router) to keep internal agent data (offloaded tool results, conversation history) separate from your project files. |
| [Durable store (LangGraph store)](#storebackend-langgraph-store) | `agent = create_deep_agent(model="google_genai:gemini-3.6-flash", backend=StoreBackend())` This gives the agent access to long-term storage that is *persisted across threads*. This is great for storing longer term memories or instructions that are applicable to the agent over multiple executions. |
| [Context Hub](#contexthubbackend) | `agent = create_deep_agent(model="google_genai:gemini-3.6-flash", backend=ContextHubBackend("my-agent"))` Stores files durably in a LangSmith Hub repo, without provisioning a separate LangGraph store. |
| [Sandbox](Sandboxes.md) | `agent = create_deep_agent(model="google_genai:gemini-3.6-flash", backend=sandbox)` Execute code in isolated environments. Sandboxes provide filesystem tools plus the `execute` tool for running shell commands. Choose from LangSmith, AgentCore, Daytona, or other [sandbox integrations](https://docs.langchain.com/oss/python/integrations/sandboxes.md). |
| [Local shell](#localshellbackend-local-shell) | `agent = create_deep_agent(model="google_genai:gemini-3.6-flash", backend=LocalShellBackend(root_dir=".", env={"PATH": "/usr/bin:/bin"}))` Filesystem and shell execution directly on the host. No isolation—use only in controlled development environments. See [security considerations](#localshellbackend-local-shell) below. |
| [Composite](#compositebackend-router) | Thread-scoped by default, `/memories/` persisted across threads. The Composite backend is maximally flexible. You can specify different routes in the filesystem to point towards different backends. See Composite routing below for a ready-to-paste example. |

```mermaid theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
graph TB
    Tools[Filesystem Tools] --> Backend[Backend]

    Backend --> State[State]
    Backend --> Disk[Filesystem]
    Backend --> Store[Store]
    Backend --> ContextHub[Context Hub]
    Backend --> Sandbox[Sandbox]
    Backend --> LocalShell[Local Shell]
    Backend --> Composite[Composite]
    Backend --> Custom[Custom]

    Composite --> Router{Routes}
    Router --> State
    Router --> Disk
    Router --> Store
    Router --> ContextHub

    Sandbox --> Execute["#43; execute tool"]
    LocalShell --> Execute["#43; execute tool"]

    classDef trigger fill:#F6FFDB,stroke:#6E8900,stroke-width:2px,color:#2E3900
    classDef process fill:#E5F4FF,stroke:#006DDD,stroke-width:2px,color:#030710
    classDef decision fill:#FDF3FF,stroke:#7E65AE,stroke-width:2px,color:#504B5F
    classDef output fill:#EBD0F0,stroke:#885270,stroke-width:2px,color:#441E33

    class Tools trigger
    class Backend,State,Disk,Store,ContextHub,Sandbox,LocalShell,Composite,Custom process
    class Router decision
    class Execute output
```

## Built-in backends

### StateBackend

```python Google theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from deepagents.backends import StateBackend

# By default we provide a StateBackend
agent = create_deep_agent(model="google_genai:gemini-3.6-flash")

# Under the hood, it looks like
agent2 = create_deep_agent(
    model="google_genai:gemini-3.6-flash",
    backend=StateBackend(),
)
```

```python OpenAI theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from deepagents.backends import StateBackend

# By default we provide a StateBackend
agent = create_deep_agent(model="openai:gpt-5.5")

# Under the hood, it looks like
agent2 = create_deep_agent(
    model="openai:gpt-5.5",
    backend=StateBackend(),
)
```

```python Anthropic theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from deepagents.backends import StateBackend

# By default we provide a StateBackend
agent = create_deep_agent(model="anthropic:claude-sonnet-5")

# Under the hood, it looks like
agent2 = create_deep_agent(
    model="anthropic:claude-sonnet-5",
    backend=StateBackend(),
)
```

```python OpenRouter theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from deepagents.backends import StateBackend

# By default we provide a StateBackend
agent = create_deep_agent(model="openrouter:z-ai/glm-5.2")

# Under the hood, it looks like
agent2 = create_deep_agent(
    model="openrouter:z-ai/glm-5.2",
    backend=StateBackend(),
)
```

```python Fireworks theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from deepagents.backends import StateBackend

# By default we provide a StateBackend
agent = create_deep_agent(model="fireworks:accounts/fireworks/models/glm-5p2")

# Under the hood, it looks like
agent2 = create_deep_agent(
    model="fireworks:accounts/fireworks/models/glm-5p2",
    backend=StateBackend(),
)
```

```python Baseten theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from deepagents.backends import StateBackend

# By default we provide a StateBackend
agent = create_deep_agent(model="baseten:zai-org/GLM-5.2")

# Under the hood, it looks like
agent2 = create_deep_agent(
    model="baseten:zai-org/GLM-5.2",
    backend=StateBackend(),
)
```

```python Ollama theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from deepagents.backends import StateBackend

# By default we provide a StateBackend
agent = create_deep_agent(model="ollama:north-mini-code-1.0")

# Under the hood, it looks like
agent2 = create_deep_agent(
    model="ollama:north-mini-code-1.0",
    backend=StateBackend(),
)
```

**How it works:**

* Stores files in LangGraph agent state for the current thread via [`StateBackend`](https://reference.langchain.com/python/deepagents/backends/state/StateBackend).
* Persists across multiple agent turns on the same thread via checkpoints. Files are not shared across threads.

> [!WARNING]
>
> Designed to be used from within a graph. Calling backend methods (e.g., `state_backend.upload_files(...)`) outside of a graph run won't take effect until the graph executes.

**Best for:**

* A scratch pad for the agent to write intermediate results.
* Automatic eviction of large tool outputs which the agent can then read back in piece by piece.

Note that this backend is shared between the supervisor agent and subagents, and any files a subagent writes will remain in the LangGraph agent state
even after that subagent's execution is complete. Those files will continue to be available to the supervisor agent and other subagents.

### FilesystemBackend (local disk)

[`FilesystemBackend`](https://reference.langchain.com/python/deepagents/backends/filesystem/FilesystemBackend) reads and writes real files under a configurable root directory.

> [!WARNING]
>
> This backend grants agents direct filesystem read/write access.
> Use with caution and only in appropriate environments.
>
> **Appropriate use cases:**
>
> * Local development CLIs (coding assistants, development tools)
> * CI/CD pipelines (see security considerations below)
>
> **Inappropriate use cases:**
>
> * Web servers or HTTP APIs - use `StateBackend`, `StoreBackend`, or a [sandbox backend](Sandboxes.md) instead
>
> **Security risks:**
>
> * Agents can read any accessible file, including secrets (API keys, credentials, `.env` files)
> * Combined with network tools, secrets may be exfiltrated via SSRF attacks
> * File modifications are permanent and irreversible
>
> **Recommended safeguards:**
>
> 1. Enable [Human-in-the-Loop (HITL) middleware](../Steering/Human-in-the-loop.md) to review sensitive operations.
> 2. Exclude secrets from accessible filesystem paths (especially in CI/CD).
> 3. Use a [sandbox backend](Sandboxes.md) for production environments requiring filesystem interaction.
> 4. **Always** use `virtual_mode=True` with `root_dir` to enable path-based access restrictions (blocks `..`, `~`, and absolute paths outside root).
>
>    Note that the default (`virtual_mode=False`) provides no security even with `root_dir` set.

```python Google theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from deepagents.backends import FilesystemBackend

agent = create_deep_agent(
    model="google_genai:gemini-3.6-flash",
    backend=FilesystemBackend(root_dir=".", virtual_mode=True),
)
```

```python OpenAI theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from deepagents.backends import FilesystemBackend

agent = create_deep_agent(
    model="openai:gpt-5.5",
    backend=FilesystemBackend(root_dir=".", virtual_mode=True),
)
```

```python Anthropic theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from deepagents.backends import FilesystemBackend

agent = create_deep_agent(
    model="anthropic:claude-sonnet-5",
    backend=FilesystemBackend(root_dir=".", virtual_mode=True),
)
```

```python OpenRouter theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from deepagents.backends import FilesystemBackend

agent = create_deep_agent(
    model="openrouter:z-ai/glm-5.2",
    backend=FilesystemBackend(root_dir=".", virtual_mode=True),
)
```

```python Fireworks theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from deepagents.backends import FilesystemBackend

agent = create_deep_agent(
    model="fireworks:accounts/fireworks/models/glm-5p2",
    backend=FilesystemBackend(root_dir=".", virtual_mode=True),
)
```

```python Baseten theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from deepagents.backends import FilesystemBackend

agent = create_deep_agent(
    model="baseten:zai-org/GLM-5.2",
    backend=FilesystemBackend(root_dir=".", virtual_mode=True),
)
```

```python Ollama theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from deepagents.backends import FilesystemBackend

agent = create_deep_agent(
    model="ollama:north-mini-code-1.0",
    backend=FilesystemBackend(root_dir=".", virtual_mode=True),
)
```

**How it works:**

* Reads/writes real files under a configurable `root_dir`.
* You can optionally set `virtual_mode=True` to sandbox and normalize paths under `root_dir`.
* Uses secure path resolution, prevents unsafe symlink traversal when possible, can use ripgrep for fast `grep`.

**Best for:**

* Local projects on your machine
* CI sandboxes
* Mounted persistent volumes

For a durable repository wiki that agents can read with these filesystem tools (from `openwiki/`), see [OpenWiki](../Context%20management/OpenWiki.md).

> [!TIP]
>
> **Wrap `FilesystemBackend` in a `CompositeBackend`** for most use cases. Deep Agents automatically write internal data to the backend, including offloaded large tool results (under `/large_tool_results/`) and conversation history (under `/conversation_history/`). When you use `FilesystemBackend` alone, these internal files are written to real disk under `root_dir`, mixing agent artifacts with your project files.
>
> Use a `CompositeBackend` to route your project directory to `FilesystemBackend` while keeping internal paths in ephemeral `StateBackend` storage:
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from deepagents import create_deep_agent
> from deepagents.backends import CompositeBackend, StateBackend, FilesystemBackend
>
> agent = create_deep_agent(
>     backend=CompositeBackend(
>         default=StateBackend(),
>         routes={
>             "/workspace/": FilesystemBackend(root_dir="/path/to/project", virtual_mode=True),
>         },
>     )
> )
> ```
>
> This way, agent reads and writes under `/workspace/` go to real disk, while offloaded tool results and other internal data stay in ephemeral state. See [Route to different backends](#route-to-different-backends) for more routing patterns.

### LocalShellBackend (local shell)

> [!WARNING]
>
> This backend grants agents direct filesystem read/write access **and** unrestricted shell execution on your host.
> Use with extreme caution and only in appropriate environments.
>
> **Appropriate use cases:**
>
> * Local development CLIs (coding assistants, development tools)
> * Personal development environments where you trust the agent's code
> * CI/CD pipelines with proper secret management
>
> **Inappropriate use cases:**
>
> * Production environments (such as web servers, APIs, multi-tenant systems)
> * Processing untrusted user input or executing untrusted code
>
> **Security risks:**
>
> * Agents can execute **arbitrary shell commands** with your user's permissions
> * Agents can read any accessible file, including secrets (API keys, credentials, `.env` files)
> * Secrets may be exposed
> * File modifications and command execution are **permanent and irreversible**
> * Commands run directly on your host system
> * Commands can consume unlimited CPU, memory, disk
>
> **Recommended safeguards:**
>
> 1. Enable [Human-in-the-Loop (HITL) middleware](../Steering/Human-in-the-loop.md) to review and approve operations before execution. This is **strongly recommended**.
> 2. Run in dedicated development environments only. Never use on shared or production systems.
> 3. Use a [sandbox backend](Sandboxes.md) for production environments requiring shell execution.
>
> **Note:** `virtual_mode=True` provides no security with shell access enabled, since commands can access any path on the system.

```python Google theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from deepagents.backends import LocalShellBackend

agent = create_deep_agent(
    model="google_genai:gemini-3.6-flash",
    backend=LocalShellBackend(root_dir=".", virtual_mode=True, env={"PATH": "/usr/bin:/bin"}),
)
```

```python OpenAI theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from deepagents.backends import LocalShellBackend

agent = create_deep_agent(
    model="openai:gpt-5.5",
    backend=LocalShellBackend(root_dir=".", virtual_mode=True, env={"PATH": "/usr/bin:/bin"}),
)
```

```python Anthropic theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from deepagents.backends import LocalShellBackend

agent = create_deep_agent(
    model="anthropic:claude-sonnet-5",
    backend=LocalShellBackend(root_dir=".", virtual_mode=True, env={"PATH": "/usr/bin:/bin"}),
)
```

```python OpenRouter theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from deepagents.backends import LocalShellBackend

agent = create_deep_agent(
    model="openrouter:z-ai/glm-5.2",
    backend=LocalShellBackend(root_dir=".", virtual_mode=True, env={"PATH": "/usr/bin:/bin"}),
)
```

```python Fireworks theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from deepagents.backends import LocalShellBackend

agent = create_deep_agent(
    model="fireworks:accounts/fireworks/models/glm-5p2",
    backend=LocalShellBackend(root_dir=".", virtual_mode=True, env={"PATH": "/usr/bin:/bin"}),
)
```

```python Baseten theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from deepagents.backends import LocalShellBackend

agent = create_deep_agent(
    model="baseten:zai-org/GLM-5.2",
    backend=LocalShellBackend(root_dir=".", virtual_mode=True, env={"PATH": "/usr/bin:/bin"}),
)
```

```python Ollama theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from deepagents.backends import LocalShellBackend

agent = create_deep_agent(
    model="ollama:north-mini-code-1.0",
    backend=LocalShellBackend(root_dir=".", virtual_mode=True, env={"PATH": "/usr/bin:/bin"}),
)
```

**How it works:**

* Extends `FilesystemBackend` with the `execute` tool for running shell commands on the host.
* Commands run directly on your machine using `subprocess.run(shell=True)` with no sandboxing.
* Supports `timeout` (default 120s), `max_output_bytes` (default 100,000), `env`, and `inherit_env` for environment variables.
* Shell commands use `root_dir` as the working directory but can access any path on the system.

**Best for:**

* Local coding assistants and development tools
* Quick iteration during development when you trust the agent

### StoreBackend (LangGraph store)

```python Google theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from deepagents.backends import StoreBackend
from langgraph.store.memory import InMemoryStore

agent = create_deep_agent(
    model="google_genai:gemini-3.6-flash",
    backend=StoreBackend(
        namespace=lambda rt: (rt.server_info.user.identity,),
    ),
    store=InMemoryStore(),  # Good for local dev; omit for LangSmith Deployment
)
```

```python OpenAI theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from deepagents.backends import StoreBackend
from langgraph.store.memory import InMemoryStore

agent = create_deep_agent(
    model="openai:gpt-5.5",
    backend=StoreBackend(
        namespace=lambda rt: (rt.server_info.user.identity,),
    ),
    store=InMemoryStore(),  # Good for local dev; omit for LangSmith Deployment
)
```

```python Anthropic theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from deepagents.backends import StoreBackend
from langgraph.store.memory import InMemoryStore

agent = create_deep_agent(
    model="anthropic:claude-sonnet-5",
    backend=StoreBackend(
        namespace=lambda rt: (rt.server_info.user.identity,),
    ),
    store=InMemoryStore(),  # Good for local dev; omit for LangSmith Deployment
)
```

```python OpenRouter theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from deepagents.backends import StoreBackend
from langgraph.store.memory import InMemoryStore

agent = create_deep_agent(
    model="openrouter:z-ai/glm-5.2",
    backend=StoreBackend(
        namespace=lambda rt: (rt.server_info.user.identity,),
    ),
    store=InMemoryStore(),  # Good for local dev; omit for LangSmith Deployment
)
```

```python Fireworks theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from deepagents.backends import StoreBackend
from langgraph.store.memory import InMemoryStore

agent = create_deep_agent(
    model="fireworks:accounts/fireworks/models/glm-5p2",
    backend=StoreBackend(
        namespace=lambda rt: (rt.server_info.user.identity,),
    ),
    store=InMemoryStore(),  # Good for local dev; omit for LangSmith Deployment
)
```

```python Baseten theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from deepagents.backends import StoreBackend
from langgraph.store.memory import InMemoryStore

agent = create_deep_agent(
    model="baseten:zai-org/GLM-5.2",
    backend=StoreBackend(
        namespace=lambda rt: (rt.server_info.user.identity,),
    ),
    store=InMemoryStore(),  # Good for local dev; omit for LangSmith Deployment
)
```

```python Ollama theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from deepagents.backends import StoreBackend
from langgraph.store.memory import InMemoryStore

agent = create_deep_agent(
    model="ollama:north-mini-code-1.0",
    backend=StoreBackend(
        namespace=lambda rt: (rt.server_info.user.identity,),
    ),
    store=InMemoryStore(),  # Good for local dev; omit for LangSmith Deployment
)
```

> [!NOTE]
>
> When deploying to [LangSmith Deployment](https://docs.langchain.com/langsmith/deployment.md), omit the `store` parameter. The platform automatically provisions a store for your agent.

> [!TIP]
>
> The `namespace` parameter controls data isolation. For multi-user deployments, always set a [namespace factory](Backends.md#namespace-factories) to isolate data per user or tenant.

**How it works:**

* [`StoreBackend`](https://reference.langchain.com/python/deepagents/backends/store/StoreBackend) stores files in a LangGraph [`BaseStore`](https://reference.langchain.com/python/langchain-core/stores/BaseStore) provided by the runtime, enabling cross‑thread durable storage.

**Best for:**

* When you already run with a configured LangGraph store (for example, Redis, Postgres, or cloud implementations behind [`BaseStore`](https://reference.langchain.com/python/langchain-core/stores/BaseStore)).
* When you're deploying your agent through [LangSmith Deployment](https://docs.langchain.com/langsmith/deployment.md) (a store is automatically provisioned for your agent).

#### Namespace factories

A namespace factory controls where `StoreBackend` reads and writes data. It receives a LangGraph [`Runtime`](https://reference.langchain.com/python/langgraph/runtime/Runtime) and returns a tuple of strings used as the store namespace. Use namespace factories to isolate data between users, tenants, or assistants.

Pass the namespace factory to the `namespace` parameter when constructing a `StoreBackend`:

```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
NamespaceFactory = Callable[[Runtime], tuple[str, ...]]
```

The `Runtime` provides:

* `rt.context`—User-supplied context passed via LangGraph's [context schema](https://docs.langchain.com/oss/python/langgraph/graph-api.md#runtime-context) (for example, `user_id`)
* `rt.server_info`—Server-specific metadata when running on LangGraph Server (assistant ID, graph ID, authenticated user)
* `rt.execution_info`—Execution identity information (thread ID, run ID, checkpoint ID)

> [!NOTE]
>
> The `Runtime` argument is available in `deepagents>=0.5.2`. Earlier 0.5.x releases passed a `BackendContext` instead—see [migrating from `BackendContext`](#migrating-from-backendcontext) below. `rt.server_info` and `rt.execution_info` require `deepagents>=0.5.0`.

**Common namespace patterns:**

```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents.backends import StoreBackend

# Per-user: each user gets their own isolated storage
backend = StoreBackend(
    namespace=lambda rt: (rt.server_info.user.identity,),  # [!code highlight]
)

# Per-assistant: all users of the same assistant share storage
backend = StoreBackend(
    namespace=lambda rt: (
        rt.server_info.assistant_id,  # [!code highlight]
    ),
)

# Per-thread: storage scoped to a single conversation
backend = StoreBackend(
    namespace=lambda rt: (
        rt.execution_info.thread_id,  # [!code highlight]
    ),
)
```

You can combine multiple components to create more specific scopes—for example, `(user_id, thread_id)` for per-user per-conversation isolation, or append a suffix like `"filesystem"` to disambiguate when the same scope uses multiple store namespaces.

Namespace components must contain only alphanumeric characters, hyphens, underscores, dots, `@`, `+`, colons, and tildes. Wildcards (`*`, `?`) are rejected to prevent glob injection.

> [!WARNING]
>
> The `namespace` parameter will be **required** in v0.5.0. Always set it explicitly for new code.

> [!NOTE]
>
> When no namespace factory is provided, the legacy default uses the `assistant_id` from LangGraph config metadata. This means all users of the same [assistant](https://docs.langchain.com/langsmith/assistants.md) share the same storage. For multi-user [going to production](../Deployment/Going%20to%20production/index.md), always provide a namespace factory.

### ContextHubBackend

> [!NOTE]
>
> **Before you begin:** `ContextHubBackend` requires a Context Hub repo set up in LangSmith. Read the [Context Hub concepts](https://docs.langchain.com/langsmith/context-engineering-concepts.md) page first if you're unfamiliar with agent repos and skill repos.

`ContextHubBackend` stores your agent's filesystem in a LangSmith Context Hub repo. It can use a standalone repo or an agent repo that links out to skill repos.

**Repo structure:** In the Context Hub, an *agent repo* holds the agent's top-level instructions and configuration (for example, `AGENTS.md`, `tools.json`). It can link to one or more *skill repos*, each packaged as a reusable capability (for example, a `SKILL.md` with instructions for email formatting or code review). When you pass `ContextHubBackend("my-agent")`, the backend mounts the agent repo at the filesystem root; linked skill repos appear as subdirectories under `/skills/`.

This means your agent's context is intentionally spread across repos: one repo per agent, separate repos per skill. That separation lets skills be versioned, shared, and reused across multiple agents independently. If this feels fragmented, see [Linked repos](https://docs.langchain.com/langsmith/context-engineering-concepts.md#linked-repos) for the rationale.

```python Google theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from deepagents.backends import ContextHubBackend

agent = create_deep_agent(
    model="google_genai:gemini-3.6-flash",
    backend=ContextHubBackend("my-agent"),
)
```

```python OpenAI theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from deepagents.backends import ContextHubBackend

agent = create_deep_agent(
    model="openai:gpt-5.5",
    backend=ContextHubBackend("my-agent"),
)
```

```python Anthropic theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from deepagents.backends import ContextHubBackend

agent = create_deep_agent(
    model="anthropic:claude-sonnet-5",
    backend=ContextHubBackend("my-agent"),
)
```

```python OpenRouter theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from deepagents.backends import ContextHubBackend

agent = create_deep_agent(
    model="openrouter:z-ai/glm-5.2",
    backend=ContextHubBackend("my-agent"),
)
```

```python Fireworks theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from deepagents.backends import ContextHubBackend

agent = create_deep_agent(
    model="fireworks:accounts/fireworks/models/glm-5p2",
    backend=ContextHubBackend("my-agent"),
)
```

```python Baseten theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from deepagents.backends import ContextHubBackend

agent = create_deep_agent(
    model="baseten:zai-org/GLM-5.2",
    backend=ContextHubBackend("my-agent"),
)
```

```python Ollama theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from deepagents.backends import ContextHubBackend

agent = create_deep_agent(
    model="ollama:north-mini-code-1.0",
    backend=ContextHubBackend("my-agent"),
)
```

Construct it with a repo identifier in `owner/name` or `name` format.

> [!NOTE]
>
> Set `LANGSMITH_API_KEY` before using `ContextHubBackend`.

**How it works:**

* Pulls the Hub repo tree lazily on first use, then serves reads from an in-memory cache.
* Persists writes and edits as Hub commits and updates the cache after successful commits.
* Uses optimistic parent-commit writes (`parent_commit`): each push targets the latest known commit hash.

**Behavior and limits:**

* If the repo does not exist, first pull is treated as empty; the first successful write can create the repo.
* If another writer advances the repo first, your stale parent-commit write can fail. Re-pull and retry on conflict.
* `upload_files()` accepts UTF-8 text. Non-UTF-8 files are rejected per path with `invalid_path`.

**Best for:**

* LangSmith-native durable filesystem persistence without separately wiring a LangGraph `BaseStore`.
* Workflows that benefit from Hub commit history on filesystem changes.

### CompositeBackend (router)

```python Google theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from deepagents.backends import CompositeBackend, StateBackend, StoreBackend
from langgraph.store.memory import InMemoryStore

agent = create_deep_agent(
    model="google_genai:gemini-3.6-flash",
    backend=CompositeBackend(
        default=StateBackend(),
        routes={
            "/memories/": StoreBackend(namespace=lambda _rt: ("memories",)),
        },
    ),
    store=InMemoryStore(),  # Store passed to create_deep_agent, not backend
)
```

```python OpenAI theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from deepagents.backends import CompositeBackend, StateBackend, StoreBackend
from langgraph.store.memory import InMemoryStore

agent = create_deep_agent(
    model="openai:gpt-5.5",
    backend=CompositeBackend(
        default=StateBackend(),
        routes={
            "/memories/": StoreBackend(namespace=lambda _rt: ("memories",)),
        },
    ),
    store=InMemoryStore(),  # Store passed to create_deep_agent, not backend
)
```

```python Anthropic theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from deepagents.backends import CompositeBackend, StateBackend, StoreBackend
from langgraph.store.memory import InMemoryStore

agent = create_deep_agent(
    model="anthropic:claude-sonnet-5",
    backend=CompositeBackend(
        default=StateBackend(),
        routes={
            "/memories/": StoreBackend(namespace=lambda _rt: ("memories",)),
        },
    ),
    store=InMemoryStore(),  # Store passed to create_deep_agent, not backend
)
```

```python OpenRouter theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from deepagents.backends import CompositeBackend, StateBackend, StoreBackend
from langgraph.store.memory import InMemoryStore

agent = create_deep_agent(
    model="openrouter:z-ai/glm-5.2",
    backend=CompositeBackend(
        default=StateBackend(),
        routes={
            "/memories/": StoreBackend(namespace=lambda _rt: ("memories",)),
        },
    ),
    store=InMemoryStore(),  # Store passed to create_deep_agent, not backend
)
```

```python Fireworks theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from deepagents.backends import CompositeBackend, StateBackend, StoreBackend
from langgraph.store.memory import InMemoryStore

agent = create_deep_agent(
    model="fireworks:accounts/fireworks/models/glm-5p2",
    backend=CompositeBackend(
        default=StateBackend(),
        routes={
            "/memories/": StoreBackend(namespace=lambda _rt: ("memories",)),
        },
    ),
    store=InMemoryStore(),  # Store passed to create_deep_agent, not backend
)
```

```python Baseten theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from deepagents.backends import CompositeBackend, StateBackend, StoreBackend
from langgraph.store.memory import InMemoryStore

agent = create_deep_agent(
    model="baseten:zai-org/GLM-5.2",
    backend=CompositeBackend(
        default=StateBackend(),
        routes={
            "/memories/": StoreBackend(namespace=lambda _rt: ("memories",)),
        },
    ),
    store=InMemoryStore(),  # Store passed to create_deep_agent, not backend
)
```

```python Ollama theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from deepagents.backends import CompositeBackend, StateBackend, StoreBackend
from langgraph.store.memory import InMemoryStore

agent = create_deep_agent(
    model="ollama:north-mini-code-1.0",
    backend=CompositeBackend(
        default=StateBackend(),
        routes={
            "/memories/": StoreBackend(namespace=lambda _rt: ("memories",)),
        },
    ),
    store=InMemoryStore(),  # Store passed to create_deep_agent, not backend
)
```

**How it works:**

* [`CompositeBackend`](https://reference.langchain.com/python/deepagents/backends/composite/CompositeBackend) routes file operations to different backends based on path prefix.
* Preserves the original path prefixes in listings and search results.

**Best for:**

* When you want to give your agent both thread-scoped and cross-thread storage, a `CompositeBackend` allows you provide both a `StateBackend` and `StoreBackend`
* When you have multiple sources of information that you want to provide to your agent as part of a single filesystem.
  * e.g. You have long-term memories stored under `/memories/` in one Store and you also have a custom backend that has documentation accessible at /docs/.

## Specify a backend

* Pass a backend instance to `create_deep_agent(model=..., backend=...)`. The filesystem middleware uses it for all tooling.
* The backend must implement `BackendProtocol` (for example, `StateBackend()`, `FilesystemBackend(root_dir=".")`, `StoreBackend()`, `ContextHubBackend("my-agent")`).
* If omitted, the default is `StateBackend()`.

## Route to different backends

Route parts of the namespace to different backends. Commonly used to persist `/memories/*` across threads and keep everything else thread-scoped.

```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from deepagents.backends import CompositeBackend, StateBackend, FilesystemBackend

agent = create_deep_agent(
    model="google_genai:gemini-3.6-flash",
    backend=CompositeBackend(
        default=StateBackend(),
        routes={
            "/memories/": FilesystemBackend(root_dir="/deepagents/myagent", virtual_mode=True),
        },
    )
)
```

Behavior:

* `/workspace/plan.md` → `StateBackend` (thread-scoped)
* `/memories/agent.md` → `FilesystemBackend` under `/deepagents/myagent`
* `ls`, `glob`, `grep` aggregate results and show original path prefixes.

Notes:

* Longer prefixes win (for example, route `"/memories/projects/"` can override `"/memories/"`).
* For StoreBackend routing, ensure a store is provided via `create_deep_agent(model=..., store=...)` or provisioned by the platform.
* Deep Agents write internal data (offloaded tool results, conversation history) to the default backend. Use `StateBackend` as the default to keep these artifacts ephemeral and avoid writing them to disk or a persistent store. See the [FilesystemBackend tip](#filesystembackend-local-disk) for a complete example.

## Offload binary content

Binary content offloading stores inline media in the backend instead of keeping base64 payloads in message history. This reduces checkpoint size for agents that read binary files or receive inline media in user messages. Offloading is opt-in and disabled by default.

> [!NOTE]
>
> Binary content offloading requires `deepagents>=0.7.21`.

Set `offload_binary_content=True` on `FilesystemMiddleware` and pass it in the `middleware` list to `create_deep_agent`. Use the same backend for the agent and the middleware.

Payloads are stored under `/blobs/<sha256>` by default. If you set `artifacts_root` on the middleware, blobs are stored under that root instead.

Message history keeps content-addressed references. Before each model call, the middleware restores the original media from its cache or the backend. Re-reading unchanged content reuses the same blob; changed content creates a new blob.

Use a backend that stores blobs outside graph state, such as a sandbox or `FilesystemBackend`. Offloading has no effect when the blob path routes to `StateBackend`, including through `CompositeBackend`. If you keep `StateBackend` as the default backend, route the blob directory to external storage.

> [!NOTE]
>
> Inline media in user messages is replaced at the next model call. The original input payload still appears in earlier checkpoints. Keep the blob storage available when resuming a thread so the middleware can restore its media.

## Custom backends

Implement a custom backend to connect Deep Agents to storage systems such as databases, object stores, and remote filesystems. See [community-built backends](https://docs.langchain.com/oss/python/integrations/backends.md) for examples.

### Implement the backend protocol

Subclass [`BackendProtocol`](https://reference.langchain.com/python/deepagents/backends/protocol/BackendProtocol) and implement the following methods:

| Method | Signature | What it does | | |
| - | - | - | - | - |
| `ls` | `(path: str) -> LsResult` | List files and directories at the given path. | | |
| `read` | `(file_path: str, offset: int, limit: int) -> ReadResult` | Return file contents, optionally paginated. | | |
| `write` | `(file_path: str, content: str) -> WriteResult` | Create or overwrite a file. | | |
| `edit` | `(file_path: str, old_string: str, new_string: str, replace_all: bool) -> EditResult` | Find-and-replace within an existing file. | | |
| `glob` | \`(pattern: str, path: str | None) -> GlobResult\` | Return paths matching a glob pattern. | |
| `grep` | \`(pattern: str, path: str | None, glob: str | None) -> GrepResult\` | Search file contents for a literal string. |
| `delete` | `(file_path: str) -> DeleteResult` | Optional. Remove a file or, recursively, a directory. If the backend does not support deletion, the tool is automatically hidden from the model at request time. | | |

To also support the `execute` tool (running shell commands), implement [`SandboxBackendProtocol`](https://reference.langchain.com/python/deepagents/backends/protocol/SandboxBackendProtocol) instead, which extends `BackendProtocol` with an `execute` method.

Always return structured result types with an `error` field for failure cases. Do not raise exceptions.

> [accordion] Example: S3-style backend skeleton
>
> This skeleton maps filesystem paths to object keys. Fill in each method with your storage client's list, read, search, upload, and read-modify-write operations.
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from deepagents.backends.protocol import (
>     BackendProtocol,
>     EditResult,
>     GlobResult,
>     GrepResult,
>     LsResult,
>     ReadResult,
>     WriteResult,
> )
>
> class S3Backend(BackendProtocol):
>     def __init__(self, bucket: str, prefix: str = ""):
>         self.bucket = bucket
>         self.prefix = prefix.rstrip("/")
>
>     def _key(self, path: str) -> str:
>         return f"{self.prefix}{path}"
>
>     def ls(self, path: str) -> LsResult:
>         ...
>
>     def read(self, file_path: str, offset: int = 0, limit: int = 2000) -> ReadResult:
>         ...
>
>     def grep(self, pattern: str, path: str | None = None, glob: str | None = None) -> GrepResult:
>         ...
>
>     def glob(self, pattern: str, path: str | None = None) -> GlobResult:
>         ...
>
>     def write(self, file_path: str, content: str) -> WriteResult:
>         ...
>
>     def edit(self, file_path: str, old_string: str, new_string: str, replace_all: bool = False) -> EditResult:
>         ...
> ```

## Permissions

Use [permissions](Permissions.md) to declaratively control which files and directories the agent can read or write. Permissions apply to the built-in filesystem tools and are evaluated before the backend is called.

```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent, FilesystemPermission

agent = create_deep_agent(
    model="google_genai:gemini-3.6-flash",
    backend=CompositeBackend(
        default=StateBackend(),
        routes={
            "/memories/": StoreBackend(
                namespace=lambda rt: (rt.server_info.user.identity,),
            ),
            "/policies/": StoreBackend(
                namespace=lambda rt: (rt.context.org_id,),
            ),
        },
    ),
    permissions=[
        FilesystemPermission(
            operations=["write"],
            paths=["/policies/**"],
            mode="deny",
        ),
    ],
)
```

For the full set of options including rule ordering, subagent permissions, and composite backend interactions, see the [permissions guide](Permissions.md).

## Add policy hooks

For custom validation logic beyond path-based allow/deny rules (rate limiting, audit logging, content inspection), enforce enterprise rules by subclassing or wrapping a backend.

Block writes/edits under selected prefixes (subclass):

```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents.backends.filesystem import FilesystemBackend
from deepagents.backends.protocol import WriteResult, EditResult

class GuardedBackend(FilesystemBackend):
    def __init__(self, *, deny_prefixes: list[str], **kwargs):
        super().__init__(**kwargs)
        self.deny_prefixes = [p if p.endswith("/") else p + "/" for p in deny_prefixes]

    def write(self, file_path: str, content: str) -> WriteResult:
        if any(file_path.startswith(p) for p in self.deny_prefixes):
            return WriteResult(error=f"Writes are not allowed under {file_path}")
        return super().write(file_path, content)

    def edit(self, file_path: str, old_string: str, new_string: str, replace_all: bool = False) -> EditResult:
        if any(file_path.startswith(p) for p in self.deny_prefixes):
            return EditResult(error=f"Edits are not allowed under {file_path}")
        return super().edit(file_path, old_string, new_string, replace_all)
```

Generic wrapper (works with any backend):

```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents.backends.protocol import (
    BackendProtocol, WriteResult, EditResult, LsResult, ReadResult, GrepResult, GlobResult,
)

class PolicyWrapper(BackendProtocol):
    def __init__(self, inner: BackendProtocol, deny_prefixes: list[str] | None = None):
        self.inner = inner
        self.deny_prefixes = [p if p.endswith("/") else p + "/" for p in (deny_prefixes or [])]

    def _deny(self, path: str) -> bool:
        return any(path.startswith(p) for p in self.deny_prefixes)

    def ls(self, path: str) -> LsResult:
        return self.inner.ls(path)

    def read(self, file_path: str, offset: int = 0, limit: int = 2000) -> ReadResult:
        return self.inner.read(file_path, offset=offset, limit=limit)
    def grep(self, pattern: str, path: str | None = None, glob: str | None = None) -> GrepResult:
        return self.inner.grep(pattern, path, glob)
    def glob(self, pattern: str, path: str | None = None) -> GlobResult:
        return self.inner.glob(pattern, path)
    def write(self, file_path: str, content: str) -> WriteResult:
        if self._deny(file_path):
            return WriteResult(error=f"Writes are not allowed under {file_path}")
        return self.inner.write(file_path, content)
    def edit(self, file_path: str, old_string: str, new_string: str, replace_all: bool = False) -> EditResult:
        if self._deny(file_path):
            return EditResult(error=f"Edits are not allowed under {file_path}")
        return self.inner.edit(file_path, old_string, new_string, replace_all)
```

## Migrate from backend factories

> [!WARNING]
>
> The backend factory pattern is **deprecated** as of `deepagents` 0.5.0. Pass pre-constructed backend instances directly instead of factory functions.

Previously, backends like `StateBackend` and `StoreBackend` required a factory function that received a runtime object, because they needed runtime context (state, store) to operate. Backends now resolve this context internally via LangGraph's `get_config()`, `get_store()`, and `get_runtime()` helpers, so you can pass instances directly.

### What changed

| Before (deprecated) | After |
| - | - |
| `backend=lambda rt: StateBackend(rt)` | `backend=StateBackend()` |
| `backend=lambda rt: StoreBackend(rt)` | `backend=StoreBackend()` |
| `backend=lambda rt: CompositeBackend(default=StateBackend(rt), ...)` | `backend=CompositeBackend(default=StateBackend(), ...)` |
| `backend: (config) => new StateBackend(config)` | `backend: new StateBackend()` |
| `backend: (config) => new StoreBackend(config)` | `backend: new StoreBackend()` |

### Deprecated APIs

| Deprecated | Replacement |
| - | - |
| Passing a callable to `backend=` in `create_deep_agent` | Pass a backend instance directly |
| `runtime` constructor argument on `StateBackend(runtime)` | `StateBackend()` (no arguments needed) |
| `runtime` constructor argument on `StoreBackend(runtime)` | `StoreBackend()` or `StoreBackend(namespace=..., store=...)` |
| `files_update` field on `WriteResult` and `EditResult` | State writes are now handled internally by the backend |
| `Command` wrapping in middleware write/edit tools | Tools return plain strings; no `Command(update=...)` needed |

> [!NOTE]
>
> The factory pattern still works at runtime and emits a deprecation warning. Update your code to use direct instances before the next major version.

### Migration example

```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
# Before (deprecated)
from deepagents import create_deep_agent
from deepagents.backends import CompositeBackend, StateBackend, StoreBackend

agent = create_deep_agent(
    model="google_genai:gemini-3.6-flash",
    backend=lambda rt: CompositeBackend(
        default=StateBackend(rt),
        routes={"/memories/": StoreBackend(rt, namespace=lambda rt: (rt.server_info.user.identity,))},
    ),
)

# After
agent = create_deep_agent(
    model="google_genai:gemini-3.6-flash",
    backend=CompositeBackend(
        default=StateBackend(),
        routes={"/memories/": StoreBackend(namespace=lambda rt: (rt.server_info.user.identity,))},
    ),
)
```

### Migrating from `BackendContext`

In `deepagents>=0.5.2` (Python) and `deepagents>=1.9.1` (TypeScript), namespace factories receive a LangGraph [`Runtime`](https://reference.langchain.com/python/langgraph/runtime/Runtime) directly instead of a `BackendContext` wrapper. The old `BackendContext` form still works via backwards-compatible `.runtime` and `.state` accessors, but those accessors emit a deprecation warning and will be removed in `deepagents>=0.7`.

**What changed:**

* The factory argument is now a `Runtime`, not a `BackendContext`.
* Drop the `.runtime` accessor—for example, `ctx.runtime.context.user_id` becomes `rt.server_info.user.identity`.
* There is no direct replacement for `ctx.state`. Namespace info should be read-only and stable for the lifetime of a run, whereas state is mutable and changes step-to-step—deriving a namespace from it risks data ending up under inconsistent keys. If you have a use case that requires reading agent state, please [open an issue](https://github.com/langchain-ai/deepagents/issues).

```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
# Before (deprecated, removed in v0.7)
StoreBackend(
    namespace=lambda ctx: (ctx.runtime.context.user_id,),  # [!code --]
)

# After
StoreBackend(
    namespace=lambda rt: (rt.server_info.user.identity,),  # [!code ++]
)
```

## Protocol reference

Backends must implement [`BackendProtocol`](https://reference.langchain.com/python/deepagents/backends/protocol/BackendProtocol).

Required methods:

* `ls(path: str) -> LsResult`
  * Return entries with at least `path`. Include `is_dir`, `size`, `modified_at` when available. Sort by `path` for deterministic output.
* `read(file_path: str, offset: int = 0, limit: int = 2000) -> ReadResult`
  * Return file data on success. On missing file, return `ReadResult(error="Error: File '/x' not found")`.
* `grep(pattern: str, path: Optional[str] = None, glob: Optional[str] = None) -> GrepResult`
  * Return structured matches. On error, return `GrepResult(error="...")` (do not raise).
* `glob(pattern: str, path: Optional[str] = None) -> GlobResult`
  * Return matched files as `FileInfo` entries (empty list if none).
* `write(file_path: str, content: str) -> WriteResult`
  * Create-only. On conflict, return `WriteResult(error=...)`. On success, set `path` and for state backends set `files_update={...}`; external backends should use `files_update=None`.
* `edit(file_path: str, old_string: str, new_string: str, replace_all: bool = False) -> EditResult`
  * Enforce uniqueness of `old_string` unless `replace_all=True`. If not found, return error. Include `occurrences` on success.

Supporting types:

* `LsResult(error, entries)`—`entries` is a `list[FileInfo]` on success, `None` on failure.
* `ReadResult(error, file_data)`—`file_data` is a `FileData` dict on success, `None` on failure.
* `GrepResult(error, matches)`—`matches` is a `list[GrepMatch]` on success, `None` on failure.
* `GlobResult(error, matches)`—`matches` is a `list[FileInfo]` on success, `None` on failure.
* `WriteResult(error, path, files_update)`
* `EditResult(error, path, files_update, occurrences)`
* `FileInfo` with fields: `path` (required), optionally `is_dir`, `size`, `modified_at`.
* `GrepMatch` with fields: `path`, `line`, `text`.
* `FileData` with fields: `content` (str), `encoding` (`"utf-8"` or `"base64"`), `created_at`, `modified_at`.

## See also

* [OpenWiki](../Context%20management/OpenWiki.md): Generate durable repository Markdown that agents read through filesystem tools
* [Memory](../Context%20management/Memory.md): Filesystem-backed long-term memory
* [Sandboxes](Sandboxes.md): Isolated filesystem and shell execution

***

[Connect these docs](https://docs.langchain.com/use-these-docs.md) to your agent of choice via MCP for real-time answers.

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/deepagents/backends.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).

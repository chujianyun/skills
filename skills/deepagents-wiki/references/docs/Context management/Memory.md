# Memory

> Add persistent memory to agents built with Deep Agents so they learn and improve across conversations

Memory lets your agent learn and improve across conversations. Deep Agents makes memory first class with filesystem-backed memory: the agent reads and writes memory as files, and you control where those files are stored using [backends](../Execution%20environment/Backends.md).

> [!TIP]
>
> To generate a repository wiki that coding agents discover through [`AGENTS.md`](https://agents.md/), see [OpenWiki](OpenWiki.md).

> [!NOTE]
>
> This page covers **long-term memory**: memory that persists across conversations. For short-term memory (conversation history and scratch files within a single session), see the [context engineering](Context%20engineering%20in%20Deep%20Agents.md) guide. Short-term memory is managed automatically as part of the agent's [state](https://docs.langchain.com/oss/python/langgraph/graph-api.md#state).
>
> ![Short-term memory is scoped to a single thread via checkpoints; long-term memory persists across threads via the store](../../assets/images/memory.png)

## How memory works

1. **Point the agent at memory files.** Pass file paths to `memory=` when creating the agent. You can also pass [skills](Skills.md) via `skills=` for procedural memory (reusable instructions that tell the agent *how* to perform a task). A [backend](../Execution%20environment/Backends.md) controls where files are stored and who can access them.
2. **Agent reads memory.** The agent can load memory files into the system prompt at startup, or read them on demand during the conversation. For example, [skills](Skills.md) use on-demand loading: the agent reads only skill descriptions at startup, then reads the full skill file only when it matches a task. This keeps context lean until a capability is needed.
3. **Agent updates memory (optional).** When the agent learns new information, it can use its built-in `edit_file` tool to update memory files. Updates can happen during the conversation (the default) or in the background between conversations via [background consolidation](#background-consolidation). Changes are persisted and available in the next conversation. Not all memory is writable: developer-defined [skills](Skills.md) and [organization policies](#organization-level-memory) are typically read-only. See [read-only vs writable memory](#read-only-vs-writable-memory) for details.

The two most common patterns are [agent-scoped memory](#agent-scoped-memory) (shared across all users) and [user-scoped memory](#user-scoped-memory) (isolated per user).

For a generated repository wiki that coding agents discover through [`AGENTS.md`](https://agents.md/), see [OpenWiki](OpenWiki.md).

## Scoped memory

Agent memory can be scoped so the same memory files are accessible to everyone using the agent or memory files can be individual to each user.

### Agent-scoped memory

Give the agent its own persistent identity that evolves over time. Agent-scoped memory is shared across all users, so the agent builds up its own persona, accumulated knowledge, and learned preferences through every conversation. As it interacts with users, it develops expertise, refines its approach, and remembers what works. It can also learn and update [skills](Skills.md) when it has write access.

The key is the backend namespace: setting it to `(assistant_id,)` means every conversation for this agent reads and writes to the same memory file.

> [!NOTE]
>
> Accessing `rt.server_info` requires `deepagents>=0.5.0`. On older versions, read the assistant ID from `get_config()["metadata"]["assistant_id"]` instead.

```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from deepagents.backends import CompositeBackend, StateBackend, StoreBackend

agent = create_deep_agent(
    model="google_genai:gemini-3.6-flash",
    memory=["/memories/AGENTS.md"],
    skills=["/skills/"],
    backend=CompositeBackend(
        default=StateBackend(),
        routes={
            "/memories/": StoreBackend(
                namespace=lambda rt: (
                    rt.server_info.assistant_id,  # [!code highlight]
                ),
            ),
            "/skills/": StoreBackend(
                namespace=lambda rt: (
                    rt.server_info.assistant_id,  # [!code highlight]
                ),
            ),
        },
    ),
)
```

> [accordion] Full example: seed memory and invoke
>
> Populate the store with initial memories, then invoke the agent across two threads to see it remember and update what it learns.
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from langchain_core.utils.uuid import uuid7
>
> from deepagents import create_deep_agent
> from deepagents.backends import CompositeBackend, StateBackend, StoreBackend
> from deepagents.backends.utils import create_file_data
> from langgraph.store.memory import InMemoryStore
>
> store = InMemoryStore()  # Use platform store when deploying to LangSmith
>
> # Seed the memory file
> store.put(
>     ("my-agent",),
>     "/memories/AGENTS.md",
>     create_file_data("""## Response style
> - Keep responses concise
> - Use code examples where possible
> """),
> )
>
> # Seed a skill
> store.put(
>     ("my-agent",),
>     "/skills/langgraph-docs/SKILL.md",
>     create_file_data("""---
> name: langgraph-docs
> description: Fetch relevant LangGraph documentation to provide accurate guidance.
> ---
>
> # langgraph-docs
>
> Use the fetch_url tool to read https://docs.langchain.com/llms.txt, then fetch relevant pages.
> """),
> )
>
> agent = create_deep_agent(
>     model="google_genai:gemini-3.6-flash",
>     memory=["/memories/AGENTS.md"],
>     skills=["/skills/"],
>     backend=lambda rt: CompositeBackend(
>         default=StateBackend(rt),
>         routes={
>             "/memories/": StoreBackend(
>                 rt, namespace=lambda rt: ("my-agent",)
>             ),
>             "/skills/": StoreBackend(
>                 rt, namespace=lambda rt: ("my-agent",)
>             ),
>         },
>     ),
>     store=store,
> )
>
> # Thread 1: the agent learns a new preference and saves it to memory
> config1 = {"configurable": {"thread_id": str(uuid7())}}
> agent.invoke(
>     {"messages": [{"role": "user", "content": "I prefer detailed explanations. Remember that."}]},
>     config=config1,
> )
>
> # Thread 2: the agent reads memory and applies the preference
> config2 = {"configurable": {"thread_id": str(uuid7())}}
> agent.invoke(
>     {"messages": [{"role": "user", "content": "Explain how transformers work."}]},
>     config=config2,
> )
> ```

### User-scoped memory

Give each user their own memory file. The agent remembers preferences, context, and history per user while core agent instructions stay fixed. Users can also have per-user [skills](Skills.md) if stored in a user-scoped backend.

The namespace uses `(user_id,)` so each user gets an isolated copy of the memory file. User A's preferences never leak into User B's conversations.

```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from deepagents.backends import CompositeBackend, StateBackend, StoreBackend

agent = create_deep_agent(
    model="google_genai:gemini-3.6-flash",
    memory=["/memories/preferences.md"],
    skills=["/skills/"],
    backend=CompositeBackend(
        default=StateBackend(),
        routes={
            "/memories/": StoreBackend(
                namespace=lambda rt: (rt.server_info.user.identity,),
            ),
            "/skills/": StoreBackend(
                namespace=lambda rt: (rt.server_info.user.identity,),
            ),
        },
    ),
)
```

> [accordion] Full example: isolated memory across users
>
> Seed per-user memories and invoke the agent as two different users. Each user sees only their own preferences.
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from langchain_core.utils.uuid import uuid7
>
> from deepagents import create_deep_agent
> from deepagents.backends import CompositeBackend, StateBackend, StoreBackend
> from deepagents.backends.utils import create_file_data
> from langgraph.store.memory import InMemoryStore
>
>
> store = InMemoryStore()  # Use platform store when deploying to LangSmith
>
> # Seed preferences for two users
> store.put(
>     ("user-alice",),
>     "/memories/preferences.md",
>     create_file_data("""## Preferences
> - Likes concise bullet points
> - Prefers Python examples
> """),
> )
> store.put(
>     ("user-bob",),
>     "/memories/preferences.md",
>     create_file_data("""## Preferences
> - Likes detailed explanations
> - Prefers TypeScript examples
> """),
> )
>
> # Seed a skill for Alice
> store.put(
>     ("user-alice",),
>     "/skills/langgraph-docs/SKILL.md",
>     create_file_data("""---
> name: langgraph-docs
> description: Fetch relevant LangGraph documentation to provide accurate guidance.
> ---
>
> # langgraph-docs
>
> Use the fetch_url tool to read https://docs.langchain.com/llms.txt, then fetch relevant pages.
> """),
> )
>
> agent = create_deep_agent(
>     model="google_genai:gemini-3.6-flash",
>     memory=["/memories/preferences.md"],
>     skills=["/skills/"],
>     backend=lambda rt: CompositeBackend(
>         default=StateBackend(rt),
>         routes={
>             "/memories/": StoreBackend(
>                 rt,
>                 namespace=lambda rt: (rt.server_info.user.identity,),
>             ),
>             "/skills/": StoreBackend(
>                 rt,
>                 namespace=lambda rt: (rt.server_info.user.identity,),
>             ),
>         },
>     ),
>     store=store,
> )
>
> # When deployed, each authenticated request resolves
> # `rt.server_info.user.identity` to the calling user, so Alice and Bob
> # automatically see only their own preferences.
> agent.invoke(
>     {"messages": [{"role": "user", "content": "How do I read a CSV file?"}]},
>     config={"configurable": {"thread_id": str(uuid7())}},
> )
> ```

## Advanced usage

On top of the basic configuration options for memory paths and scope, you can also configure more advanced parameters for memory:

| Dimension | Question it answers | Options |
| - | - | - |
| **Duration** | How long does it last? | [Short-term](Context%20engineering%20in%20Deep%20Agents.md) (single conversation) or [long-term](#scoped-memory) (across conversations) |
| **Information type** | What kind of information is it? | [Episodic](#episodic-memory) (past experiences), [procedural](Skills.md) (instructions and skills), or [semantic](https://docs.langchain.com/oss/python/concepts/memory.md#semantic-memory) (facts) |
| **Scope** | Who can see and modify it? | [User](#user-scoped-memory), [agent](#agent-scoped-memory), or [organization](#organization-level-memory) |
| **Update strategy** | When are memories written? | During conversation (default) or [between conversations](#background-consolidation) |
| **Retrieval** | How are memories read? | Loaded into prompt (default) or on demand (e.g., [skills](Skills.md)) |
| **Agent permissions** | Can the agent write to memory? | [Read-write](#read-only-vs-writable-memory) (default) or [read-only](#read-only-vs-writable-memory) (for shared policies) |

### Episodic memory

Episodic memory stores records of past experiences: what happened, in what order, and what the outcome was. Unlike semantic memory (facts and preferences stored in files like `AGENTS.md`), episodic memory preserves the full conversational context so the agent can recall *how* a problem was solved, not just *what* was learned from it. To generate and maintain a repository-level wiki for coding agents, see [OpenWiki](OpenWiki.md).

Deep Agents already use [checkpointers](https://docs.langchain.com/oss/python/langgraph/checkpointers.md#checkpoints) which is the mechanism that supports episodic memory: every conversation is persisted as a checkpointed thread.

To make past conversations searchable, wrap thread search in a tool. The `user_id` is pulled from the runtime context rather than passed as a parameter:

```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from langgraph_sdk import get_client
from langchain.tools import tool, ToolRuntime

client = get_client(url="<DEPLOYMENT_URL>")


@tool
async def search_past_conversations(query: str, runtime: ToolRuntime) -> str:
    """Search past conversations for relevant context."""
    user_id = runtime.server_info.user.identity  # [!code highlight]
    threads = await client.threads.search(
        metadata={"user_id": user_id},
        limit=5,
    )
    results = []
    for thread in threads:
        history = await client.threads.get_history(thread_id=thread["thread_id"])
        results.append(history)
    return str(results)
```

You can scope thread search by user or organization by adjusting the metadata filter:

```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
# Search conversations for a specific user
threads = await client.threads.search(
    metadata={"user_id": user_id},
    limit=5,
)

# Search conversations across an organization
threads = await client.threads.search(
    metadata={"org_id": org_id},
    limit=5,
)
```

This is useful for agents that perform complex, multi-step tasks. For example, a coding agent can look back at a past debugging session and skip straight to the likely root cause.

### Organization-level memory

Organization-level memory follows the same pattern as user-scoped memory, but with an organization-wide namespace instead of a per-user one. Use it for policies or knowledge that should apply across all users and agents in an organization.

Organization memory is typically **read-only** to prevent prompt injection via shared state. See [read-only vs writable memory](#read-only-vs-writable-memory) for details.

```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from deepagents.backends import CompositeBackend, StateBackend, StoreBackend

agent = create_deep_agent(
    model="google_genai:gemini-3.6-flash",
    memory=[
        "/memories/preferences.md",
        "/policies/compliance.md",
    ],
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
)
```

Populate organization memory from your application code:

```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from langgraph_sdk import get_client
from deepagents.backends.utils import create_file_data

client = get_client(url="<DEPLOYMENT_URL>")

await client.store.put_item(
    (org_id,),
    "/compliance.md",
    create_file_data("""## Compliance policies
- Never disclose internal pricing
- Always include disclaimers on financial advice
"""),
)
```

Use [permissions](../Execution%20environment/Permissions.md) to enforce that org-level memory is read-only, or [policy hooks](../Execution%20environment/Backends.md#add-policy-hooks) for custom validation logic.

### Background consolidation

By default, the agent writes memories during the conversation (hot path). An alternative is to process memories **between conversations** as a background task, sometimes called **sleep time compute**. A separate deep agent reviews recent conversations, extracts key facts, and merges them with existing memories.

| Approach | Pros | Cons |
| - | - | - |
| **Hot path** (during conversation) | Memories available immediately, transparent to user | Adds latency, agent must multitask |
| **Background** (between conversations) | No user-facing latency, can synthesize across multiple conversations | Memories not available until next conversation, requires a second agent |

For most applications, the hot path is sufficient. Add background consolidation when you need to reduce latency or improve memory quality across many conversations.

The recommended pattern is to deploy a **consolidation agent** alongside your main agent — a deep agent that reads recent conversation history, extracts key facts, and merges them into the memory store — and trigger it on a [cron schedule](#cron). Pick a cadence that reflects how often your users actually interact with the agent: a chat product with steady daily traffic might consolidate every few hours, while a tool used a handful of times per week only needs to run nightly or weekly. Consolidating much more often than users converse just burns tokens on no-op runs.

#### Consolidation agent

The consolidation agent reads recent conversation history and merges key facts into the memory store. Register it alongside your main agent in `langgraph.json`:

```python consolidation_agent.py theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from datetime import datetime, timedelta, timezone

from deepagents import create_deep_agent
from langchain.tools import tool, ToolRuntime
from langgraph_sdk import get_client

sdk_client = get_client(url="<DEPLOYMENT_URL>")


@tool
async def search_recent_conversations(query: str, runtime: ToolRuntime) -> str:
    """Search this user's conversations updated in the last 6 hours."""
    user_id = runtime.server_info.user.identity  # [!code highlight]

    since = datetime.now(timezone.utc) - timedelta(hours=6)
    threads = await sdk_client.threads.search(
        metadata={"user_id": user_id},
        updated_after=since.isoformat(),
        limit=20,
    )
    conversations = []
    for thread in threads:
        history = await sdk_client.threads.get_history(
            thread_id=thread["thread_id"]
        )
        conversations.append(history["values"]["messages"])
    return str(conversations)


agent = create_deep_agent(
    model="google_genai:gemini-3.6-flash",
    system_prompt="""Review recent conversations and update the user's memory file.
Merge new facts, remove outdated information, and keep it concise.""",
    tools=[search_recent_conversations],
)
```

```json langgraph.json theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
{
  "dependencies": ["."],
  "graphs": {
    "agent": "./agent.py:agent",
    "consolidation_agent": "./consolidation_agent.py:agent"
  },
  "env": ".env"
}
```

#### Cron

A [cron job](https://docs.langchain.com/langsmith/cron-jobs.md) runs the consolidation agent on a fixed schedule. The agent searches recent conversations and synthesizes them into memory. Match the schedule to your usage patterns so consolidation runs roughly track real activity.

```mermaid theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
graph LR
    Store[(Memory store)] -.->|reads| Conv1[Conversation 1]
    Store -.->|reads| Conv2[Conversation 2]
    Cron[Cron schedule] -->|periodic| Agent[Consolidation agent]
    Agent -->|writes| Store

    classDef trigger fill:#F6FFDB,stroke:#6E8900,stroke-width:2px,color:#2E3900
    classDef process fill:#E5F4FF,stroke:#006DDD,stroke-width:2px,color:#030710
    classDef output fill:#EBD0F0,stroke:#885270,stroke-width:2px,color:#441E33
    classDef schedule fill:#FDF3FF,stroke:#7E65AE,stroke-width:2px,color:#504B5F

    class Conv1,Conv2 trigger
    class Agent process
    class Store output
    class Cron schedule
```

Schedule the consolidation agent with a cron job:

```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from langgraph_sdk import get_client

client = get_client(url="<DEPLOYMENT_URL>")

cron_job = await client.crons.create(
    assistant_id="consolidation_agent",
    schedule="0 */6 * * *",
    input={"messages": [{"role": "user", "content": "Consolidate recent memories."}]},
)
```

> [!NOTE]
>
> All cron schedules are interpreted in **UTC**. See [cron jobs](https://docs.langchain.com/langsmith/cron-jobs.md) for details on managing and deleting cron jobs.

> [!WARNING]
>
> The cron interval must match the lookback window inside the consolidation agent. The example above runs every 6 hours (`0 */6 * * *`) and the agent's `search_recent_conversations` tool looks back `timedelta(hours=6)` — keep these in sync. If the cron runs more often than the lookback, you'll reprocess the same conversations; if it runs less often, you'll drop memories that fall outside the window.

For more on deploying agents with background processes, see [going to production](../Deployment/Going%20to%20production/index.md).

### Read-only vs writable memory

By default, the agent can both read and write memory files. For shared state like organization policies or compliance rules, you may want to make memory **read-only** so the agent can reference it but not modify it. This prevents prompt injection via shared memory and ensures that only your application code controls what's in the file.

| Permission | Use case | How it works |
| - | - | - |
| **Read-write** (default) | User preferences, agent self-improvement, learned [skills](Skills.md) | Agent updates files via `edit_file` tool |
| **Read-only** | Organization policies, compliance rules, shared knowledge bases, developer-defined [skills](Skills.md) | Populate via application code or the [Store API](https://docs.langchain.com/langsmith/custom-store.md). Use [permissions](../Execution%20environment/Permissions.md) to deny writes to specific paths, or [policy hooks](../Execution%20environment/Backends.md#add-policy-hooks) for custom validation logic. |

**Security considerations:** If one user can write to memory that another user reads, a malicious user could inject instructions into shared state. To mitigate this:

* **Default to user scope** `(user_id)` unless you have a specific reason to share
* Use **read-only memory** for shared policies (populate via application code, not the agent)
* Add **human-in-the-loop** validation before the agent writes to shared memory. Use an [interrupt](https://docs.langchain.com/oss/python/langgraph/interrupts.md) to require human approval for writes to sensitive paths.

To enforce read-only memory, use [permissions](../Execution%20environment/Permissions.md) to declaratively deny writes to specific paths. For custom validation logic (rate limiting, audit logging, content inspection), use [backend policy hooks](../Execution%20environment/Backends.md#add-policy-hooks).

### Concurrent writes

Multiple threads can write to memory in parallel, but concurrent writes to the **same file** can cause last-write-wins conflicts. For user-scoped memory this is rare since users typically have one active conversation at a time. For agent-scoped or organization-scoped memory, consider using [background consolidation](#background-consolidation) to serialize writes, or structure memory as separate files per topic to reduce contention.

In practice, if a write fails due to a conflict, the LLM is usually smart enough to retry or recover gracefully, so a single lost write is not catastrophic.

### Multiple agents in the same deployment

To give each agent its own memory in a shared deployment, add `assistant_id` to the namespace:

```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
StoreBackend(
    namespace=lambda rt: (
        rt.server_info.assistant_id,  # [!code highlight]
        rt.server_info.user.identity,
    ),
)
```

Use `assistant_id` alone if you only need per-agent isolation without per-user scoping.

> [!TIP]
>
> Use [LangSmith tracing](https://docs.langchain.com/langsmith/trace-with-langgraph.md) to audit what your agent writes to memory. Every file write appears as a tool call in the trace.

## See also

* [OpenWiki](OpenWiki.md): Generate and maintain repository wikis that coding agents find through `AGENTS.md`
* [Backends](../Execution%20environment/Backends.md): Choose where memory files are stored
* [Context engineering](Context%20engineering%20in%20Deep%20Agents.md): Short-term memory, offloading, and summarization
* [Skills](Skills.md): On-demand procedural memory

***

[Connect these docs](https://docs.langchain.com/use-these-docs.md) to your agent of choice via MCP for real-time answers.

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/deepagents/memory.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).

# Subagents

In the **subagents** architecture, a central main [agent](../../Core%20components/Agents.md) (often referred to as a **supervisor**) coordinates subagents by calling them as [tools](../../Core%20components/Tools.md). The main agent decides which subagent to invoke, what input to provide, and how to combine results. By default, subagents are stateless—they don't remember past interactions, with all conversation memory maintained by the main agent. This provides [context](../Context%20engineering%20in%20agents.md) isolation: each subagent invocation works in a clean context window, preventing context bloat in the main conversation.

You can also pass the main agent's conversation history into a subagent when it needs that context. See [Subagent inputs](#subagent-inputs).

For built-in subagent support, see [Deep Agents](https://docs.langchain.com/oss/python/deepagents/subagents.md).

```mermaid
graph LR
    A[User] --> B[Main Agent]
    B --> C[Subagent A]
    B --> D[Subagent B]
    B --> E[Subagent C]
    C --> B
    D --> B
    E --> B
    B --> F[User response]

    classDef trigger fill:#F6FFDB,stroke:#6E8900,stroke-width:2px,color:#2E3900
    classDef process fill:#E5F4FF,stroke:#006DDD,stroke-width:2px,color:#030710

    class A,F trigger
    class B,C,D,E process
```

## Key characteristics

* Centralized control: All routing passes through the main agent
* No direct user interaction: Subagents return results to the main agent, not the user (though you can use [interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts.md#pause-using-interrupt) within a subagent to allow user interaction)
* Subagents via tools: Subagents are invoked via tools
* Parallel execution: The main agent can invoke multiple subagents in a single turn

> [!NOTE]
>
> **Supervisor vs. Router**: A supervisor agent (this pattern) is different from a [router](Router.md). The supervisor is a full agent that maintains conversation context and dynamically decides which subagents to call across multiple turns. A router is typically a single classification step that dispatches to agents without maintaining ongoing conversation state.

## When to use

Use the subagents pattern when you have multiple distinct domains (e.g., calendar, email, CRM, database), subagents don't need to converse directly with users, or you want centralized workflow control. For simpler cases with just a few [tools](../../Core%20components/Tools.md), use a [single agent](../../Core%20components/Agents.md).

> [!TIP]
>
> **Need user interaction within a subagent?** While subagents typically return results to the main agent rather than conversing directly with users, you can use [interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts.md#pause-using-interrupt) within a subagent to pause execution and gather user input. This is useful when a subagent needs clarification or approval before proceeding. The main agent remains the orchestrator, but the subagent can collect information from the user mid-task.

## Basic implementation

The core mechanism wraps a subagent as a tool that the main agent can call:

```python
from langchain.tools import tool
from langchain.agents import create_agent

# Create a subagent
subagent = create_agent(model="google_genai:gemini-4-hydrogen", tools=[...])

# Wrap it as a tool
@tool("research", description="Research a topic and return findings")
def call_research_agent(query: str):
    result = subagent.invoke({"messages": [{"role": "user", "content": query}]})
    return result["messages"][-1].content

# Main agent with subagent as a tool
main_agent = create_agent(model="google_genai:gemini-4-hydrogen", tools=[call_research_agent])
```

> [card] [Tutorial: Build a personal assistant with subagents](../../Learn/Tutorials/Multi-agent/Build%20a%20personal%20assistant%20with%20subagents.md)
>
> Learn how to build a personal assistant using the subagents pattern, where a central main agent (supervisor) coordinates specialized worker agents.

## Design decisions

When implementing the subagents pattern, you'll make several key design choices. This table summarizes the options—each is covered in detail in the sections below.

| Decision | Options |
| - | - |
| [**Sync vs. async**](#sync-vs-async) | Sync (blocking) vs. async (background) |
| [**Tool patterns**](#tool-patterns) | Tool per agent vs. single dispatch tool |
| [**Subagent specs**](#subagent-specs) | System prompt vs. enum constraint vs. tool-based discovery (single dispatch tool only) |
| [**Subagent inputs**](#subagent-inputs) | Query only vs. full context |
| [**Subagent outputs**](#subagent-outputs) | Subagent result vs full conversation history |

## Sync vs. async

Subagent execution can be **synchronous** (blocking) or **asynchronous** (background). Your choice depends on whether the main agent needs the result to continue.

| Mode | Main agent behavior | Best for | Tradeoff |
| - | - | - | - |
| **Sync** | Waits for subagent to complete | Main agent needs result to continue | Simple, but blocks the conversation |
| **Async** | Continues while subagent runs in background | Independent tasks, user shouldn't wait | Responsive, but more complex |

> [!TIP]
>
> Not to be confused with Python's `async`/`await`. Here, "async" means the main agent kicks off a background job (typically in a separate process or service) and continues without blocking.

### Synchronous (default)

By default, subagent calls are **synchronous**: the main agent waits for each subagent to complete before continuing. Use sync when the main agent's next action depends on the subagent's result.

```mermaid
sequenceDiagram
    participant User
    participant Main Agent
    participant Research Subagent

    User->>Main Agent: "What's the weather in Tokyo?"
    Main Agent->>Research Subagent: research("Tokyo weather")
    Note over Main Agent: Waiting for result...
    Research Subagent-->>Main Agent: "Currently 72°F, sunny"
    Main Agent-->>User: "It's 72°F and sunny in Tokyo"
```

**When to use sync:**

* Main agent needs the subagent's result to formulate its response
* Tasks have order dependencies (e.g., fetch data → analyze → respond)
* Subagent failures should block the main agent's response

**Tradeoffs:**

* Simple implementation—just call and wait
* User sees no response until all subagents complete
* Long-running tasks freeze the conversation

### Asynchronous

Use **asynchronous execution** when the subagent's work is independent—the main agent doesn't need the result to continue conversing with the user. The main agent kicks off a background job and remains responsive.

```mermaid
sequenceDiagram
    participant User
    participant Main Agent
    participant Job System
    participant Contract Reviewer

    User->>Main Agent: "Review this M&A contract"
    Main Agent->>Job System: run_agent("legal_reviewer", task)
    Job System->>Contract Reviewer: Start agent
    Job System-->>Main Agent: job_id: "job_123"
    Main Agent-->>User: "Started review (job_123)"

    Note over Contract Reviewer: Reviewing 150+ pages...

    User->>Main Agent: "What's the status?"
    Main Agent->>Job System: check_status(job_id)
    Job System-->>Main Agent: "running"
    Main Agent-->>User: "Still reviewing contract..."

    Note over Contract Reviewer: Review completes

    User->>Main Agent: "Is it done yet?"
    Main Agent->>Job System: check_status(job_id)
    Job System-->>Main Agent: "completed"
    Main Agent->>Job System: get_result(job_id)
    Job System-->>Main Agent: Contract analysis
    Main Agent-->>User: "Review complete: [findings]"
```

**When to use async:**

* Subagent work is independent of the main conversation flow
* Users should be able to continue chatting while work happens
* You want to run multiple independent tasks in parallel

**Three-tool pattern:**

1. **Start job**: Kicks off the background task, returns a job ID
2. **Check status**: Returns current state (pending, running, completed, failed)
3. **Get result**: Retrieves the completed result

**Handling job completion:** When a job finishes, your application needs to notify the user. One approach: surface a notification that, when clicked, sends a `HumanMessage` like "Check job\_123 and summarize the results."

## Tool patterns

There are two main ways to expose subagents as tools:

| Pattern | Best for | Trade-off |
| - | - | - |
| [**Tool per agent**](#tool-per-agent) | Fine-grained control over each subagent's input/output | More setup, but more customization |
| [**Single dispatch tool**](#single-dispatch-tool) | Many agents, distributed teams, convention over configuration | Simpler composition, less per-agent customization |

### Tool per agent

```mermaid
graph LR
    A[User] --> B[Main Agent]
    B --> C[Subagent A]
    B --> D[Subagent B]
    B --> E[Subagent C]
    C --> B
    D --> B
    E --> B
    B --> F[User response]

    classDef trigger fill:#F6FFDB,stroke:#6E8900,stroke-width:2px,color:#2E3900
    classDef process fill:#E5F4FF,stroke:#006DDD,stroke-width:2px,color:#030710

    class A,F trigger
    class B,C,D,E process
```

The key idea is wrapping subagents as tools that the main agent can call:

```python
from langchain.tools import tool
from langchain.agents import create_agent

# Create a sub-agent
subagent = create_agent(model="...", tools=[...])  # [!code highlight]

# Wrap it as a tool  # [!code highlight]
@tool("subagent_name", description="subagent_description")  # [!code highlight]
def call_subagent(query: str):  # [!code highlight]
    result = subagent.invoke({"messages": [{"role": "user", "content": query}]})
    return result["messages"][-1].content

# Main agent with subagent as a tool  # [!code highlight]
main_agent = create_agent(model="...", tools=[call_subagent])  # [!code highlight]
```

The main agent invokes the subagent tool when it decides the task matches the subagent's description, receives the result, and continues orchestration. See [Context engineering](#context-engineering) for fine-grained control.

### Single dispatch tool

An alternative approach uses a single parameterized tool to invoke ephemeral sub-agents for independent tasks. Unlike the [tool per agent](#tool-per-agent) approach where each sub-agent is wrapped as a separate tool, this uses a convention-based approach with a single `task` tool: the task description is passed as a human message to the sub-agent, and the sub-agent's final message is returned as the tool result.

Use this approach when you want to distribute agent development across multiple teams, need to isolate complex tasks into separate context windows, need a scalable way to add new agents without modifying the coordinator, or prefer convention over customization. This approach trades flexibility in context engineering for simplicity in agent composition and strong context isolation.

```mermaid
graph LR
    A[User] --> B[Main Agent]
    B --> C{task<br/>agent_name, description}
    C -->|research| D[Research Agent]
    C -->|writer| E[Writer Agent]
    C -->|reviewer| F[Reviewer Agent]
    D --> C
    E --> C
    F --> C
    C --> B
    B --> G[User response]

    classDef trigger fill:#F6FFDB,stroke:#6E8900,stroke-width:2px,color:#2E3900
    classDef process fill:#E5F4FF,stroke:#006DDD,stroke-width:2px,color:#030710
    classDef decision fill:#FDF3FF,stroke:#7E65AE,stroke-width:2px,color:#504B5F

    class A,G trigger
    class B,D,E,F process
    class C decision
```

**Key characteristics:**

* Single task tool: One parameterized tool that can invoke any registered sub-agent by name
* Convention-based invocation: Agent selected by name, task passed as human message, final message returned as tool result
* Team distribution: Different teams can develop and deploy agents independently
* Agent discovery: Sub-agents can be discovered via system prompt (listing available agents) or through [progressive disclosure](../../Learn/Tutorials/Multi-agent/Build%20a%20SQL%20assistant%20with%20on-demand%20skills.md) (loading agent information on-demand via tools)

> [!TIP]
>
> An interesting aspect of this approach is that sub-agents may have the exact same capabilities as the main agent. In such cases, invoking a sub-agent is **really about context isolation** as the primary reason—allowing complex, multi-step tasks to run in isolated context windows without bloating the main agent's conversation history. The sub-agent completes its work autonomously and returns only a concise summary, keeping the main thread focused and efficient.

> [accordion] Agent registry with task dispatcher
>
> ```python
> from langchain.tools import tool
> from langchain.agents import create_agent
>
> # Sub-agents developed by different teams
> research_agent = create_agent(
>     model="gpt-6.1-sol",
>     system_prompt="You are a research specialist..."
> )
>
> writer_agent = create_agent(
>     model="gpt-6.1-sol",
>     system_prompt="You are a writing specialist..."
> )
>
> # Registry of available sub-agents
> SUBAGENTS = {
>     "research": research_agent,
>     "writer": writer_agent,
> }
>
> @tool
> def task(
>     agent_name: str,
>     description: str
> ) -> str:
>     """Launch an ephemeral subagent for a task.
>
>     Available agents:
>     - research: Research and fact-finding
>     - writer: Content creation and editing
>     """
>     agent = SUBAGENTS[agent_name]
>     result = agent.invoke({
>         "messages": [
>             {"role": "user", "content": description}
>         ]
>     })
>     return result["messages"][-1].content
>
> # Main coordinator agent
> main_agent = create_agent(
>     model="gpt-6.1-sol",
>     tools=[task],
>     system_prompt=(
>         "You coordinate specialized sub-agents. "
>         "Available: research (fact-finding), "
>         "writer (content creation). "
>         "Use the task tool to delegate work."
>     ),
> )
> ```

## Context engineering

Control how context flows between the main agent and its subagents:

| Category | Purpose | Impacts |
| - | - | - |
| [**Subagent specs**](#subagent-specs) | Ensure subagents are invoked when they should be | Main agent routing decisions |
| [**Subagent inputs**](#subagent-inputs) | Ensure subagents can execute well with optimized context | Subagent performance |
| [**Subagent outputs**](#subagent-outputs) | Ensure the supervisor can act on subagent results | Main agent performance |

See also our comprehensive guide on [context engineering](../Context%20engineering%20in%20agents.md) for agents.

### Subagent specs

The **names** and **descriptions** associated with subagents are the primary way the main agent knows which subagents to invoke. These are prompting levers—choose them carefully.

* **Name**: How the main agent refers to the sub-agent. Keep it clear and action-oriented (e.g., `research_agent`, `code_reviewer`).
* **Description**: What the main agent knows about the sub-agent's capabilities. Be specific about what tasks it handles and when to use it.

For the [single dispatch tool](#single-dispatch-tool) design, you must additionally provide the main agent with information about the subagents it can invoke.
You can provide this information in different ways based on the number of agents and whether your registry is static or dynamic:

| Method | Best for | Tradeoff |
| - | - | - |
| **System prompt enumeration** | Small, static agent lists (\< 10 agents) | Simple, but requires prompt updates when agents change |
| **Enum constraint** | Small, static agent lists (\< 10 agents) | Type-safe and explicit, but requires code changes when agents change |
| **Tool-based discovery** | Large or dynamic agent registries | Flexible and scalable, but adds complexity |

#### System prompt enumeration

List available agents directly in the main agent's system prompt. The main agent sees the list of agents and their descriptions as part of its instructions.

**When to use:**

* You have a small, fixed set of agents (\< 10)
* Agent registry rarely changes
* You want the simplest implementation

**Example:**

```python
main_agent = create_agent(
    model="...",
    tools=[task],
    system_prompt=(
        "You coordinate specialized sub-agents. "
        "Available agents:\n"
        "- research: Research and fact-finding\n"
        "- writer: Content creation and editing\n"
        "- reviewer: Code and document review\n"
        "Use the task tool to delegate work."
    ),
)
```

#### Enum constraint on dispatch tool

Add an enum constraint to the `agent_name` parameter in your dispatch tool. This provides type safety and makes available agents explicit in the tool schema.

**When to use:**

* You have a small, fixed set of agents (\< 10)
* You want type safety and explicit agent names
* You prefer schema-based validation over prompt-based guidance

**Example:**

```python
from enum import Enum

class AgentName(str, Enum):
    RESEARCH = "research"
    WRITER = "writer"
    REVIEWER = "reviewer"

@tool
def task(
    agent_name: AgentName,  # Enum constraint
    description: str
) -> str:
    """Launch an ephemeral subagent for a task."""
    # ...
```

#### Tool-based discovery

Provide a separate tool (e.g., `list_agents` or `search_agents`) that the main agent can call to discover available agents on-demand. This enables progressive disclosure and supports dynamic registries.

**When to use:**

* You have many agents (> 10) or a growing registry
* Agent registry changes frequently or is dynamic
* You want to reduce prompt size and token usage
* Different teams manage different agents independently

**Example:**

```python
@tool
def list_agents(query: str = "") -> str:
    """List available subagents, optionally filtered by query."""
    agents = search_agent_registry(query)
    return format_agent_list(agents)

@tool
def task(agent_name: str, description: str) -> str:
    """Launch an ephemeral subagent for a task."""
    # ...

main_agent = create_agent(
    model="...",
    tools=[task, list_agents],
    system_prompt="Use list_agents to discover available subagents, then use task to invoke them."
)
```

### Subagent inputs

Customize what context the subagent receives to execute its task. Add input that isn't practical to capture in a static prompt—full message history, prior results, or task metadata—by pulling from the agent's state.

```python Subagent inputs example expandable
from langchain.agents import AgentState
from langchain.tools import tool, ToolRuntime

class CustomState(AgentState):
    example_state_key: str

@tool(
    "subagent1_name",
    description="subagent1_description"
)
def call_subagent1(query: str, runtime: ToolRuntime[None, CustomState]):
    # Apply any logic needed to transform the messages into a suitable input
    subagent_input = some_logic(query, runtime.state["messages"])
    result = subagent1.invoke({
        "messages": subagent_input,
        # You could also pass other state keys here as needed.
        # Make sure to define these in both the main and subagent's
        # state schemas.
        "example_state_key": runtime.state["example_state_key"]
    })
    return result["messages"][-1].content
```

`some_logic` controls how much context the subagent receives. Passing only the task description (`query`) keeps the subagent isolated. Passing the parent's message history (`runtime.state["messages"]`) instead seeds the subagent with prior work, which helps when it needs to continue something the parent already started, like resuming a PR review or picking up a bug fix.

[Deep Agents](https://docs.langchain.com/oss/python/deepagents/subagents.md#forked-subagents) names these patterns `mode: "isolated"` (default) and `mode: "fork"`, and implements forking for you: a forked subagent receives the parent's full message history (including tool calls) and system prompt.

| Mode | Subagent receives | Best for | Tradeoff |
| - | - | - | - |
| **Isolated** (default) | Only the task description | Focused work that needs little prior context | Context isolation, but re-derives everything the parent already did |
| **Forked** | The parent's conversation history (and, in Deep Agents, the system prompt) | Continuing a task the parent already started | Seeded with prior context, at the cost of a larger prompt and less isolation |

### Subagent outputs

Customize what the main agent receives back so it can make good decisions. Two strategies:

1. **Prompt the sub-agent**: Specify exactly what should be returned. A common failure mode is that the sub-agent performs tool calls or reasoning but doesn't include results in its final message—remind it that the supervisor only sees the final output.
2. **Format in code**: Adjust or enrich the response before returning it. For example, pass specific state keys back in addition to the final text using a [`Command`](https://docs.langchain.com/oss/python/langgraph/graph-api#command).

```python Subagent outputs example expandable
from typing import Annotated
from langchain.agents import AgentState
from langchain.tools import InjectedToolCallId
from langgraph.types import Command


@tool(
    "subagent1_name",
    description="subagent1_description"
)
def call_subagent1(
    query: str,
    tool_call_id: Annotated[str, InjectedToolCallId],
) -> Command:
    result = subagent1.invoke({
        "messages": [{"role": "user", "content": query}]
    })
    return Command(update={
        # Pass back additional state from the subagent
        "example_state_key": result["example_state_key"],
        "messages": [
            ToolMessage(
                content=result["messages"][-1].content,
                tool_call_id=tool_call_id
            )
        ]
    })
```

## Checkpointing and state inspection

By default, subagents use the **inherited checkpointer** mode—each invocation starts with fresh state, supports [interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts.md#pause-using-interrupt), and runs safely in parallel. If you need a subagent to maintain its own persistent conversation history across invocations, compile it with `checkpointer=True` (continuations mode). See [subgraph persistence](https://docs.langchain.com/oss/python/langgraph/use-subgraphs.md#subgraph-persistence) for a full comparison of modes.

Because subagents are called inside tool functions, LangGraph cannot [statically discover](https://docs.langchain.com/oss/python/langgraph/use-subgraphs.md#view-subgraph-state) them. This means [`get_state` with `subgraphs`](https://docs.langchain.com/oss/python/langgraph/use-subgraphs#view-subgraph-state) will not return subagent state. If you need to read nested graph state (e.g., during an [interrupt](https://docs.langchain.com/oss/python/langgraph/interrupts.md#pause-using-interrupt)), invoke the subagent from a [node function](https://docs.langchain.com/oss/python/langgraph/use-subgraphs.md#call-a-subgraph-inside-a-node) in a custom graph instead. See [subgraph persistence](https://docs.langchain.com/oss/python/langgraph/use-subgraphs.md#subgraph-persistence) for details on how each mode affects state visibility.

> [card] [Migrate from langgraph-supervisor](https://docs.langchain.com/oss/python/migrate/langgraph-supervisor.md)
>
> The langgraph-supervisor package is no longer actively maintained. Learn how to migrate from create\_supervisor to the subagents pattern, including interrupt and resume flows with external API callbacks.

***

[Connect these docs](https://docs.langchain.com/use-these-docs.md) to your agent of choice via MCP for real-time answers.

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/langchain/multi-agent/subagents.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).

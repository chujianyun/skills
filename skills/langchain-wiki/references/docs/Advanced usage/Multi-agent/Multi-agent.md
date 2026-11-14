# Multi-agent

Multi-agent systems coordinate specialized components to tackle complex workflows. However, not every complex task requires this approach—a single agent with the right (sometimes dynamic) tools and prompt can often achieve similar results.

> [!TIP]
>
> For built-in multi-agent support, use [Managed Deep Agents](https://docs.langchain.com/langsmith/python/managed-deep-agents-overview.md): a managed higher-level harness built on LangChain that ships with [subagents](https://docs.langchain.com/oss/python/deepagents/subagents.md), [skills](https://docs.langchain.com/oss/python/deepagents/skills.md), planning, a virtual filesystem, and context management. Alternatively, for maximum flexibility while using the same Deep Agents harness, use [Deep Agents](https://docs.langchain.com/oss/python/deepagents/overview.md) and host agents yourself, or run a custom [Agent Server](https://docs.langchain.com/langsmith/deployment.md).

## Why multi-agent?

When developers say they need "multi-agent," they're usually looking for one or more of these capabilities:

* &#x20;**Context management**: Provide specialized knowledge without overwhelming the model's context window. If context were infinite and latency zero, you could dump all knowledge into a single prompt—but since it's not, you need patterns to selectively surface relevant information.
* &#x20;**Distributed development**: Allow different teams to develop and maintain capabilities independently, composing them into a larger system with clear boundaries.
* &#x20;**Parallelization**: Spawn specialized workers for subtasks and execute them concurrently for faster results.

Multi-agent patterns are particularly valuable when a single agent has too many [tools](../../Core%20components/Tools.md) and makes poor decisions about which to use, when tasks require specialized knowledge with extensive context (long prompts and domain-specific tools), or when you need to enforce sequential constraints that unlock capabilities only after certain conditions are met.

> [!TIP]
>
> At the center of multi-agent design is **[context engineering](../Context%20engineering%20in%20agents.md)**—deciding what information each agent sees. The quality of your system depends on ensuring each agent has access to the right data for its task.

## Patterns

Here are the main patterns for building multi-agent systems, each suited to different use cases:

| Pattern | How it works |
| - | - |
| [**Subagents**](Subagents.md) | A main agent coordinates subagents as tools. All routing passes through the main agent, which decides when and how to invoke each subagent. |
| [**Handoffs**](Handoffs.md) | Behavior changes dynamically based on state. Tool calls update a state variable that triggers routing or configuration changes, switching agents or adjusting the current agent's tools and prompt. |
| [**Skills**](Skills.md) | Specialized prompts and knowledge loaded on-demand. A single agent stays in control while loading context from skills as needed. |
| [**Router**](Router.md) | A routing step classifies input and directs it to one or more specialized agents. Results are synthesized into a combined response. |
| [**Custom workflow**](Custom%20workflow.md) | Build bespoke execution flows with [LangGraph](https://docs.langchain.com/oss/python/langgraph/overview.md), mixing deterministic logic and agentic behavior. Embed other patterns as nodes in your workflow. |

### Choosing a pattern

Use this table to match your requirements to the right pattern:

| Pattern | Distributed development | Parallelization | Multi-hop | Direct user interaction |
| - | :-: | :-: | :-: | :-: |
| [**Subagents**](Subagents.md) | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐ |
| [**Handoffs**](Handoffs.md) | - | - | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| [**Skills**](Skills.md) | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| [**Router**](Router.md) | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | - | ⭐⭐⭐ |

* **Distributed development**: Can different teams maintain components independently?
* **Parallelization**: Can multiple agents execute concurrently?
* **Multi-hop**: Does the pattern support calling multiple subagents in series?
* **Direct user interaction**: Can subagents converse directly with the user?

> [!TIP]
>
> You can mix patterns! For example, a **subagents** architecture can invoke tools that invoke custom workflows or router agents. Subagents can even use the **skills** pattern to load context on-demand. The possibilities are endless!

### Visual overview

> [tab] Subagents
>
> A main agent coordinates subagents as tools. All routing passes through the main agent.
>
> ![Subagents pattern: main agent coordinates subagents as tools](../../../assets/pattern-subagents-2adcd61ea2c7.png)

> [tab] Handoffs
>
> Agents transfer control to each other via tool calls. Each agent can hand off to others or respond directly to the user.
>
> ![Handoffs pattern: agents transfer control via tool calls](../../../assets/pattern-handoffs-221a4b9ea3bc.png)

> [tab] Skills
>
> A single agent loads specialized prompts and knowledge on-demand while staying in control.
>
> ![Skills pattern: single agent loads specialized context on-demand](../../../assets/pattern-skills-d0adc379d258.png)

> [tab] Router
>
> A routing step classifies input and directs it to specialized agents. Results are synthesized.
>
> ![Router pattern: routing step classifies input to specialized agents](../../../assets/pattern-router-e75d275fdd4c.png)

> [!TIP]
>
> Trace the full coordination flow across agents with [LangSmith](https://smith.langchain.com?utm_source=docs\&utm_medium=cta\&utm_campaign=langsmith-signup\&utm_content=oss-langchain-multi-agent-index). Follow the [tracing quickstart](https://docs.langchain.com/langsmith/trace-with-langchain.md) to get set up.
>
> We recommend you also set up [LangSmith Engine](https://docs.langchain.com/langsmith/engine.md) which monitors your traces, detects issues, and proposes fixes.

## Performance comparison

Different patterns have different performance characteristics. Understanding these tradeoffs helps you choose the right pattern for your latency and cost requirements.

**Key metrics:**

* **Model calls**: Number of LLM invocations. More calls = higher latency (especially if sequential) and higher per-request API costs.
* **Tokens processed**: Total [context window](../Context%20engineering%20in%20agents.md) usage across all calls. More tokens = higher processing costs and potential context limits.

### One-shot request

> **User:** "Buy coffee"

A specialized coffee agent/skill can call a `buy_coffee` tool.

| Pattern | Model calls | Best fit |
| - | :-: | :-: |
| [**Subagents**](Subagents.md) | 4 | |
| [**Handoffs**](Handoffs.md) | 3 | ✅ |
| [**Skills**](Skills.md) | 3 | ✅ |
| [**Router**](Router.md) | 3 | ✅ |

> [tab] Subagents
>
> **4 model calls:**
>
> ![Subagents one-shot: 4 model calls for buy coffee request](../../../assets/oneshot-subagents-c6ec4ce537ef.png)

> [tab] Handoffs
>
> **3 model calls:**
>
> ![Handoffs one-shot: 3 model calls for buy coffee request](../../../assets/oneshot-handoffs-2581e29e2883.png)

> [tab] Skills
>
> **3 model calls:**
>
> ![Skills one-shot: 3 model calls for buy coffee request](../../../assets/oneshot-skills-51a3b1492034.png)

> [tab] Router
>
> **3 model calls:**
>
> ![Router one-shot: 3 model calls for buy coffee request](../../../assets/oneshot-router-615e2bf7435e.png)

**Key insight:** Handoffs, Skills, and Router are most efficient for single tasks (3 calls each). Subagents adds one extra call because results flow back through the main agent—this overhead provides centralized control.

### Repeat request

> **Turn 1:** "Buy coffee"
> **Turn 2:** "Buy coffee again"

The user repeats the same request in the same conversation.

| Pattern | Turn 2 calls | Total (both turns) | Best fit |
| - | :-: | :-: | :-: |
| [**Subagents**](Subagents.md) | 4 | 8 | |
| [**Handoffs**](Handoffs.md) | 2 | 5 | ✅ |
| [**Skills**](Skills.md) | 2 | 5 | ✅ |
| [**Router**](Router.md) | 3 | 6 | |

> [tab] Subagents
>
> **4 calls again → 8 total**
>
> * Subagents are **stateless by design**—each invocation follows the same flow
> * The main agent maintains conversation context, but subagents start fresh each time
> * This provides strong context isolation but repeats the full flow

> [tab] Handoffs
>
> **2 calls → 5 total**
>
> * The coffee agent is **still active** from turn 1 (state persists)
> * No handoff needed—agent directly calls `buy_coffee` tool (call 1)
> * Agent responds to user (call 2)
> * **Saves 1 call by skipping the handoff**

> [tab] Skills
>
> **2 calls → 5 total**
>
> * The skill context is **already loaded** in conversation history
> * No need to reload—agent directly calls `buy_coffee` tool (call 1)
> * Agent responds to user (call 2)
> * **Saves 1 call by reusing loaded skill**

> [tab] Router
>
> **3 calls again → 6 total**
>
> * Routers are **stateless**—each request requires an LLM routing call
> * Turn 2: Router LLM call (1) → Milk agent calls buy\_coffee (2) → Milk agent responds (3)
> * Can be optimized by wrapping as a tool in a stateful agent

**Key insight:** Stateful patterns (Handoffs, Skills) save 40-50% of calls on repeat requests. Subagents maintain consistent cost per request—this stateless design provides strong context isolation but at the cost of repeated model calls.

### Multi-domain

> **User:** "Compare Python, JavaScript, and Rust for web development"

Each language agent/skill contains \~2000 tokens of documentation. All patterns can make parallel tool calls.

| Pattern | Model calls | Total tokens | Best fit |
| - | :-: | :-: | :-: |
| [**Subagents**](Subagents.md) | 5 | \~9K | ✅ |
| [**Handoffs**](Handoffs.md) | 7+ | \~14K+ | |
| [**Skills**](Skills.md) | 3 | \~15K | |
| [**Router**](Router.md) | 5 | \~9K | ✅ |

> [tab] Subagents
>
> **5 calls, \~9K tokens**
>
> ![Subagents multi-domain: 5 calls with parallel execution](../../../assets/multidomain-subagents-d64bf2ea4b18.png)
>
> Each subagent works in **isolation** with only its relevant context. Total: **9K tokens**.

> [tab] Handoffs
>
> **7+ calls, \~14K+ tokens**
>
> ![Handoffs multi-domain: 7+ sequential calls](../../../assets/multidomain-handoffs-02676c9f383b.png)
>
> Handoffs executes **sequentially**—can't research all three languages in parallel. Growing conversation history adds overhead. Total: **\~14K+ tokens**.

> [tab] Skills
>
> **3 calls, \~15K tokens**
>
> ![Skills multi-domain: 3 calls with accumulated context](../../../assets/multidomain-skills-4b04e47fee41.png)
>
> After loading, **every subsequent call processes all 6K tokens of skill documentation**. Subagents processes 67% fewer tokens overall due to context isolation. Total: **15K tokens**.

> [tab] Router
>
> **5 calls, \~9K tokens**
>
> ![Router multi-domain: 5 calls with parallel execution](../../../assets/multidomain-router-ce6e0067384f.png)
>
> Router uses an **LLM for routing**, then invokes agents in parallel. Similar to Subagents but with explicit routing step. Total: **9K tokens**.

**Key insight:** For multi-domain tasks, patterns with parallel execution (Subagents, Router) are most efficient. Skills has fewer calls but high token usage due to context accumulation. Handoffs is inefficient here—it must execute sequentially and can't leverage parallel tool calling for consulting multiple domains simultaneously.

### Summary

Here's how patterns compare across all three scenarios:

| Pattern | One-shot | Repeat request | Multi-domain |
| - | :-: | :-: | :-: |
| [**Subagents**](Subagents.md) | 4 calls | 8 calls (4+4) | 5 calls, 9K tokens |
| [**Handoffs**](Handoffs.md) | 3 calls | 5 calls (3+2) | 7+ calls, 14K+ tokens |
| [**Skills**](Skills.md) | 3 calls | 5 calls (3+2) | 3 calls, 15K tokens |
| [**Router**](Router.md) | 3 calls | 6 calls (3+3) | 5 calls, 9K tokens |

**Choosing a pattern:**

| Optimize for | [Subagents](Subagents.md) | [Handoffs](Handoffs.md) | [Skills](Skills.md) | [Router](Router.md) |
| - | :-: | :-: | :-: | :-: |
| Single requests | | ✅ | ✅ | ✅ |
| Repeat requests | | ✅ | ✅ | |
| Parallel execution | ✅ | | | ✅ |
| Large-context domains | ✅ | | | ✅ |
| Simple, focused tasks | | | ✅ | |

***

[Connect these docs](https://docs.langchain.com/use-these-docs.md) to your agent of choice via MCP for real-time answers.

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/langchain/multi-agent/index.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).

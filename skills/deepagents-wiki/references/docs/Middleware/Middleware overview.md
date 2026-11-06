# Middleware overview

> Control and customize agent execution at every step

Middleware provides a way to more tightly control what happens inside the agent. Middleware is useful for the following:

* Tracking agent behavior with logging, analytics, and debugging.
* Transforming prompts, [tool selection](Prebuilt%20middleware.md#llm-tool-selector), and output formatting.
* Adding [retries](Prebuilt%20middleware.md#tool-retry), [fallbacks](Prebuilt%20middleware.md#model-fallback), and early termination logic.
* Applying [rate limits](Prebuilt%20middleware.md#model-call-limit), guardrails, and [PII detection](Prebuilt%20middleware.md#pii-detection).

Add middleware by passing them to [`create_agent`](https://reference.langchain.com/python/langchain/agents/factory/create_agent):

```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware, HumanInTheLoopMiddleware

agent = create_agent(
    model="gpt-5.5",
    tools=[...],
    middleware=[
        SummarizationMiddleware(...),
        HumanInTheLoopMiddleware(...)
    ],
)
```

## The agent loop

The core agent loop involves calling a model, letting it choose tools to execute, and then finishing when it calls no more tools:

![Core agent loop diagram](../../assets/images/core_agent_loop.png)

Middleware exposes hooks before and after each of those steps:

![Middleware flow diagram](../../assets/images/middleware_final.png)

## Use middleware inside a LangGraph workflow

Middleware is not a separate runtime: hooks run inside the compiled [LangGraph](https://docs.langchain.com/oss/python/langgraph/overview.md) that [`create_agent`](https://reference.langchain.com/python/langchain/agents/factory/create_agent) returns. You can drop the whole agent (middleware and all) into a larger [StateGraph](https://reference.langchain.com/python/langgraph/graph/state/StateGraph) as a node or subgraph, and every middleware hook continues to run.

Reach for this pattern when the surrounding topology is more than a standard "loop until done": classifying input before routing to one of several agents, fanning out work in parallel, or stitching agent calls together with deterministic steps.

`HumanInTheLoopMiddleware` matches against each tool's `.name`.

`@tool`-decorated functions take their name from the function, so the key below is `"send_email"`.

```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from langchain.agents import AgentState, create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langgraph.graph import START, StateGraph

# Assumes read_email, send_email, classify_node, and route are defined elsewhere.
email_agent = create_agent(
    model="claude-sonnet-4-6",
    tools=[read_email, send_email],
    middleware=[HumanInTheLoopMiddleware(interrupt_on={"send_email": True})],
)

graph = (
    StateGraph(AgentState)
    .add_node("classify", classify_node)
    .add_node("email_agent", email_agent)
    .add_edge(START, "classify")
    .add_conditional_edges("classify", route)
    .compile()
)
```

The HITL interrupt, summarization, PII redaction, retries, and any custom hooks all travel with the agent node. See [Use subgraphs](https://docs.langchain.com/oss/python/langgraph/use-subgraphs.md) for the full set of composition patterns, including subgraph checkpointer scoping (per-invocation versus per-thread).

## Additional resources

> [card] [Built-in middleware](Prebuilt%20middleware.md)
>
> Explore built-in middleware for common use cases.

> [card] [Custom middleware](Custom%20middleware.md)
>
> Build your own middleware with hooks and decorators.

> [card] [Middleware API reference](https://reference.langchain.com/python/langchain/middleware/)
>
> Complete API reference for middleware.

> [card] [Middleware integrations](https://docs.langchain.com/oss/python/integrations/middleware.md)
>
> Provider-specific middleware for Anthropic, AWS, OpenAI, and more.

> [card] [Testing agents](https://docs.langchain.com/oss/python/langchain/test.md)
>
> Test your agents with LangSmith.

***

[Connect these docs](https://docs.langchain.com/use-these-docs.md) to your agent of choice via MCP for real-time answers.

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/langchain/middleware/overview.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).

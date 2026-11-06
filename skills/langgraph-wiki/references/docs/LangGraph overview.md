# LangGraph overview

> Low-level orchestration framework and runtime for long-running, stateful agents

LangGraph is a low-level orchestration framework and runtime for long-running, stateful agents. You define workflows as graphs of shared state, nodes, and edges, and can mix deterministic steps with LLM-driven steps in the same graph.

LangGraph focuses on orchestration capabilities such as [durable execution](Capabilities/Persistence.md), [streaming](Capabilities/Streaming.md), and [human-in-the-loop](Capabilities/Interrupts.md). It does not prescribe prompts or agent architecture.

Before you start, learn the building blocks agents use, especially [models](https://docs.langchain.com/oss/python/langchain/models.md) and [tools](https://docs.langchain.com/oss/python/langchain/tools.md). Docs examples often use [LangChain](https://docs.langchain.com/oss/python/langchain/overview.md) for those integrations, but LangGraph does not require LangChain.

If you want a higher-level agent loop first, use [Deep Agents](https://docs.langchain.com/oss/python/deepagents/overview.md) or LangChain [agents](https://docs.langchain.com/oss/python/langchain/agents.md). Use LangGraph when you need explicit control over state and control flow.

**How LangChain products fit together**

* [Deep Agents](https://docs.langchain.com/oss/python/deepagents/overview.md) is an [agent harness](https://docs.langchain.com/oss/python/concepts/products.md#agent-harnesses-like-the-deep-agents-sdk): planning, subagents, filesystem tools, and context management on top of LangGraph.
* [LangChain](https://docs.langchain.com/oss/python/langchain/overview.md) is the agent framework: abstractions and integrations for models, tools, and agent loops.
* [LangGraph](LangGraph%20overview.md) is the orchestration runtime: durable execution, streaming, human-in-the-loop, and persistence.
* [LangSmith](https://docs.langchain.com/langsmith/observability.md) is the platform for tracing, evaluation, prompts, and deployment across frameworks.
* [LangSmith Engine](https://docs.langchain.com/langsmith/engine.md) detects issues in LangGraph agent traces and proposes fixes. You can open a pull request with the proposed fix from the Engine tab.
* [LangSmith Fleet](https://docs.langchain.com/langsmith/fleet/index.md) is the no-code agent builder for templates, integrations, and routine automation.

For a comparison of the open source stack, see [Frameworks, runtimes, and harnesses](https://docs.langchain.com/oss/python/concepts/products.md).

## &#x20;Install

```bash pip
pip install -U langgraph
```

```bash uv
uv add langgraph
```

Create a minimal graph:

```python
from langgraph.graph import StateGraph, MessagesState, START, END

def mock_llm(state: MessagesState):
    return {"messages": [{"role": "ai", "content": "hello world"}]}

graph = StateGraph(MessagesState)
graph.add_node(mock_llm)
graph.add_edge(START, "mock_llm")
graph.add_edge("mock_llm", END)
graph = graph.compile()

graph.invoke({"messages": [{"role": "user", "content": "hi!"}]})
```

For a full calculator agent, see the [LangGraph quickstart](Get%20started/Quickstart.md).

## Capabilities

LangGraph provides the runtime primitives for stateful, long-running workflows. It does not abstract prompts or force a fixed agent architecture.

* **Deterministic and agentic steps**: Combine hand-coded nodes with model-driven nodes in one graph.
* [**Persistence**](Capabilities/Persistence.md): Checkpoint state and resume after failures or pauses.
* [**Human-in-the-loop**](Capabilities/Interrupts.md): Pause execution, inspect or edit state, then continue.
* [**Memory**](https://docs.langchain.com/oss/python/concepts/memory.md): Short-term thread state and longer-term memory across sessions.
* [**Streaming**](Capabilities/Streaming.md): Stream tokens, state updates, and other events as the graph runs.

## Integrations, deployment, and observability

LangGraph works on its own. However, you can also pair it with other LangCHain products:

> [card] [LangChain](https://docs.langchain.com/oss/python/langchain/overview.md)
>
> Integrations and agent abstractions built on LangGraph.

> [card] [LangSmith Deployment](https://docs.langchain.com/langsmith/deployment.md)
>
> Deploy and scale stateful agents, with visual prototyping in Studio.

> [card] [LangSmith Observability](https://docs.langchain.com/langsmith/observability.md)
>
> Trace requests, evaluate outputs, and monitor deployments.

## See also

* [LangGraph quickstart](Get%20started/Quickstart.md)
* [Graph API overview](Build%20with%20the%20Graph%20API/Graph%20API%20overview.md)
* [Choosing between Graph and Functional APIs](Get%20started/Choosing%20between%20Graph%20and%20Functional%20APIs.md)
* [Frameworks, runtimes, and harnesses](https://docs.langchain.com/oss/python/concepts/products.md)

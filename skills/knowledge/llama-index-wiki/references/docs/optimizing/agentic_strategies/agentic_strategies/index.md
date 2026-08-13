# developers.llamaindex.ai/python/framework/optimizing/agentic_strategies/agentic_strategies/index.md
> https://developers.llamaindex.ai/python/framework/optimizing/agentic_strategies/agentic_strategies/index.md

--- title: Agentic strategies | Developer Documentation ---

You can build agents on top of your existing LlamaIndex RAG workflow to empower it with automated decision capabilities. A lot of modules (routing, query transformations, and more) are already agentic in nature in that they use LLMs for decision making.

## Simpler Agentic Strategies
These include routing and query transformations.
- Routing - Query Transformations - Sub Question Query Engine (Intro)
## Data Agents
This guides below show you how to deploy a full agent loop, capable of chain-of-thought and query planning, on top of existing RAG query engines as tools for more advanced decision making.
Make sure to check out our full module guide on Data Agents, which highlight these use cases and much more.
Our lower-level agent API shows you the internals of how an agent works (with step-wise execution).
Example guides below (using LLM-provider-specific function calling):
- Basic Function Agent - Function Agent with Query Engine Tools - Function Agent Retrieval - Function Agent Query Cookbook - Function Agent w/ Context Retrieval
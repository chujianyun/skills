# developers.llamaindex.ai/python/framework/use_cases/prompting/index.md
> https://developers.llamaindex.ai/python/framework/use_cases/prompting/index.md

--- title: Prompting | Developer Documentation ---
Prompting LLMs is a fundamental unit of any LLM application. You can build an entire application entirely around prompting, or orchestrate with other modules (e.g. retrieval) to build RAG, agents, and more.
LlamaIndex supports LLM abstractions and simple-to-advanced prompt abstractions to make complex prompt workflows possible.
## LLM Integrations
LlamaIndex supports 40+ LLM integrations, from proprietary model providers like OpenAI, Anthropic to open-source models/model providers like Mistral, Ollama, Replicate. It provides all the tools to standardize interface around common LLM usage patterns, including but not limited to async, streaming, function calling.
Here’s the full module guide for LLMs.
## Prompts
LlamaIndex has robust prompt abstractions that capture all the common interaction patterns with LLMs.
Here’s the full module guide for prompts.
### Table Stakes
- Text Completion Prompts - Chat Prompts
### Advanced
- Variable Mappings, Functions, Partials - RichPromptTemplate Features
## Prompt Chains and Pipelines
LlamaIndex has robust abstractions for creating sequential prompt chains, as well as general DAGs to orchestrate prompts with any other component. This allows you to build complex workflows, including RAG with multi-hop query understanding layers, as well as agents.
These pipelines are integrated with observability partners out of the box.
# developers.llamaindex.ai/python/framework/changes/deprecated_terms/index.md
> https://developers.llamaindex.ai/python/framework/changes/deprecated_terms/index.md

--- title: Deprecated Terms | Developer Documentation ---
As LlamaIndex continues to evolve, many class names and APIs have been adjusted, improved, and deprecated.
The following is a list of previously popular terms that have been deprecated, with links to their replacements.
## GPTSimpleVectorIndex

This has been renamed to `VectorStoreIndex`, as well as unifying all vector indexes to a single unified interface. You can integrate with various vector databases by modifying the underlying `vector_store`.

Please see the following links for more details on usage.

## GPTVectorStoreIndex
This has been renamed to `VectorStoreIndex`, but it is only a cosmetic change. Please see the following links for more details on usage.
- Index Usage Pattern - Vector Store Guide - Vector Store Integrations
## LLMPredictor

The `LLMPredictor` object is no longer intended to be used by users. Instead, you can setup an LLM directly and pass it into the `Settings` or the interface using the LLM. The `LLM` class itself has similar attributes and methods as the `LLMPredictor`.

- LLMs in LlamaIndex - Setting LLMs in the Settings
## PromptHelper and max\_input\_size/
The `max_input_size` parameter for the prompt helper has since been replaced with `context_window`.
The `PromptHelper` in general has been deprecated in favour of specifying parameters directly in the `service_context` and `node_parser`.
See the following links for more details.
- Configuring settings in the Settings - Parsing Documents into Nodes
## ServiceContext
The `ServiceContext` object has been deprecated in favour of the `Settings` object.
- Configuring settings in the Settings
## llama-index-legacy
The `llama-index-legacy` package has been deprecated and removed from the repository. Please see the latest getting started guide for the latest information and usage.
- Getting Started
## AgentRunner/AgentWorker (and related classes)

The `AgentRunner` and `AgentWorker` classes have been deprecated in favour of AgentWorkflow and Workflows.

- `AgentRunner` - `FunctionCallingAgent` - `FunctionCallingAgentWorker` - `llama_index.core.agent.ReActAgent` (use llama\_index.core.agent.workflow.ReActAgent) - `ReActAgentWorker` - `LATSAgentWorker` - `CoAAgentWorker` - `FnAgentWorker` - `QueryPipelineAgentWorker` - `MultiModalReActAgentWorker` - `IntrospectiveAgentWorker` - `SelfReflectiveAgentWorker` - `ToolInteractiveReflectionAgentWorker` - `LLMCompilerAgentWorker` - `QueryUnderstandAgentWorker`

## QueryPipeline (and related classes)
QueryPipeline has been deprecated in favour of Workflows.
This includes the following deprecated classes:
- `AgentFnComponent` - `AgentInputComponent` - `BaseAgentComponent` - `CustomAgentComponent` - `ArgPackComponent` - `FnComponent` - `FunctionComponent` - `InputComponent` - `RouterComponent` - `SelectorComponent` - `ToolRunnerComponent` - `StatefulFnComponent` - `LoopComponent` - etc.
# developers.llamaindex.ai/python/framework/optimizing/custom_modules/index.md
> https://developers.llamaindex.ai/python/framework/optimizing/custom_modules/index.md

--- title: Writing Custom Modules | Developer Documentation ---
A core design principle of LlamaIndex is that **almost every core module can be subclassed and customized**.

This allows you to use LlamaIndex for any advanced LLM use case, beyond the capabilities offered by our prepackaged modules. You’re free to write as much custom code for any given module, but still take advantage of our lower-level abstractions and also plug this module along with other components.

We offer convenient/guided ways to subclass our modules, letting you write your custom logic without having to worry about having to define all boilerplate (for instance, [callbacks] (/python/framework/module_guides/observability/callbacks/index.md)).
This guide centralizes all the resources around writing custom modules in LlamaIndex. Check them out below 👇
## Custom LLMs
- Custom LLMs
## Custom Embeddings
- Custom Embedding Model
## Custom Output Parsers
- Custom Output Parsers
## Custom Transformations
- Custom Transformations - Custom Property Graph Extractors
## Custom Retrievers
- Custom Retrievers - Custom Property Graph Retrievers
## Custom Postprocessors/Rerankers
- Custom Node Postprocessor
## Custom Query Engines
- Custom Query Engine
## Custom Agents
- Custom Function Calling Agent - Custom ReAct Agent
## Other Ways of Customization
Some modules can be customized heavily within your workflows but not through subclassing (and instead through parameters or functions we expose). We list these in guides below:
- Customizing Documents - Customizing Nodes - Customizing Prompts within Higher-Level Modules
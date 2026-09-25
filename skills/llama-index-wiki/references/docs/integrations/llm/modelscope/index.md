# developers.llamaindex.ai/python/framework/integrations/llm/modelscope/index.md
> https://developers.llamaindex.ai/python/framework/integrations/llm/modelscope/index.md

--- title: ModelScope LLMS | Developer Documentation ---

In this notebook, we show how to use the ModelScope LLM models in LlamaIndex. Check out the ModelScope site [1].

If you’re opening this Notebook on colab, you will need to install LlamaIndex 🦙 and the modelscope.
``` !pip install llama-index-llms-modelscope ```
## Basic Usage
``` import sys from llama_index.llms.modelscope import ModelScopeLLM

llm = ModelScopeLLM(model_name="qwen/Qwen3-8B", model_revision="master")
rsp = llm.complete("Hello, who are you?") print(rsp) ```
#### Use Message request
``` from llama_index.core.base.llms.types import MessageRole, ChatMessage
messages = [ ChatMessage( role=MessageRole.SYSTEM, content="You are a helpful assistant." ), ChatMessage(role=MessageRole.USER, content="How to make cake?"), ] resp = llm.chat(messages) print(resp) ```

[1] https://www.modelscope.cn/
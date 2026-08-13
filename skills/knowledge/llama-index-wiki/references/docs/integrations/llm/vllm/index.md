# developers.llamaindex.ai/python/framework/integrations/llm/vllm/index.md
> https://developers.llamaindex.ai/python/framework/integrations/llm/vllm/index.md

--- title: vLLM | Developer Documentation ---

There’s two modes of using vLLM local and remote. Let’s start form the former one, which requeries CUDA environment available locally.
### Install vLLM
`pip install vllm`\ or if you want to compile you can compile from source [1]
### Orca-7b Completion Example
``` %pip install llama-index-llms-vllm ```
``` import os
os.environ["HF_HOME"] = "model/" ```
``` from llama_index.llms.vllm import Vllm, VllmServer ```
``` llm = Vllm( model="microsoft/Orca-2-7b", tensor_parallel_size=4, max_new_tokens=100, vllm_kwargs={"swap_space": 1, "gpu_memory_utilization": 0.5}, ) ```

``` llm.complete("[INST]You are a helpful assistant[/INST] What is a black hole ?") ```
### LLama-2-7b Completion Example
``` llm = Vllm( model="codellama/CodeLlama-7b-hf", dtype="float16", tensor_parallel_size=4, temperature=0, max_new_tokens=100, vllm_kwargs={ "swap_space": 1, "gpu_memory_utilization": 0.5, "max_model_len": 4096, }, ) ```

``` llm.complete("import socket\n\ndef ping_exponential_backoff(host: str):") ```
### Mistral chat 7b Completion Example
``` llm = Vllm( model="mistralai/Mistral-7B-Instruct-v0.1", dtype="float16", tensor_parallel_size=4, temperature=0, max_new_tokens=100, vllm_kwargs={ "swap_space": 1, "gpu_memory_utilization": 0.5, "max_model_len": 4096, }, ) ```

``` Vllm mock initialized ```
``` llm.complete(" What is a black hole ?") ```
# Calling vLLM via HTTP

In this mode there is no need to install `vllm` model nor have CUDA available locally. To setup the vLLM API you can follow the guide present here [2]. Note: `llama-index-llms-vllm` module is a client for `vllm.entrypoints.api_server` which is only a demo [3].\ If vLLM server is launched with `vllm.entrypoints.openai.api_server` as OpenAI Compatible Server [4] or via [Docker] [5] you need `OpenAILike` class from `llama-index-llms-openai-like` module

### Completion Response
``` from llama_index.core.llms import ChatMessage ```
``` llm = VllmServer( api_url="http://localhost:8000/generate", max_new_tokens=100, temperature=0 ) ```
``` llm.complete("what is a black hole ?") ```
``` message = [ChatMessage(content="hello", role="user")] llm.chat(message) ```
### Streaming Response
``` list(llm.stream_complete("what is a black hole"))[-1] ```
``` message = [ChatMessage(content="what is a black hole", role="user")] [x for x in llm.stream_chat(message)][-1] ```
### Async Response
``` import asyncio
await llm.acomplete("What is a black hole") ```
``` await llm.achat(message) ```
``` [x async for x in await llm.astream_complete("what is a black hole")][-1] ```
``` [x async for x in await llm.astream_chat(message)][-1] ```

[1] https://docs.vllm.ai/en/latest/getting_started/installation.html
[2] https://docs.vllm.ai/en/latest/serving/distributed_serving.html
[3] https://github.com/vllm-project/vllm/blob/abfc4f3387c436d46d6701e9ba916de8f9ed9329/vllm/entrypoints/api_server.py#L2
[4] https://docs.vllm.ai/en/latest/getting_started/quickstart.html#openai-compatible-server
[5] https://docs.vllm.ai/en/latest/serving/deploying_with_docker.html
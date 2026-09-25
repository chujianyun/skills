# developers.llamaindex.ai/python/framework/integrations/llm/nvidia_text_completion/index.md
> https://developers.llamaindex.ai/python/framework/integrations/llm/nvidia_text_completion/index.md

--- title: NVIDIA LLM Text Completion API | Developer Documentation ---

The `llama-index-llms-nvidia` package extends the `NVIDIA` class to support the `/completions` API for code completion models such as:
- `bigcode/starcoder2-7b` - `bigcode/starcoder2-15b`
## Installation
``` %pip install --upgrade --quiet llama-index-llms-nvidia ```
## Setup
**To get started:**
1. Create a free account with NVIDIA [1], which hosts NVIDIA AI Foundation models.
2. Click on your model of choice.
3. Under Input select the Python tab, and click `Get API Key`. Then click `Generate Key`.
4. Copy and save the generated key as NVIDIA\_API\_KEY. From there, you should have access to the endpoints.
``` import getpass import os

# del os.environ['NVIDIA_API_KEY'] ## delete key and reset if os.environ.get("NVIDIA_API_KEY", "").startswith("nvapi-"): print("Valid NVIDIA_API_KEY already in environment. Delete to reset") else: nvapi_key = getpass.getpass("NVAPI Key (starts with nvapi-): ") assert nvapi_key.startswith( "nvapi-" ), f"{nvapi_key[:5]}... is not a valid key" os.environ["NVIDIA_API_KEY"] = nvapi_key ```
``` # llama-parse is async-first, running the async code in a notebook requires the use of nest_asyncio import nest_asyncio

nest_asyncio.apply() ```
## Working with the NVIDIA API Catalog
### Usage of the `use_chat_completions` argument

Set `None` (default) to decide per-invocation whether to use `/chat/completions` or `/completions` endpoints with query keyword arguments.

- Set `False` to use the `/completions` endpoint. - Set `True` to use the `/chat/completions` endpoint.

llm = NVIDIA(model="bigcode/starcoder2-15b", use_chat_completions=False) ```
### Available models
Use `is_chat_model` to filter available text completion models:
``` print([model for model in llm.available_models if model.is_chat_model]) ```
## Working with NVIDIA NIMs

In addition to connecting to hosted NVIDIA NIMs [2], this connector can be used to connect to local NIM instances. This helps you take your applications local when necessary.

For instructions on how to set up local NIM instances, refer to NVIDIA NIM [3].
``` from llama_index.llms.nvidia import NVIDIA

# Connect to a NIM running at localhost:8080 llm = NVIDIA(base_url="http://localhost:8080/v1") ```
### Complete: `.complete()`
We can use `.complete()`/`.acomplete()` (which takes a string) to prompt a response from the selected model.
Let’s use our default model for this task.
``` print(llm.complete("# Function that does quicksort:")) ```
As expected, LlamaIndex returns a `CompletionResponse`.
#### Async Complete: `.acomplete()`
There is also an async implementation which can be leveraged in the same way!
``` await llm.acomplete("# Function that does quicksort:") ```
#### Streaming
``` x = llm.stream_complete(prompt="# Reverse string in python:", max_tokens=512) ```
``` for t in x: print(t.delta, end="") ```

#### Async Streaming
``` x = await llm.astream_complete( prompt="# Reverse program in python:", max_tokens=512 ) ```

``` async for t in x: print(t.delta, end="") ```

[1] https://build.nvidia.com/
[2] https://ai.nvidia.com
[3] https://developer.nvidia.com/nim
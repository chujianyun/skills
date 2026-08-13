# developers.llamaindex.ai/python/framework/integrations/llm/openvino/index.md
> https://developers.llamaindex.ai/python/framework/integrations/llm/openvino/index.md

--- title: OpenVINO LLMs | Developer Documentation ---

OpenVINO™ [1] is an open-source toolkit for optimizing and deploying AI inference. OpenVINO™ Runtime can enable running the same model optimized across various hardware [devices] [2]. Accelerate your deep learning performance across use cases like: language + LLMs, computer vision, automatic speech recognition, and more.

OpenVINO models can be run locally through `OpenVINOLLM` entitiy wrapped by LlamaIndex :
In the below line, we install the packages necessary for this demo:
``` %pip install llama-index-llms-openvino transformers huggingface_hub ```
Now that we’re set up, let’s play around:
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.
``` !pip install llama-index ```
``` from llama_index.llms.openvino import OpenVINOLLM ```
``` def messages_to_prompt(messages): prompt = "" for message in messages: if message.role == "system": prompt += f"<|system|>\n{message.content}</s>\n" elif message.role == "user": prompt += f"<|user|>\n{message.content}</s>\n" elif message.role == "assistant": prompt += f"<|assistant|>\n{message.content}</s>\n"

# ensure we start with a system prompt, insert blank if needed if not prompt.startswith("<|system|>\n"): prompt = "<|system|>\n</s>\n" + prompt

# add final assistant prompt prompt = prompt + "<|assistant|>\n"
return prompt

def completion_to_prompt(completion): return f"<|system|>\n</s>\n<|user|>\n{completion}</s>\n<|assistant|>\n" ```
### Model Loading
Models can be loaded by specifying the model parameters using the `OpenVINOLLM` method.
If you have an Intel GPU, you can specify `device_map="gpu"` to run inference on it.
``` ov_config = { "PERFORMANCE_HINT": "LATENCY", "NUM_STREAMS": "1", "CACHE_DIR": "", }

ov_llm = OpenVINOLLM( model_id_or_path="HuggingFaceH4/zephyr-7b-beta", context_window=3900, max_new_tokens=256, model_kwargs={"ov_config": ov_config}, generate_kwargs={"temperature": 0.7, "top_k": 50, "top_p": 0.95}, messages_to_prompt=messages_to_prompt, completion_to_prompt=completion_to_prompt, device_map="cpu", ) ```

``` response = ov_llm.complete("What is the meaning of life?") print(str(response)) ```

### Inference with local OpenVINO model

It is possible to export your model [3] to the OpenVINO IR format with the CLI, and load the model from local folder.

``` !optimum-cli export openvino --model HuggingFaceH4/zephyr-7b-beta ov_model_dir ```
It is recommended to apply 8 or 4-bit weight quantization to reduce inference latency and model footprint using `--weight-format`:
``` !optimum-cli export openvino --model HuggingFaceH4/zephyr-7b-beta --weight-format int8 ov_model_dir ```
``` !optimum-cli export openvino --model HuggingFaceH4/zephyr-7b-beta --weight-format int4 ov_model_dir ```
``` ov_llm = OpenVINOLLM( model_id_or_path="ov_model_dir", context_window=3900, max_new_tokens=256, model_kwargs={"ov_config": ov_config}, generate_kwargs={"temperature": 0.7, "top_k": 50, "top_p": 0.95}, messages_to_prompt=messages_to_prompt, completion_to_prompt=completion_to_prompt, device_map="gpu", ) ```

You can get additional inference speed improvement with Dynamic Quantization of activations and KV-cache quantization. These options can be enabled with `ov_config` as follows:

``` ov_config = { "KV_CACHE_PRECISION": "u8", "DYNAMIC_QUANTIZATION_GROUP_SIZE": "32", "PERFORMANCE_HINT": "LATENCY", "NUM_STREAMS": "1", "CACHE_DIR": "", } ```

### Streaming
Using `stream_complete` endpoint
``` response = ov_llm.stream_complete("Who is Paul Graham?") for r in response: print(r.delta, end="") ```

Using `stream_chat` endpoint
``` from llama_index.core.llms import ChatMessage
messages = [ ChatMessage( role="system", content="You are a pirate with a colorful personality" ), ChatMessage(role="user", content="What is your name"), ] resp = ov_llm.stream_chat(messages)

for r in resp: print(r.delta, end="") ```
For more information refer to:
- OpenVINO LLM guide [4].
- OpenVINO Documentation [5].
- OpenVINO Get Started Guide [6].
- RAG example with LlamaIndex [7].

[1] https://github.com/openvinotoolkit/openvino
[2] https://github.com/openvinotoolkit/openvino?tab=readme-ov-file#supported-hardware-matrix
[3] https://github.com/huggingface/optimum-intel?tab=readme-ov-file#export
[4] https://docs.openvino.ai/2024/learn-openvino/llm_inference_guide.html
[5] https://docs.openvino.ai/2024/home.html
[6] https://www.intel.com/content/www/us/en/content-details/819067/openvino-get-started-guide.html
[7] https://github.com/openvinotoolkit/openvino_notebooks/tree/latest/notebooks/llm-rag-llamaindex
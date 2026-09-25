# developers.llamaindex.ai/python/framework/integrations/llm/optimum_intel/index.md
> https://developers.llamaindex.ai/python/framework/integrations/llm/optimum_intel/index.md

--- title: Optimum Intel LLMs optimized with IPEX backend | Developer Documentation ---

Optimum Intel [1] accelerates Hugging Face pipelines on Intel architectures leveraging Intel Extension for Pytorch, (IPEX) [2] optimizations

Optimum Intel models can be run locally through `OptimumIntelLLM` entitiy wrapped by LlamaIndex :
In the below line, we install the packages necessary for this demo:
``` %pip install llama-index-llms-optimum-intel ```
Now that we’re set up, let’s play around:
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.
``` !pip install llama-index ```
``` from llama_index.llms.optimum_intel import OptimumIntelLLM ```
``` def messages_to_prompt(messages): prompt = "" for message in messages: if message.role == "system": prompt += f"<|system|>\n{message.content}</s>\n" elif message.role == "user": prompt += f"<|user|>\n{message.content}</s>\n" elif message.role == "assistant": prompt += f"<|assistant|>\n{message.content}</s>\n"

# ensure we start with a system prompt, insert blank if needed if not prompt.startswith("<|system|>\n"): prompt = "<|system|>\n</s>\n" + prompt

# add final assistant prompt prompt = prompt + "<|assistant|>\n"
return prompt

def completion_to_prompt(completion): return f"<|system|>\n</s>\n<|user|>\n{completion}</s>\n<|assistant|>\n" ```
### Model Loading
Models can be loaded by specifying the model parameters using the `OptimumIntelLLM` method.
``` oi_llm = OptimumIntelLLM( model_name="Intel/neural-chat-7b-v3-3", tokenizer_name="Intel/neural-chat-7b-v3-3", context_window=3900, max_new_tokens=256, generate_kwargs={"temperature": 0.7, "top_k": 50, "top_p": 0.95}, messages_to_prompt=messages_to_prompt, completion_to_prompt=completion_to_prompt, device_map="cpu", ) ```

``` response = oi_llm.complete("What is the meaning of life?") print(str(response)) ```

### Streaming
Using `stream_complete` endpoint
``` response = oi_llm.stream_complete("Who is Mother Teresa?") for r in response: print(r.delta, end="") ```

Using `stream_chat` endpoint
``` from llama_index.core.llms import ChatMessage
messages = [ ChatMessage( role="system", content="You are an American chef in a small restaurant in New Orleans", ), ChatMessage(role="user", content="What is your dish of the day?"), ] resp = oi_llm.stream_chat(messages)

for r in resp: print(r.delta, end="") ```

[1] https://github.com/rbrugaro/optimum-intel
[2] https://github.com/intel/intel-extension-for-pytorch
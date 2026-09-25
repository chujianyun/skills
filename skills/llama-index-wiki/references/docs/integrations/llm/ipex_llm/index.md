# developers.llamaindex.ai/python/framework/integrations/llm/ipex_llm/index.md
> https://developers.llamaindex.ai/python/framework/integrations/llm/ipex_llm/index.md

--- title: IPEX-LLM on Intel CPU | Developer Documentation ---

> IPEX-LLM [1] is a PyTorch library for running LLM on Intel CPU and GPU (e.g., local PC with iGPU, discrete GPU such as Arc, Flex and Max) with very low latency.
This example goes over how to use LlamaIndex to interact with `ipex-llm` [1] for text generation and chat on CPU.
> **Note** > > You could refer to here [2] for full examples of `IpexLLM`. Please note that for running on Intel CPU, please specify `-d 'cpu'` in command argument when running the examples.

Install `llama-index-llms-ipex-llm`. This will also install `ipex-llm` and its dependencies.
``` %pip install llama-index-llms-ipex-llm ```
In this example we’ll use HuggingFaceH4/zephyr-7b-alpha [3] model for demostration. It requires updating `transformers` and `tokenizers` packages.
``` %pip install -U transformers==4.37.0 tokenizers==0.15.2 ```
Before loading the Zephyr model, you’ll need to define `completion_to_prompt` and `messages_to_prompt` for formatting prompts. This is essential for preparing inputs that the model can interpret accurately.
``` # Transform a string into input zephyr-specific input def completion_to_prompt(completion): return f"<|system|>\n</s>\n<|user|>\n{completion}</s>\n<|assistant|>\n"

[Column 1]
# Transform a list of chat messages into zephyr-specific input def messages_to_prompt(messages): prompt = "" for message in messages: if message.role == "system": prompt += f"<|system|>\n{message.content}</s>\n" elif message.role == "user": prompt += f"<|user|>\n{message.content}</s>\n" elif message.role == "assistant": prompt += f"<|assistant|>\n{message.content}</s>\n"

# ensure we start with a system prompt, insert blank if needed if not prompt.startswith("<|system|>\n"): prompt = "<|system|>\n</s>\n" + prompt
# add final assistant prompt prompt = prompt + "<|assistant|>\n"
return prompt ```
## Basic Usage
``` import warnings
warnings.filterwarnings( "ignore", category=UserWarning, message=".*padding_mask.*" )
from llama_index.llms.ipex_llm import IpexLLM
llm = IpexLLM.from_model_id( model_name="HuggingFaceH4/zephyr-7b-alpha", tokenizer_name="HuggingFaceH4/zephyr-7b-alpha", context_window=512, max_new_tokens=128, generate_kwargs={"do_sample": False}, completion_to_prompt=completion_to_prompt, messages_to_prompt=messages_to_prompt, ) ```

``` Loading checkpoint shards: 0%| | 0/8 [00:00<?, ?it/s]

[Column 2]
Load the Zephyr model locally using IpexLLM using `IpexLLM.from_model_id`. It will load the model directly in its Huggingface format and convert it automatically to low-bit format for inference.


2024-04-11 21:36:54,739 - INFO - Converting the current model to sym_int4 format...... ```
Now you can proceed to use the loaded model for text completion and interactive chat.
### Text Completion
``` completion_response = llm.complete("Once upon a time, ") print(completion_response.text) ```

``` in a far-off land, there was a young girl named Lily. Lily lived in a small village surrounded by lush green forests and rolling hills. She loved nothing more than spending her days exploring the woods and playing with her animal friends. One day, while wandering through the forest, Lily stumbled upon a magical tree. The tree was unlike any other she had ever seen. Its trunk was made of shimmering crystal, and its branches were adorned with sparkling jewels. Lily was immediately drawn to the tree and sat down to admire its beauty. Suddenly, ```

### Streaming Text Completion
``` response_iter = llm.stream_complete("Once upon a time, there's a little girl") for response in response_iter: print(response.delta, end="", flush=True) ```

``` who loved to play with her toys. She had a favorite teddy bear named Ted, and a doll named Dolly. She would spend hours playing with them, imagining all sorts of adventures. One day, she decided to take Ted and Dolly on a real adventure. She packed a backpack with some snacks, a blanket, and a map. They set off on a hike in the nearby woods. The little girl was so excited that she could barely contain her joy. Ted and Dolly were happy to be along for the ride. They walked for what seemed like hours, but the little girl didn't mind

### Chat
``` from llama_index.core.llms import ChatMessage
message = ChatMessage(role="user", content="Explain Big Bang Theory briefly") resp = llm.chat([message]) print(resp) ```

``` assistant: The Big Bang Theory is a popular American sitcom that aired from 2007 to 2019. The show follows the lives of two brilliant but socially awkward physicists, Leonard Hofstadter (Johnny Galecki) and Sheldon Cooper (Jim Parsons), and their friends and colleagues, Penny (Kaley Cuoco), Rajesh Koothrappali (Kunal Nayyar), and Howard Wolowitz (Simon Helberg). The show is set in Pasadena, California, and revolves around the characters' work at Caltech and
```
### Streaming Chat
``` message = ChatMessage(role="user", content="What is AI?") resp = llm.stream_chat([message], max_tokens=256) for r in resp: print(r.delta, end="") ```

``` AI stands for Artificial Intelligence. It refers to the development of computer systems that can perform tasks that typically require human intelligence, such as learning, reasoning, and problem-solving. AI involves the use of machine learning algorithms, natural language processing, and other advanced techniques to enable computers to understand and respond to human input in a more natural and intuitive way. ```

## Save/Load Low-bit Model
Alternatively, you might save the low-bit model to disk once and use `from_model_id_low_bit` instead of `from_model_id` to reload it for later use - even across different machines. It is space-efficient, as the low-bit model demands significantly less disk space than the original model. And `from_model_id_low_bit` is also more efficient than `from_model_id` in terms of speed and memory usage, as it skips the model conversion step.
To save the low-bit model, use `save_low_bit` as follows.
``` saved_lowbit_model_path = ( "./zephyr-7b-alpha-low-bit" # path to save low-bit model )

llm._model.save_low_bit(saved_lowbit_model_path) del llm ```
Load the model from saved lowbit model path as follows.
> Note that the saved path for the low-bit model only includes the model itself but not the tokenizers. If you wish to have everything in one place, you will need to manually download or copy the tokenizer files from the original model’s directory to the location where the low-bit model is saved.
``` llm_lowbit = IpexLLM.from_model_id_low_bit( model_name=saved_lowbit_model_path, tokenizer_name="HuggingFaceH4/zephyr-7b-alpha", # tokenizer_name=saved_lowbit_model_path, # copy the tokenizers to saved path if you want to use it this way context_window=512, max_new_tokens=64, completion_to_prompt=completion_to_prompt, generate_kwargs={"do_sample": False}, ) ```

``` 2024-04-11 21:38:06,151 - INFO - Converting the current model to sym_int4 format...... ```
Try stream completion using the loaded low-bit model.
``` response_iter = llm_lowbit.stream_complete("What is Large Language Model?") for response in response_iter: print(response.delta, end="", flush=True) ```

``` A large language model (LLM) is a type of artificial intelligence (AI) model that is trained on a massive amount of text data. These models are capable of generating human-like responses to text inputs and can be used for various natural language processing (NLP) tasks, such as text classification, sentiment analysis ```

[1] https://github.com/intel-analytics/ipex-llm/
[2] https://github.com/run-llama/llama_index/tree/main/llama-index-integrations/llms/llama-index-llms-ipex-llm/examples
[3] https://huggingface.co/HuggingFaceH4/zephyr-7b-alpha
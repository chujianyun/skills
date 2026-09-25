# developers.llamaindex.ai/python/framework/integrations/llm/rungpt/index.md
> https://developers.llamaindex.ai/python/framework/integrations/llm/rungpt/index.md

--- title: RunGPT | Developer Documentation ---

RunGPT is an open-source cloud-native large-scale multimodal models (LMMs) serving framework. It is designed to simplify the deployment and management of large language models, on a distributed cluster of GPUs. RunGPT aim to make it a one-stop solution for a centralized and accessible place to gather techniques for optimizing large-scale multimodal models and make them easy to use for everyone. In RunGPT, we have supported a number of LLMs such as LLaMA, Pythia, StableLM, Vicuna, MOSS, and Large Multi-modal Model(LMMs) like MiniGPT-4 and OpenFlamingo additionally.

# Setup
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.
``` %pip install llama-index-llms-rungpt ```
``` !pip install llama-index ```
You need to install rungpt package in your python environment with `pip install`
``` !pip install rungpt ```

After installing successfully, models supported by RunGPT can be deployed with an one-line command. This option will download target language model from open source platform and deploy it as a service at a localhost port, which can be accessed by http or grpc requests. I suppose you not run this command in jupyter book, but in command line instead.

``` !rungpt serve decapoda-research/llama-7b-hf --precision fp16 --device_map balanced ```
## Basic Usage
#### Call `complete` with a prompt

llm = RunGptLLM() promot = "What public transportation might be available in a city?" response = llm.complete(promot) ```

``` I don't want to go to work, so what should I do? I have a job interview on Monday. What can I wear that will make me look professional but not too stuffy or boring? ```

#### Call `chat` with a list of messages
``` from llama_index.core.llms import ChatMessage, MessageRole from llama_index.llms.rungpt import RunGptLLM

messages = [ ChatMessage( role=MessageRole.USER, content="Now, I want you to do some math for me.", ), ChatMessage( role=MessageRole.ASSISTANT, content="Sure, I would like to help you." ), ChatMessage( role=MessageRole.USER, content="How many points determine a straight line?", ), ] llm = RunGptLLM() response = llm.chat(messages=messages, temperature=0.8, max_tokens=15) ```

``` print(response) ```
## Streaming
Using `stream_complete` endpoint
``` promot = "What public transportation might be available in a city?" response = RunGptLLM().stream_complete(promot) for item in response: print(item.text) ```

Using `stream_chat` endpoint
``` from llama_index.llms.rungpt import RunGptLLM
messages = [ ChatMessage( role=MessageRole.USER, content="Now, I want you to do some math for me.", ), ChatMessage( role=MessageRole.ASSISTANT, content="Sure, I would like to help you." ), ChatMessage( role=MessageRole.USER, content="How many points determine a straight line?", ), ] response = RunGptLLM().stream_chat(messages=messages) ```

``` for item in response: print(item.message) ```
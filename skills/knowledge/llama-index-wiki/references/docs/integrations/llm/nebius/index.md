# developers.llamaindex.ai/python/framework/integrations/llm/nebius/index.md
> https://developers.llamaindex.ai/python/framework/integrations/llm/nebius/index.md

[Column 1]
--- title: Nebius LLMs | Developer Documentation ---

First, let’s install LlamaIndex and dependencies of Nebius AI Studio.
``` %pip install llama-index-llms-nebius llama-index ```

``` import os
NEBIUS_API_KEY = os.getenv("NEBIUS_API_KEY") # NEBIUS_API_KEY = "" ```
``` from llama_index.llms.nebius import NebiusLLM
llm = NebiusLLM( api_key=NEBIUS_API_KEY, model="meta-llama/Llama-3.3-70B-Instruct-fast" ) ```

#### Call `complete` with a prompt
``` response = llm.complete("Amsterdam is the capital of ") print(response) ```

[Column 2]
This notebook demonstrates how to use LLMs from Nebius AI Studio [1] with LlamaIndex. Nebius AI Studio implements all state-of-the-art LLMs available for commercial use.
Upload your Nebius AI Studio key from system variables below or simply insert it. You can get it by registering for free at Nebius AI Studio [2] and issuing the key at [API Keys section] [3].”

``` None of PyTorch, TensorFlow >= 2.0, or Flax have been found. Models won't be available and only tokenizers, configuration and file/data utilities can be used. ```


#### Call `chat` with a list of messages

messages = [ ChatMessage(role="system", content="You are a helpful AI assistant."), ChatMessage( role="user", content="Answer briefly: who is Wall-e?", ), ] response = llm.chat(messages) print(response) ```

``` assistant: WALL-E is a small waste-collecting robot and the main character in the 2008 Pixar animated film of the same name. ```
### Streaming
#### Using `stream_complete` endpoint
``` response = llm.stream_complete("Amsterdam is the capital of ") for r in response: print(r.delta, end="") ```

``` The Netherlands! Amsterdam is indeed the capital and largest city of the Netherlands. ```
#### Using `stream_chat` with a list of messages
``` from llama_index.core.llms import ChatMessage
messages = [ ChatMessage(role="system", content="You are a helpful AI assistant."), ChatMessage( role="user", content="Answer briefly: who is Wall-e?", ), ] response = llm.stream_chat(messages) for r in response: print(r.delta, end="") ```

``` WALL-E is a small waste-collecting robot and the main character in the 2008 Pixar animated film of the same name. ```

[1] https://studio.nebius.ai/
[2] https://auth.eu.nebius.com/ui/login
[3] https://studio.nebius.ai/settings/api-keys
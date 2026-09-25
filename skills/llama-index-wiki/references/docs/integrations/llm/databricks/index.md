# developers.llamaindex.ai/python/framework/integrations/llm/databricks/index.md
> https://developers.llamaindex.ai/python/framework/integrations/llm/databricks/index.md

--- title: Databricks | Developer Documentation ---

Integrate with Databricks LLMs APIs.
## Pre-requisites
- Databricks personal access token [1] to query and access Databricks model serving endpoints.

- Databricks workspace [2] in a supported region [3] for Foundation Model APIs pay-per-token.

## Setup
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.
``` % pip install llama-index-llms-databricks ```
``` !pip install llama-index ```
``` from llama_index.llms.databricks import Databricks ```

``` None of PyTorch, TensorFlow >= 2.0, or Flax have been found. Models won't be available and only tokenizers, configuration and file/data utilities can be used. ```

Terminal window
``` export DATABRICKS_TOKEN=<your api key> export DATABRICKS_SERVING_ENDPOINT=<your api serving endpoint> ```

Alternatively, you can pass your API key and serving endpoint to the LLM when you init it:
``` llm = Databricks( model="databricks-dbrx-instruct", api_key="<API_KEY>", api_base="https://[your-work-space].cloud.databricks.com/serving-endpoints/", ) ```

A list of available LLM models can be found here [4].
``` response = llm.complete("Explain the importance of open source LLMs") ```
``` print(response) ```
#### Call `chat` with a list of messages

messages = [ ChatMessage( role="system", content="You are a pirate with a colorful personality" ), ChatMessage(role="user", content="What is your name"), ] resp = llm.chat(messages) ```

``` print(resp) ```
### Streaming
Using `stream_complete` endpoint
``` response = llm.stream_complete("Explain the importance of open source LLMs") ```
``` for r in response: print(r.delta, end="") ```

Using `stream_chat` endpoint
``` from llama_index.core.llms import ChatMessage
messages = [ ChatMessage( role="system", content="You are a pirate with a colorful personality" ), ChatMessage(role="user", content="What is your name"), ] resp = llm.stream_chat(messages) ```

``` for r in resp: print(r.delta, end="") ```

[1] https://docs.databricks.com/en/dev-tools/auth/pat.html
[2] https://docs.databricks.com/en/workspace/index.html
[3] https://docs.databricks.com/en/machine-learning/model-serving/model-serving-limits.html#regions
[4] https://console.groq.com/docs/models
# developers.llamaindex.ai/python/framework/integrations/llm/qianfan/index.md
> https://developers.llamaindex.ai/python/framework/integrations/llm/qianfan/index.md

--- title: Client of Baidu Intelligent Cloud's Qianfan LLM Platform | Developer Documentation ---

Baidu Intelligent Cloud’s Qianfan LLM Platform offers API services for all Baidu LLMs, such as ERNIE-3.5-8K and ERNIE-4.0-8K. It also provides a small number of open-source LLMs like Llama-2-70b-chat.

Before using the chat client, you need to activate the LLM service on the Qianfan LLM Platform console’s online service [1] page. Then, Generate an Access Key and a Secret Key in the Security Authentication [2] page of the console.

## Installation
Install the necessary package:
``` %pip install llama-index-llms-qianfan ```
## Initialization
``` from llama_index.llms.qianfan import Qianfan import asyncio

access_key = "XXX" secret_key = "XXX" model_name = "ERNIE-Speed-8K" endpoint_url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ernie_speed" context_window = 8192 llm = Qianfan(access_key, secret_key, model_name, endpoint_url, context_window) ```

## Synchronous Chat
Generate a chat response synchronously using the `chat` method:
``` from llama_index.core.base.llms.types import ChatMessage
messages = [ ChatMessage(role="user", content="Tell me a joke."), ] chat_response = llm.chat(messages) print(chat_response.message.content) ```

## Synchronous Stream Chat
Generate a streaming chat response synchronously using the `stream_chat` method:
``` messages = [ ChatMessage(role="system", content="You are a helpful assistant."), ChatMessage(role="user", content="Tell me a story."), ] content = "" for chat_response in llm.stream_chat(messages): content += chat_response.delta print(chat_response.delta, end="") ```

## Asynchronous Chat
Generate a chat response asynchronously using the `achat` method:
``` async def async_chat(): messages = [ ChatMessage(role="user", content="Tell me an async joke."), ] chat_response = await llm.achat(messages) print(chat_response.message.content)

asyncio.run(async_chat()) ```
## Asynchronous Stream Chat
Generate a streaming chat response asynchronously using the `astream_chat` method:
``` async def async_stream_chat(): messages = [ ChatMessage(role="system", content="You are a helpful assistant."), ChatMessage(role="user", content="Tell me an async story."), ] content = "" response = await llm.astream_chat(messages) async for chat_response in response: content += chat_response.delta print(chat_response.delta, end="")

asyncio.run(async_stream_chat()) ```

[1] https://console.bce.baidu.com/qianfan/ais/console/onlineService
[2] https://console.bce.baidu.com/iam/#/iam/accesslist
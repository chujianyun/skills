# developers.llamaindex.ai/python/framework/integrations/llm/maritalk/index.md
> https://developers.llamaindex.ai/python/framework/integrations/llm/maritalk/index.md

--- title: Maritalk | Developer Documentation ---
## Introduction

MariTalk is an assistant developed by the Brazilian company Maritaca AI [1]. MariTalk is based on language models that have been specially trained to understand Portuguese well.

This notebook demonstrates how to use MariTalk with Llama Index through two examples:
1. Get pet name suggestions with chat method; 2. Classify film reviews as negative or positive with few-shot examples with complete method.
## Installation
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex.
``` !pip install llama-index !pip install llama-index-llms-maritalk !pip install asyncio ```

## API Key
You will need an API key that can be obtained from chat.maritaca.ai (“Chaves da API” section).
### Example 1 - Pet Name Suggestions with Chat
``` from llama_index.core.llms import ChatMessage from llama_index.llms.maritalk import Maritalk

import asyncio
# To customize your API key, do this # otherwise it will lookup MARITALK_API_KEY from your env variable llm = Maritalk(api_key="<API_KEY>", model="sabia-2-medium")

# Call chat with a list of messages messages = [ ChatMessage( role="system", content="You are an assistant specialized in suggesting pet names. Given the animal, you must suggest 4 names.", ), ChatMessage(role="user", content="I have a dog."), ]

# Sync chat response = llm.chat(messages) print(response)

# Async chat async def get_dog_name(llm, messages): response = await llm.achat(messages) print(response)

asyncio.run(get_dog_name(llm, messages)) ```
#### Stream Generation

For tasks involving the generation of long text, such as creating an extensive article or translating a large document, it can be advantageous to receive the response in parts, as the text is generated, instead of waiting for the complete text. This makes the application more responsive and efficient, especially when the generated text is extensive. We offer two approaches to meet this need: one synchronous and another asynchronous.

``` # Sync streaming chat response = llm.stream_chat(messages) for chunk in response: print(chunk.delta, end="", flush=True)

# Async streaming chat async def get_dog_name_streaming(llm, messages): async for chunk in await llm.astream_chat(messages): print(chunk.delta, end="", flush=True)

asyncio.run(get_dog_name_streaming(llm, messages)) ```
### Example 2 - Few-shot Examples with Complete
We recommend using the `llm.complete()` method when using the model with few-shot examples
``` prompt = """Classifique a resenha de filme como "positiva" ou "negativa".
Resenha: Gostei muito do filme, é o melhor do ano! Classe: positiva
Resenha: O filme deixa muito a desejar. Classe: negativa
Resenha: Apesar de longo, valeu o ingresso.. Classe:"""
# Sync complete response = llm.complete(prompt) print(response)

# Async complete async def classify_review(llm, prompt): response = await llm.acomplete(prompt) print(response)

asyncio.run(classify_review(llm, prompt)) ```
``` # Sync streaming complete response = llm.stream_complete(prompt) for chunk in response: print(chunk.delta, end="", flush=True)

# Async streaming complete async def classify_review_streaming(llm, prompt): async for chunk in await llm.astream_complete(prompt): print(chunk.delta, end="", flush=True)

asyncio.run(classify_review_streaming(llm, prompt)) ```

[1] https://www.maritaca.ai
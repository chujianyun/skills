# developers.llamaindex.ai/python/framework/integrations/embeddings/deepinfra/index.md
> https://developers.llamaindex.ai/python/framework/integrations/embeddings/deepinfra/index.md

--- title: DeepInfra | Developer Documentation ---

With this integration, you can use the DeepInfra embeddings model to get embeddings for your text data. Here is the link to the embeddings models [1].

First, you need to sign up on the DeepInfra website [2] and get the API token. You can copy `model_ids` from the model cards and start using them in your code.

### Installation
``` !pip install llama-index llama-index-embeddings-deepinfra ```
### Initialization
``` from dotenv import load_dotenv, find_dotenv from llama_index.embeddings.deepinfra import DeepInfraEmbeddingModel

_ = load_dotenv(find_dotenv())
model = DeepInfraEmbeddingModel( model_id="BAAI/bge-large-en-v1.5", # Use custom model ID api_token="YOUR_API_TOKEN", # Optionally provide token here normalize=True, # Optional normalization text_prefix="text: ", # Optional text prefix query_prefix="query: ", # Optional query prefix ) ```

### Synchronous Requests

``` response = model.get_text_embedding("hello world") print(response) ```

#### Batch Requests
``` texts = ["hello world", "goodbye world"] response_batch = model.get_text_embedding_batch(texts) print(response_batch) ```

#### Query Requests
``` query_response = model.get_query_embedding("hello world") print(query_response) ```

### Asynchronous Requests
#### Get Text Embedding
``` async def main(): text = "hello world" async_response = await model.aget_text_embedding(text) print(async_response)

if __name__ == "__main__": import asyncio
asyncio.run(main()) ```
---
For any questions or feedback, please contact us at <feedback@deepinfra.com>.

[1] https://deepinfra.com/models/embeddings
[2] https://deepinfra.com/
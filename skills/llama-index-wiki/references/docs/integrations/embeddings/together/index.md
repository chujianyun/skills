# developers.llamaindex.ai/python/framework/integrations/embeddings/together/index.md
> https://developers.llamaindex.ai/python/framework/integrations/embeddings/together/index.md

--- title: Together AI Embeddings | Developer Documentation ---

This notebook shows how to use `Together AI` for embeddings. Together AI provides access to many state-of-the-art embedding models.

Visit <https://together.ai> and sign up to get an API key.
## Setup
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.
``` %pip install llama-index-embeddings-together ```
``` !pip install llama-index ```
``` # You can set the API key in the embeddings or env # import os # os.environ["TOEGETHER_API_KEY"] = "your-api-key"

from llama_index.embeddings.together import TogetherEmbedding
embed_model = TogetherEmbedding( model_name="togethercomputer/m2-bert-80M-8k-retrieval", api_key="..." ) ```

## Get Embeddings
``` embeddings = embed_model.get_text_embedding("hello world") ```
``` print(len(embeddings)) ```
``` 768 ```
``` print(embeddings[:5]) ```
``` [-0.11657876, -0.012690996, 0.24342081, 0.32781482, 0.022501636] ```
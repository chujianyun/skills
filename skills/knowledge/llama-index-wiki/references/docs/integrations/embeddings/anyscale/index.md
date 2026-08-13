# developers.llamaindex.ai/python/framework/integrations/embeddings/anyscale/index.md
> https://developers.llamaindex.ai/python/framework/integrations/embeddings/anyscale/index.md

--- title: Anyscale Embeddings | Developer Documentation ---

This guide shows you how to use Anyscale Embeddings through Anyscale Endpoints [1].
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.
``` %pip install llama-index-embeddings-anyscale ```
``` !pip install llama-index ```
``` from llama_index.embeddings.anyscale import AnyscaleEmbedding
embed_model = AnyscaleEmbedding( api_key=ANYSCALE_ENDPOINT_TOKEN, embed_batch_size=10 ) ```

``` # Basic embedding example embeddings = embed_model.get_text_embedding( "It is raining cats and dogs here!" ) print(len(embeddings), embeddings[:10]) ```

[1] https://docs.endpoints.anyscale.com/
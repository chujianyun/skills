# developers.llamaindex.ai/python/framework/integrations/embeddings/fastembed/index.md
> https://developers.llamaindex.ai/python/framework/integrations/embeddings/fastembed/index.md

--- title: Qdrant FastEmbed Embeddings | Developer Documentation ---

LlamaIndex supports FastEmbed [1] for embeddings generation.
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.
``` %pip install llama-index-embeddings-fastembed ```
``` %pip install llama-index ```
To use this provider, the `fastembed` package needs to be installed.
``` %pip install fastembed ```
The list of supported models can be found here [2].
``` from llama_index.embeddings.fastembed import FastEmbedEmbedding
embed_model = FastEmbedEmbedding(model_name="BAAI/bge-small-en-v1.5") ```
``` 100%|██████████| 76.7M/76.7M [00:18<00:00, 4.23MiB/s] ```
``` embeddings = embed_model.get_text_embedding("Some text to embed.") print(len(embeddings)) print(embeddings[:5]) ```

``` 384 [-0.04166769981384277, 0.0018720313673838973, 0.02632238157093525, -0.036030545830726624, -0.014812108129262924] ```

[1] https://qdrant.github.io/fastembed/
[2] https://qdrant.github.io/fastembed/examples/Supported_Models/
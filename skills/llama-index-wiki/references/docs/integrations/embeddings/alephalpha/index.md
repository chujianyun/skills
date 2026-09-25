# developers.llamaindex.ai/python/framework/integrations/embeddings/alephalpha/index.md
> https://developers.llamaindex.ai/python/framework/integrations/embeddings/alephalpha/index.md

--- title: Aleph Alpha Embeddings | Developer Documentation ---
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.
``` %pip install llama-index-embeddings-alephalpha ```
``` !pip install llama-index ```
``` # Initialise with your AA token import os
os.environ["AA_TOKEN"] = "your_token_here" ```
#### With `luminous-base` embeddings.

- representation=“Document”: Use this for texts (documents) you want to store in your vector database - representation=“Query”: Use this for search queries to find the most relevant documents in your vector database - representation=“Symmetric”: Use this for clustering, classification, anomaly detection or visualisation tasks.

``` from llama_index.embeddings.alephalpha import AlephAlphaEmbedding
# To customize your token, do this # otherwise it will lookup AA_TOKEN from your env variable # embed_model = AlephAlpha(token="<aa_token>")
# with representation='query' embed_model = AlephAlphaEmbedding( model="luminous-base", representation="Query", )

``` representation_enum: SemanticRepresentation.Query

``` # with representation='Document' embed_model = AlephAlphaEmbedding( model="luminous-base", representation="Document", )
embeddings = embed_model.get_text_embedding("Hello Aleph Alpha!")
print(len(embeddings)) print(embeddings[:5]) ```
``` representation_enum: SemanticRepresentation.Document
5120 [0.14257812, 2.59375, 0.33203125, -0.33789062, -0.94140625] ```
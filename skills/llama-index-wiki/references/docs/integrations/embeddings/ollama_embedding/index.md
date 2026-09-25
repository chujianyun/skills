# developers.llamaindex.ai/python/framework/integrations/embeddings/ollama_embedding/index.md
> https://developers.llamaindex.ai/python/framework/integrations/embeddings/ollama_embedding/index.md

--- title: Ollama Embeddings | Developer Documentation ---
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.
``` %pip install llama-index-embeddings-ollama ```
``` from llama_index.embeddings.ollama import OllamaEmbedding
ollama_embedding = OllamaEmbedding( model_name="embeddinggemma", base_url="http://localhost:11434", # Can optionally pass additional kwargs to ollama # ollama_additional_kwargs={"mirostat": 0}, ) ```
You can generate embeddings using one of several methods:
- `get_text_embedding_batch` - `get_text_embedding` - `get_query_embedding`
As well as async versions:
- `aget_text_embedding_batch` - `aget_text_embedding` - `aget_query_embedding`
``` embeddings = ollama_embedding.get_text_embedding_batch( ["This is a passage!", "This is another passage"], show_progress=True ) print(f"Got vectors of length {len(embeddings[0])}") print(embeddings[0][:10]) ```
``` Generating embeddings: 100%|██████████| 2/2 [00:00<00:00, 3.66it/s]
Got vectors of length 768 [-0.19284482, -0.0048683924, 0.011490762, -0.035292886, 0.0018508184, 0.013227936, -0.045588765, 0.027076142, 0.03387062, -0.030585105] ```
``` embedding = ollama_embedding.get_text_embedding( "This is a piece of text!", ) print(f"Got vectors of length {len(embedding)}") print(embedding[:10]) ```
``` Got vectors of length 768 [-0.18305846, -0.009758809, 0.022796445, -0.038445882, -0.00894579, 0.023117013, -0.05166001, 0.037556227, 0.03699912, -0.017603736] ```
``` embedding = ollama_embedding.get_query_embedding( "This is a query!", ) print(f"Got vectors of length {len(embedding)}") print(embedding[:10]) ```
``` Got vectors of length 768 [-0.19484262, -0.014648143, 0.02743501, -0.015000358, 0.0027351314, 0.019096522, -0.071097225, 0.033618074, 0.05173764, -0.024861954] ```
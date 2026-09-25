# developers.llamaindex.ai/python/framework/integrations/vector_stores/hnswlibindexdemo/index.md
> https://developers.llamaindex.ai/python/framework/integrations/vector_stores/hnswlibindexdemo/index.md

--- title: Hnswlib | Developer Documentation ---

Hnswlib is a fast approximate nearest neighbor search index. It’s a lightweight, header-only C++ HNSW implementation that has no dependencies other than C++11. Hnswlib provides python bindings.

``` %pip install llama-index %pip install llama-index-vector-stores-hnswlib %pip install llama-index-embeddings-huggingface %pip install hnswlib ```

### Import package dependencies
``` from llama_index.vector_stores.hnswlib import HnswlibVectorStore from llama_index.core import ( VectorStoreIndex, StorageContext, SimpleDirectoryReader, ) from llama_index.embeddings.huggingface import HuggingFaceEmbedding ```

### Load example data

``` !mkdir -p 'data/paul_graham/' !wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt' ```

### Read the data
``` documents = SimpleDirectoryReader("./data/paul_graham/").load_data() print(f"Total documents: {len(documents)}") print(f"First document, id: {documents[0].doc_id}") print(f"First document, hash: {documents[0].hash}") print( "First document, text" f" ({len(documents[0].text)} characters):\n{'='*20}\n{documents[0].text[:360]} ..." ) ```

### Load the embedding model
``` embed_model = HuggingFaceEmbedding( model_name="sentence-transformers/all-MiniLM-L6-v2", normalize=True, ) ```

### Create Hnswlib Vector Store object from Hnswlib.Index parameters
``` hnswlib_vector_store = HnswlibVectorStore.from_params( space="ip", dimension=embed_model._model.get_sentence_embedding_dimension(), max_elements=1000, ) ```

Alternatively, You can create a Hnswlib.Index object Yourself.
``` import hnswlib
index = hnswlib.Index( "ip", embed_model._model.get_sentence_embedding_dimension() ) index.init_index(max_elements=1000)

hnswlib_vector_store = HnswlibVectorStore(index) ```
### Build index from documents
``` hnswlib_storage_context = StorageContext.from_defaults( vector_store=hnswlib_vector_store ) hnswlib_index = VectorStoreIndex.from_documents( documents, storage_context=hnswlib_storage_context, embed_model=embed_model, show_progress=True, ) ```

### Query index
``` k = 5 query = "Before college I wrote what begginers should write." hnswlib_vector_retriever = hnswlib_index.as_retriever(similarity_top_k=k) nodes_with_scores = nodes_with_scores = hnswlib_vector_retriever.retrieve( query ) for node in nodes_with_scores: print(f"Node {node.id_} | Score: {node.score:.3f} - {node.text[:120]}...") ```
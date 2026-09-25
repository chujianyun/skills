# developers.llamaindex.ai/python/framework/integrations/vector_stores/faissindexdemo/index.md
> https://developers.llamaindex.ai/python/framework/integrations/vector_stores/faissindexdemo/index.md

--- title: Faiss Vector Store | Developer Documentation ---

If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.
``` %pip install llama-index-vector-stores-faiss ```
``` !pip install llama-index ```
#### Creating a Faiss Index
``` import logging import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO) logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout)) ```
``` import faiss
# dimensions of text-ada-embedding-002 d = 1536 faiss_index = faiss.IndexFlatL2(d) ```

#### Load documents, build the VectorStoreIndex
``` from llama_index.core import ( SimpleDirectoryReader, load_index_from_storage, VectorStoreIndex, StorageContext, ) from llama_index.vector_stores.faiss import FaissVectorStore from IPython.display import Markdown, display ```

Download Data

``` !mkdir -p 'data/paul_graham/' !wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt' ```

``` # load documents documents = SimpleDirectoryReader("./data/paul_graham/").load_data() ```
``` vector_store = FaissVectorStore(faiss_index=faiss_index) storage_context = StorageContext.from_defaults(vector_store=vector_store) index = VectorStoreIndex.from_documents( documents, storage_context=storage_context ) ```
``` # save index to disk index.storage_context.persist() ```
``` # load index from disk vector_store = FaissVectorStore.from_persist_dir("./storage") storage_context = StorageContext.from_defaults( vector_store=vector_store, persist_dir="./storage" ) index = load_index_from_storage(storage_context=storage_context) ```
#### Query Index
``` # set Logging to DEBUG for more detailed outputs query_engine = index.as_query_engine() response = query_engine.query("What did the author do growing up?") ```

``` # set Logging to DEBUG for more detailed outputs query_engine = index.as_query_engine() response = query_engine.query( "What did the author do after his time at Y Combinator?" ) ```
``` display(Markdown(f"<b>{response}</b>")) ```
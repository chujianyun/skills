# developers.llamaindex.ai/python/framework/integrations/vector_stores/weaviateindexdemo-hybrid/index.md
> https://developers.llamaindex.ai/python/framework/integrations/vector_stores/weaviateindexdemo-hybrid/index.md

--- title: Weaviate Vector Store - Hybrid Search | Developer Documentation ---
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.
``` %pip install llama-index-vector-stores-weaviate ```
``` !pip install llama-index ```
``` import logging import sys
logging.basicConfig(stream=sys.stdout, level=logging.INFO) logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout)) ```
## Creating a Weaviate Client
``` import os import openai
os.environ["OPENAI_API_KEY"] = "" openai.api_key = os.environ["OPENAI_API_KEY"] ```
``` import weaviate ```
``` # Connect to cloud instance cluster_url = "" api_key = ""
client = weaviate.connect_to_wcs( cluster_url=cluster_url, auth_credentials=weaviate.auth.AuthApiKey(api_key), )
# Connect to local instance # client = weaviate.connect_to_local() ```
``` from llama_index.core import VectorStoreIndex, SimpleDirectoryReader from llama_index.vector_stores.weaviate import WeaviateVectorStore from llama_index.core.response.notebook_utils import display_response ```
## Download Data

``` !mkdir -p 'data/paul_graham/' !wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt' ```

## Load documents
``` # load documents documents = SimpleDirectoryReader("./data/paul_graham/").load_data() ```

## Build the VectorStoreIndex with WeaviateVectorStore
``` from llama_index.core import StorageContext

vector_store = WeaviateVectorStore(weaviate_client=client) storage_context = StorageContext.from_defaults(vector_store=vector_store) index = VectorStoreIndex.from_documents( documents, storage_context=storage_context )

# NOTE: you may also choose to define a index_name manually. # index_name = "test_prefix" # vector_store = WeaviateVectorStore(weaviate_client=client, index_name=index_name) ```

## Query Index with Default Vector Search
``` # set Logging to DEBUG for more detailed outputs query_engine = index.as_query_engine(similarity_top_k=2) response = query_engine.query("What did the author do growing up?") ```

## Query Index with Hybrid Search
Use hybrid search with bm25 and vector.\ `alpha` parameter determines weighting (alpha = 0 -> bm25, alpha=1 -> vector search).
### By default, `alpha=0.75` is used (very similar to vector search)
``` # set Logging to DEBUG for more detailed outputs query_engine = index.as_query_engine( vector_store_query_mode="hybrid", similarity_top_k=2 ) response = query_engine.query( "What did the author do growing up?", ) ```

### Set `alpha=0.` to favor bm25
``` # set Logging to DEBUG for more detailed outputs query_engine = index.as_query_engine( vector_store_query_mode="hybrid", similarity_top_k=2, alpha=0.0 ) response = query_engine.query( "What did the author do growing up?", ) ```

``` display_response(response) ```
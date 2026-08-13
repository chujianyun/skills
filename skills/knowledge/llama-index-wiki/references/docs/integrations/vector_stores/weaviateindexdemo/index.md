# developers.llamaindex.ai/python/framework/integrations/vector_stores/weaviateindexdemo/index.md
> https://developers.llamaindex.ai/python/framework/integrations/vector_stores/weaviateindexdemo/index.md

--- title: Weaviate Vector Store | Developer Documentation ---
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.
``` %pip install llama-index-vector-stores-weaviate ```
``` !pip install llama-index ```
#### Creating a Weaviate Client
``` import os import openai
os.environ["OPENAI_API_KEY"] = "" openai.api_key = os.environ["OPENAI_API_KEY"] ```
``` import logging import sys
logging.basicConfig(stream=sys.stdout, level=logging.INFO) logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout)) ```
``` import weaviate ```
``` # cloud cluster_url = "" api_key = ""

# local # client = connect_to_local() ```
#### Load documents, build the VectorStoreIndex
``` from llama_index.core import VectorStoreIndex, SimpleDirectoryReader from llama_index.vector_stores.weaviate import WeaviateVectorStore from IPython.display import Markdown, display ```

Download Data

``` !mkdir -p 'data/paul_graham/' !wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt' ```

``` # load documents documents = SimpleDirectoryReader("./data/paul_graham").load_data() ```
``` from llama_index.core import StorageContext
# If you want to load the index later, be sure to give it a name! vector_store = WeaviateVectorStore( weaviate_client=client, index_name="LlamaIndex" ) storage_context = StorageContext.from_defaults(vector_store=vector_store) index = VectorStoreIndex.from_documents( documents, storage_context=storage_context )
# NOTE: you may also choose to define a index_name manually. # index_name = "test_prefix" # vector_store = WeaviateVectorStore(weaviate_client=client, index_name=index_name) ```
#### Using a custom batch configuration

Llamaindex defaults to Weaviate’s dynamic batching, optimized for most common scenarios. However, in low-latency setups, this can overload the server or max out any GRPC Message limits in place. For more control and a better ingestion process, consider adjusting batch size by using the fixed size batch.

Here is how you can fine tune WeaviateVectorStore and define a custom batch:
``` from weaviate.classes.config import ConsistencyLevel
custom_batch = client.batch.fixed_size( batch_size=123, concurrent_requests=3, consistency_level=ConsistencyLevel.ALL, ) vector_store_fixed = WeaviateVectorStore( weaviate_client=client, index_name="LlamaIndex", # we pass our custom batch as a client_kwargs client_kwargs={"custom_batch": custom_batch}, ) ```

#### Query Index
``` # set Logging to DEBUG for more detailed outputs query_engine = index.as_query_engine() response = query_engine.query("What did the author do growing up?") ```

``` display(Markdown(f"<b>{response}</b>")) ```
## Loading the index

Here, we use the same index name as when we created the initial index. This stops it from being auto-generated and allows us to easily connect back to it.

``` cluster_url = "" api_key = ""

client = weaviate.connect_to_wcs( cluster_url=cluster_url, auth_credentials=weaviate.auth.AuthApiKey(api_key), )

# local # client = weaviate.connect_to_local() ```
``` vector_store = WeaviateVectorStore( weaviate_client=client, index_name="LlamaIndex" )

loaded_index = VectorStoreIndex.from_vector_store(vector_store) ```
``` # set Logging to DEBUG for more detailed outputs query_engine = loaded_index.as_query_engine() response = query_engine.query("What happened at interleaf?") display(Markdown(f"<b>{response}</b>")) ```

## Metadata Filtering
Let’s insert a dummy document, and try to filter so that only that document is returned.
``` from llama_index.core import Document
doc = Document.example() print(doc.metadata) print("-----") print(doc.text[:100]) ```

``` loaded_index.insert(doc) ```
``` from llama_index.core.vector_stores import ExactMatchFilter, MetadataFilters
filters = MetadataFilters( filters=[ExactMatchFilter(key="filename", value="README.md")] ) query_engine = loaded_index.as_query_engine(filters=filters) response = query_engine.query("What is the name of the file?") display(Markdown(f"<b>{response}</b>")) ```

# Deleting the index completely
You can delete the index created by the vector store using the `delete_index` function
``` vector_store.delete_index() ```
``` vector_store.delete_index() # calling the function again does nothing ```
# Connection Termination
You must ensure your client connections are closed:
``` client.close() ```
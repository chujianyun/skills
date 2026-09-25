# developers.llamaindex.ai/python/framework/integrations/vector_stores/pineconeindexdemo/index.md
> https://developers.llamaindex.ai/python/framework/integrations/vector_stores/pineconeindexdemo/index.md

--- title: Pinecone Vector Store | Developer Documentation ---
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.
``` %pip install llama-index llama-index-vector-stores-pinecone ```
``` import logging import sys import os
logging.basicConfig(stream=sys.stdout, level=logging.INFO) logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout)) ```
#### Creating a Pinecone Index
``` from pinecone import Pinecone, ServerlessSpec ```
``` os.environ["PINECONE_API_KEY"] = "..." os.environ["OPENAI_API_KEY"] = "sk-proj-..."
api_key = os.environ["PINECONE_API_KEY"]
pc = Pinecone(api_key=api_key) ```
``` # delete if needed # pc.delete_index("quickstart") ```
``` # dimensions are for text-embedding-ada-002
pc.create_index( name="quickstart", dimension=1536, metric="euclidean", spec=ServerlessSpec(cloud="aws", region="us-east-1"), )

# If you need to create a PodBased Pinecone index, you could alternatively do this: # # from pinecone import Pinecone, PodSpec # # pc = Pinecone(api_key='xxx') # # pc.create_index( # name='my-index', # dimension=1536, # metric='cosine', # spec=PodSpec( # environment='us-east1-gcp', # pod_type='p1.x1', # pods=1 # ) # ) # ```

``` pinecone_index = pc.Index("quickstart") ```
#### Load documents, build the PineconeVectorStore and VectorStoreIndex
``` from llama_index.core import VectorStoreIndex, SimpleDirectoryReader from llama_index.vector_stores.pinecone import PineconeVectorStore from IPython.display import Markdown, display ```
Download Data

``` !mkdir -p 'data/paul_graham/' !wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt' ```

``` # load documents documents = SimpleDirectoryReader("./data/paul_graham").load_data() ```
``` # initialize without metadata filter from llama_index.core import StorageContext
if "OPENAI_API_KEY" not in os.environ: raise EnvironmentError(f"Environment variable OPENAI_API_KEY is not set")
vector_store = PineconeVectorStore(pinecone_index=pinecone_index) storage_context = StorageContext.from_defaults(vector_store=vector_store) index = VectorStoreIndex.from_documents( documents, storage_context=storage_context ) ```
#### Query Index
May take a minute or so for the index to be ready!
``` # set Logging to DEBUG for more detailed outputs query_engine = index.as_query_engine() response = query_engine.query("What did the author do growing up?") ```
``` INFO:httpx:HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK" HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK" INFO:httpx:HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK" HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK" ```
``` display(Markdown(f"<b>{response}</b>")) ```

**The author, growing up, worked on writing and programming. They wrote short stories and tried writing programs on an IBM 1401 computer. They later got a microcomputer and started programming more extensively, writing simple games and a word processor.**

## Filtering
You can also fetch a list of nodes directly with filters.
``` from llama_index.core.vector_stores.types import ( MetadataFilter, MetadataFilters, FilterOperator, FilterCondition, )

filter = MetadataFilters( filters=[ MetadataFilter( key="file_path", value="/Users/loganmarkewich/giant_change/llama_index/docs/examples/vector_stores/data/paul_graham/paul_graham_essay.txt", operator=FilterOperator.EQ, ) ], condition=FilterCondition.AND, ) ```

You can fetch nodes directly with the filters. The below will return all nodes that match the filter.
``` nodes = vector_store.get_nodes(filters=filter, limit=100) print(len(nodes)) ```

``` 22 ```
You can also fetch using top-k and filters.
``` query_engine = index.as_query_engine(similarity_top_k=2, filters=filter) response = query_engine.query("What did the author do growing up?") print(len(response.source_nodes)) ```

``` INFO:httpx:HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK" HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK" INFO:httpx:HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK" HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK" 2 ```
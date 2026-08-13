# developers.llamaindex.ai/python/framework/integrations/vector_stores/qdrantindexdemo/index.md
> https://developers.llamaindex.ai/python/framework/integrations/vector_stores/qdrantindexdemo/index.md

--- title: Qdrant Vector Store | Developer Documentation ---

#### Creating a Qdrant client
``` %pip install llama-index-vector-stores-qdrant llama-index-readers-file llama-index-embeddings-fastembed llama-index-llms-openai ```
``` import logging import sys import os

import qdrant_client from IPython.display import Markdown, display from llama_index.core import VectorStoreIndex, SimpleDirectoryReader from llama_index.core import StorageContext from llama_index.vector_stores.qdrant import QdrantVectorStore from llama_index.embeddings.fastembed import FastEmbedEmbedding from llama_index.core import Settings

Settings.embed_model = FastEmbedEmbedding(model_name="BAAI/bge-base-en-v1.5") ```
If running for the first, time, install the dependencies using:
``` !pip install -U qdrant_client fastembed ```
Set your OpenAI key for authenticating the LLM
Follow these set the OpenAI API key to the OPENAI\_API\_KEY environment variable -
1. Using Terminal
``` export OPENAI_API_KEY=your_api_key_here ```
2. Using IPython Magic Command in Jupyter Notebook
``` %env OPENAI_API_KEY=<YOUR_OPENAI_API_KEY> ```
3. Using Python Script
``` import os
os.environ["OPENAI_API_KEY"] = "your_api_key_here" ```
Note: It’s generally recommended to set sensitive information like API keys as environment variables rather than hardcoding them into scripts.
``` logging.basicConfig(stream=sys.stdout, level=logging.INFO) logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout)) ```

Download Data

``` !mkdir -p 'data/paul_graham/' !wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt' ```

#### Load the documents
``` # load documents documents = SimpleDirectoryReader("./data/paul_graham/").load_data() ```

#### Build the VectorStoreIndex
``` client = qdrant_client.QdrantClient( # you can use :memory: mode for fast and light-weight experiments, # it does not require to have Qdrant deployed anywhere # but requires qdrant-client >= 1.1.1 # location=":memory:" # otherwise set Qdrant instance address with: # url="http://<host>:<port>" # otherwise set Qdrant instance with host and port: host="localhost", port=6333 # set API KEY for Qdrant Cloud # api_key="<API_KEY>", ) ```

``` vector_store = QdrantVectorStore(client=client, collection_name="paul_graham") storage_context = StorageContext.from_defaults(vector_store=vector_store) index = VectorStoreIndex.from_documents( documents, storage_context=storage_context, ) ```

#### Query Index
``` # set Logging to DEBUG for more detailed outputs query_engine = index.as_query_engine() response = query_engine.query("What did the author do growing up?") ```

**The author worked on writing and programming before college.**
``` # set Logging to DEBUG for more detailed outputs query_engine = index.as_query_engine() response = query_engine.query( "What did the author do after his time at Viaweb?" ) ```

**The author arranged to do freelance work for a group that did projects for customers after his time at Viaweb.**
#### Build the VectorStoreIndex asynchronously
``` # To connect to the same event-loop, # allows async events to run on notebook

import nest_asyncio
nest_asyncio.apply() ```
``` aclient = qdrant_client.AsyncQdrantClient( # you can use :memory: mode for fast and light-weight experiments, # it does not require to have Qdrant deployed anywhere # but requires qdrant-client >= 1.1.1 location=":memory:" # otherwise set Qdrant instance address with: # uri="http://<host>:<port>" # set API KEY for Qdrant Cloud # api_key="<API_KEY>", ) ```

``` vector_store = QdrantVectorStore( collection_name="paul_graham", client=client, aclient=aclient, prefer_grpc=True, ) storage_context = StorageContext.from_defaults(vector_store=vector_store) index = VectorStoreIndex.from_documents( documents, storage_context=storage_context, use_async=True, ) ```

#### Async Query Index
``` query_engine = index.as_query_engine(use_async=True) response = await query_engine.aquery("What did the author do growing up?") ```

**The author worked on writing short stories and programming, particularly on an IBM 1401 computer in 9th grade using an early version of Fortran. Later, the author transitioned to working on microcomputers, starting with a TRS-80 in about 1980, where they wrote simple games, programs, and a word processor.**

``` # set Logging to DEBUG for more detailed outputs query_engine = index.as_query_engine(use_async=True) response = await query_engine.aquery( "What did the author do after his time at Viaweb?" ) ```

``` display(Markdown(f"<b>{response}</b>")) ```
**The author went on to co-found Y Combinator after his time at Viaweb.**
## Hybrid Search

You can enable hybrid search when creating an qdrant index. Here, we use Qdrant’s BM25 capabilities to quickly create a sparse and dense index for hybrid retrieval.

``` from qdrant_client import QdrantClient, AsyncQdrantClient from llama_index.core import VectorStoreIndex from llama_index.core import StorageContext from llama_index.vector_stores.qdrant import QdrantVectorStore
client = QdrantClient(host="localhost", port=6333) aclient = AsyncQdrantClient(host="localhost", port=6333)
vector_store = QdrantVectorStore( client=client, aclient=aclient, collection_name="paul_graham_hybrid", enable_hybrid=True, fastembed_sparse_model="Qdrant/bm25", )

index = VectorStoreIndex.from_documents( documents, storage_context=StorageContext.from_defaults(vector_store=vector_store), )
# retrieve 2 sparse, 2 dense, and filter down to 3 total hybrid results query_engine = index.as_query_engine( vector_store_query_mode="hybrid", sparse_top_k=2, similarity_top_k=2, hybrid_top_k=3, )

response = query_engine.query("What did the author do growing up?") display(Markdown(f"<b>{response}</b>")) ```
## Saving and Loading
To restore an index, in most cases, you can just restore using the vector store object itself. The index is saved automatically by Qdrant.
``` loaded_index = VectorStoreIndex.from_vector_store( vector_store, # Embedding model should match the original embedding model # embed_model=Settings.embed_model ) ```
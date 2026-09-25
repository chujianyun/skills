# developers.llamaindex.ai/python/framework/integrations/retrievers/simple_fusion/index.md
> https://developers.llamaindex.ai/python/framework/integrations/retrievers/simple_fusion/index.md

--- title: Simple Fusion Retriever | Developer Documentation ---

In this example, we walk through how you can combine retrieval results from multiple queries and multiple indexes.
The retrieved nodes will be returned as the top-k across all queries and indexes, as well as handling de-duplication of any nodes.
``` import os import openai

os.environ["OPENAI_API_KEY"] = "sk-..." openai.api_key = os.environ["OPENAI_API_KEY"] ```
## Setup
For this notebook, we will use two very similar pages of our documentation, each stored in a separaete index.
``` from llama_index.core import SimpleDirectoryReader
documents_1 = SimpleDirectoryReader( input_files=["../../community/integrations/vector_stores.md"] ).load_data() documents_2 = SimpleDirectoryReader( input_files=["../../module_guides/storing/vector_stores.md"] ).load_data() ```

``` from llama_index.core import VectorStoreIndex
index_1 = VectorStoreIndex.from_documents(documents_1) index_2 = VectorStoreIndex.from_documents(documents_2) ```
## Fuse the Indexes!

In this step, we fuse our indexes into a single retriever. This retriever will also generate augment our query by generating extra queries related to the original question, and aggregate the results.

This setup will query 4 times, once with your original query, and generate 3 more queries.
By default, it uses the following prompt to generate extra queries:
``` QUERY_GEN_PROMPT = ( "You are a helpful assistant that generates multiple search queries based on a " "single input query. Generate {num_queries} search queries, one on each line, " "related to the following input query:\n" "Query: {query}\n" "Queries:\n" ) ```

``` from llama_index.core.retrievers import QueryFusionRetriever
retriever = QueryFusionRetriever( [index_1.as_retriever(), index_2.as_retriever()], similarity_top_k=2, num_queries=4, # set this to 1 to disable query generation use_async=True, verbose=True, # query_gen_prompt="...", # we could override the query generation prompt here ) ```

``` # apply nested async to run in a notebook import nest_asyncio

nest_asyncio.apply() ```
``` nodes_with_scores = retriever.retrieve("How do I setup a chroma vector store?") ```
``` Generated queries: 1. What are the steps to set up a chroma vector store? 2. Best practices for configuring a chroma vector store 3. Troubleshooting common issues when setting up a chroma vector store ```

``` for node in nodes_with_scores: print(f"Score: {node.score:.2f} - {node.text[:100]}...") ```

``` Score: 0.78 - # Vector Stores
Vector stores contain embedding vectors of ingested document chunks (and sometimes ... Score: 0.78 - # Using Vector Stores

LlamaIndex offers multiple integration points with vector stores / vector dat... ```
## Use in a Query Engine!
Now, we can plug our retriever into a query engine to synthesize natural language responses.
``` from llama_index.core.query_engine import RetrieverQueryEngine
query_engine = RetrieverQueryEngine.from_args(retriever) ```
``` response = query_engine.query( "How do I setup a chroma vector store? Can you give an example?" ) ```

``` Generated queries: 1. How to set up a chroma vector store? 2. Step-by-step guide for creating a chroma vector store. 3. Examples of chroma vector store setups and configurations. ```

``` from llama_index.core.response.notebook_utils import display_response
display_response(response) ```
**`Final Response:`** To set up a Chroma vector store, you need to follow these steps:
1. Import the necessary libraries:
``` import chromadb from llama_index.vector_stores.chroma import ChromaVectorStore ```

2. Create a Chroma client:
``` chroma_client = chromadb.EphemeralClient() chroma_collection = chroma_client.create_collection("quickstart") ```

3. Construct the vector store:
``` vector_store = ChromaVectorStore(chroma_collection=chroma_collection) ```
Here’s an example of how to set up a Chroma vector store using the above steps:
``` import chromadb from llama_index.vector_stores.chroma import ChromaVectorStore

# Creating a Chroma client # EphemeralClient operates purely in-memory, PersistentClient will also save to disk chroma_client = chromadb.EphemeralClient() chroma_collection = chroma_client.create_collection("quickstart")

# construct vector store vector_store = ChromaVectorStore(chroma_collection=chroma_collection) ```

This example demonstrates how to create a Chroma client, create a collection named “quickstart”, and then construct a Chroma vector store using that collection.
# developers.llamaindex.ai/python/framework/integrations/vector_stores/elasticsearch_auto_retriever/index.md
> https://developers.llamaindex.ai/python/framework/integrations/vector_stores/elasticsearch_auto_retriever/index.md

--- title: Auto-Retrieval from a Vector Database | Developer Documentation ---

This guide shows how to perform **auto-retrieval** in LlamaIndex.
Many popular vector dbs support a set of metadata filters in addition to a query string for semantic search. Given a natural language query, we first use the LLM to infer a set of metadata filters as well as the right query string to pass to the vector db (either can also be blank). This overall query bundle is then executed against the vector db.
This allows for more dynamic, expressive forms of retrieval beyond top-k semantic search. The relevant context for a given query may only require filtering on a metadata tag, or require a joint combination of filtering + semantic search within the filtered set, or just raw semantic search.
We demonstrate an example with Elasticsearch, but auto-retrieval is also implemented with many other vector dbs (e.g. Pinecone, Weaviate, and more).
## Setup
We first define imports.
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.
``` %pip install llama-index-vector-stores-elasticsearch ```
``` !pip install llama-index ```
``` import logging import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO) logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout)) ```
``` # set up OpenAI import os import getpass

os.environ["OPENAI_API_KEY"] = getpass.getpass("OpenAI API Key:") import openai
openai.api_key = os.environ["OPENAI_API_KEY"] ```
## Defining Some Sample Data
We insert some sample nodes containing text chunks into the vector database. Note that each `TextNode` not only contains the text, but also metadata e.g. `category` and `country`. These metadata fields will get converted/stored as such in the underlying vector db.
``` from llama_index.core import VectorStoreIndex, StorageContext from llama_index.vector_stores.elasticsearch import ElasticsearchStore ```

``` from llama_index.core.schema import TextNode
nodes = [ TextNode( text=( "A bunch of scientists bring back dinosaurs and mayhem breaks" " loose" ), metadata={"year": 1993, "rating": 7.7, "genre": "science fiction"}, ), TextNode( text=( "Leo DiCaprio gets lost in a dream within a dream within a dream" " within a ..." ), metadata={ "year": 2010, "director": "Christopher Nolan", "rating": 8.2, }, ), TextNode( text=( "A psychologist / detective gets lost in a series of dreams within" " dreams within dreams and Inception reused the idea" ), metadata={"year": 2006, "director": "Satoshi Kon", "rating": 8.6}, ), TextNode( text=( "A bunch of normal-sized women are supremely wholesome and some" " men pine after them" ), metadata={"year": 2019, "director": "Greta Gerwig", "rating": 8.3}, ), TextNode( text="Toys come alive and have a blast doing so", metadata={"year": 1995, "genre": "animated"}, ), ] ```

## Build Vector Index with Elasticsearch Vector Store
Here we load the data into the vector store. As mentioned above, both the text and metadata for each node will get converted into corresponding representation in Elasticsearch. We can now run semantic queries and also metadata filtering on this data from Elasticsearch.
``` vector_store = ElasticsearchStore( index_name="auto_retriever_movies", es_url="http://localhost:9200" ) storage_context = StorageContext.from_defaults(vector_store=vector_store) ```

``` index = VectorStoreIndex(nodes, storage_context=storage_context) ```
## Define `VectorIndexAutoRetriever`
We define our core `VectorIndexAutoRetriever` module. The module takes in `VectorStoreInfo`, which contains a structured description of the vector store collection and the metadata filters it supports. This information will then be used in the auto-retrieval prompt where the LLM infers metadata filters.
``` from llama_index.core.retrievers import VectorIndexAutoRetriever from llama_index.core.vector_stores import MetadataInfo, VectorStoreInfo

vector_store_info = VectorStoreInfo( content_info="Brief summary of a movie", metadata_info=[ MetadataInfo( name="genre", description="The genre of the movie", type="string or list[string]", ), MetadataInfo( name="year", description="The year the movie was released", type="integer", ), MetadataInfo( name="director", description="The name of the movie director", type="string", ), MetadataInfo( name="rating", description="A 1-10 rating for the movie", type="float", ), ], ) retriever = VectorIndexAutoRetriever( index, vector_store_info=vector_store_info ) ```

## Running over some sample data
We try running over some sample data. Note how metadata filters are inferred - this helps with more precise retrieval!
``` retriever.retrieve( "What are 2 movies by Christopher Nolan were made before 2020?" ) ```

``` retriever.retrieve("Has Andrei Tarkovsky directed any science fiction movies") ```
``` INFO:llama_index.indices.vector_store.retrievers.auto_retriever.auto_retriever:Using query str: science fiction Using query str: science fiction INFO:llama_index.indices.vector_store.retrievers.auto_retriever.auto_retriever:Using filters: {'director': 'Andrei Tarkovsky'} Using filters: {'director': 'Andrei Tarkovsky'} INFO:llama_index.indices.vector_store.retrievers.auto_retriever.auto_retriever:Using top_k: 2 Using top_k: 2 INFO:elastic_transport.transport:POST http://localhost:9200/auto_retriever_movies/_search [status:200 duration:0.042s] POST http://localhost:9200/auto_retriever_movies/_search [status:200 duration:0.042s]

[] ```
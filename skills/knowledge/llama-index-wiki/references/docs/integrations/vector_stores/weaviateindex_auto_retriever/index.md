# developers.llamaindex.ai/python/framework/integrations/vector_stores/weaviateindex_auto_retriever/index.md
> https://developers.llamaindex.ai/python/framework/integrations/vector_stores/weaviateindex_auto_retriever/index.md

--- title: Auto-Retrieval from a Weaviate Vector Database | Developer Documentation ---

This guide shows how to perform **auto-retrieval** in LlamaIndex with Weaviate [1].
The Weaviate vector database supports a set of metadata filters [2] in addition to a query string for semantic search. Given a natural language query, we first use a Large Language Model (LLM) to infer a set of metadata filters as well as the right query string to pass to the vector database (either can also be blank). This overall query bundle is then executed against the vector database.
This allows for more dynamic, expressive forms of retrieval beyond top-k semantic search. The relevant context for a given query may only require filtering on a metadata tag, or require a joint combination of filtering + semantic search within the filtered set, or just raw semantic search.
## Setup
We first define imports and define an empty Weaviate collection.
If you’re opening this Notebook on Colab, you will probably need to install LlamaIndex 🦙.
``` %pip install llama-index-vector-stores-weaviate ```
``` !pip install llama-index weaviate-client ```
``` import logging import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO) logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout)) ```
We will be using GPT-4 for its reasoning capabilities to infer the metadata filters. Depending on your use case, `"gpt-3.5-turbo"` can work as well.
``` # set up OpenAI import os import getpass import openai

os.environ["OPENAI_API_KEY"] = getpass.getpass("OpenAI API Key:") openai.api_key = os.environ["OPENAI_API_KEY"] ```
``` from llama_index.embeddings.openai import OpenAIEmbedding from llama_index.llms.openai import OpenAI from llama_index.core.settings import Settings

Settings.llm = OpenAI(model="gpt-4") Settings.embed_model = OpenAIEmbedding() ```
This Notebook uses Weaviate in Embedded mode [3], which is supported on Linux and macOS.
If you prefer to try out Weaviate’s fully managed service, Weaviate Cloud Services (WCS) [4], you can enable the code in the comments.
``` import weaviate from weaviate.embedded import EmbeddedOptions

# Connect to Weaviate client in embedded mode client = weaviate.connect_to_embedded()
# Enable this code if you want to use Weaviate Cloud Services instead of Embedded mode. """ import weaviate

# cloud cluster_url = "" api_key = ""

client = weaviate.connect_to_wcs(cluster_url=cluster_url, auth_credentials=weaviate.auth.AuthApiKey(api_key), )

# local # client = weaviate.connect_to_local() """ ```

## Defining Some Sample Data
We insert some sample nodes containing text chunks into the vector database. Note that each `TextNode` not only contains the text, but also metadata e.g. `category` and `country`. These metadata fields will get converted/stored as such in the underlying vector db.
``` from llama_index.core.schema import TextNode
nodes = [ TextNode( text=( "Michael Jordan is a retired professional basketball player," " widely regarded as one of the greatest basketball players of all" " time." ), metadata={ "category": "Sports", "country": "United States", }, ), TextNode( text=( "Angelina Jolie is an American actress, filmmaker, and" " humanitarian. She has received numerous awards for her acting" " and is known for her philanthropic work." ), metadata={ "category": "Entertainment", "country": "United States", }, ), TextNode( text=( "Elon Musk is a business magnate, industrial designer, and" " engineer. He is the founder, CEO, and lead designer of SpaceX," " Tesla, Inc., Neuralink, and The Boring Company." ), metadata={ "category": "Business", "country": "United States", }, ), TextNode( text=( "Rihanna is a Barbadian singer, actress, and businesswoman. She" " has achieved significant success in the music industry and is" " known for her versatile musical style."

), metadata={ "category": "Music", "country": "Barbados", }, ), TextNode( text=( "Cristiano Ronaldo is a Portuguese professional footballer who is" " considered one of the greatest football players of all time. He" " has won numerous awards and set multiple records during his" " career." ), metadata={ "category": "Sports", "country": "Portugal", }, ), ] ```

## Build Vector Index with Weaviate Vector Store
Here we load the data into the vector store. As mentioned above, both the text and metadata for each node will get converted into corresponding representations in Weaviate. We can now run semantic queries and also metadata filtering on this data from Weaviate.
``` from llama_index.core import VectorStoreIndex, StorageContext from llama_index.vector_stores.weaviate import WeaviateVectorStore

vector_store = WeaviateVectorStore( weaviate_client=client, index_name="LlamaIndex_filter" )

storage_context = StorageContext.from_defaults(vector_store=vector_store) ```
``` index = VectorStoreIndex(nodes, storage_context=storage_context) ```
## Define `VectorIndexAutoRetriever`
We define our core `VectorIndexAutoRetriever` module. The module takes in `VectorStoreInfo`, which contains a structured description of the vector store collection and the metadata filters it supports. This information will then be used in the auto-retrieval prompt where the LLM infers metadata filters.
``` from llama_index.core.retrievers import VectorIndexAutoRetriever from llama_index.core.vector_stores.types import MetadataInfo, VectorStoreInfo

vector_store_info = VectorStoreInfo( content_info="brief biography of celebrities", metadata_info=[ MetadataInfo( name="category", type="str", description=( "Category of the celebrity, one of [Sports, Entertainment," " Business, Music]" ), ), MetadataInfo( name="country", type="str", description=( "Country of the celebrity, one of [United States, Barbados," " Portugal]" ), ), ], )

retriever = VectorIndexAutoRetriever( index, vector_store_info=vector_store_info ) ```

## Running over some sample data
We try running over some sample data. Note how metadata filters are inferred - this helps with more precise retrieval!
``` response = retriever.retrieve("Tell me about celebrities from United States") ```

``` response = retriever.retrieve( "Tell me about Sports celebrities from United States" ) ```
``` print(response[0]) ```

[1] https://weaviate.io/
[2] https://weaviate.io/developers/weaviate/search/filters
[3] https://weaviate.io/developers/weaviate/installation/embedded
[4] https://weaviate.io/developers/weaviate/installation/weaviate-cloud-services
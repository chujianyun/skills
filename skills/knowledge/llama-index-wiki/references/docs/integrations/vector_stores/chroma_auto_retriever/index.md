# developers.llamaindex.ai/python/framework/integrations/vector_stores/chroma_auto_retriever/index.md
> https://developers.llamaindex.ai/python/framework/integrations/vector_stores/chroma_auto_retriever/index.md

--- title: Auto-Retrieval from a Vector Database | Developer Documentation ---

This guide shows how to perform **auto-retrieval** in LlamaIndex.
Many popular vector dbs support a set of metadata filters in addition to a query string for semantic search. Given a natural language query, we first use the LLM to infer a set of metadata filters as well as the right query string to pass to the vector db (either can also be blank). This overall query bundle is then executed against the vector db.
This allows for more dynamic, expressive forms of retrieval beyond top-k semantic search. The relevant context for a given query may only require filtering on a metadata tag, or require a joint combination of filtering + semantic search within the filtered set, or just raw semantic search.
We demonstrate an example with Chroma, but auto-retrieval is also implemented with many other vector dbs (e.g. Pinecone, Weaviate, and more).
## Setup
We first define imports and define an empty Chroma collection.
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.
``` %pip install llama-index-vector-stores-chroma ```
``` !pip install llama-index ```
``` import logging import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO) logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout)) ```
``` # set up OpenAI import os import getpass

os.environ["OPENAI_API_KEY"] = getpass.getpass("OpenAI API Key:") import openai
openai.api_key = os.environ["OPENAI_API_KEY"] ```
``` import chromadb ```
``` chroma_client = chromadb.EphemeralClient() chroma_collection = chroma_client.create_collection("quickstart") ```

``` INFO:chromadb.telemetry.posthog:Anonymized telemetry enabled. See https://docs.trychroma.com/telemetry for more information. Anonymized telemetry enabled. See https://docs.trychroma.com/telemetry for more information. ```

## Defining Some Sample Data
We insert some sample nodes containing text chunks into the vector database. Note that each `TextNode` not only contains the text, but also metadata e.g. `category` and `country`. These metadata fields will get converted/stored as such in the underlying vector db.
``` from llama_index.core import VectorStoreIndex, StorageContext from llama_index.vector_stores.chroma import ChromaVectorStore ```

``` from llama_index.core.schema import TextNode
nodes = [ TextNode( text=( "Michael Jordan is a retired professional basketball player," " widely regarded as one of the greatest basketball players of all" " time." ), metadata={ "category": "Sports", "country": "United States", }, ), TextNode( text=( "Angelina Jolie is an American actress, filmmaker, and" " humanitarian. She has received numerous awards for her acting" " and is known for her philanthropic work." ), metadata={ "category": "Entertainment", "country": "United States", }, ), TextNode( text=( "Elon Musk is a business magnate, industrial designer, and" " engineer. He is the founder, CEO, and lead designer of SpaceX," " Tesla, Inc., Neuralink, and The Boring Company." ), metadata={ "category": "Business", "country": "United States", }, ), TextNode( text=( "Rihanna is a Barbadian singer, actress, and businesswoman. She" " has achieved significant success in the music industry and is" " known for her versatile musical style."

), metadata={ "category": "Music", "country": "Barbados", }, ), TextNode( text=( "Cristiano Ronaldo is a Portuguese professional footballer who is" " considered one of the greatest football players of all time. He" " has won numerous awards and set multiple records during his" " career." ), metadata={ "category": "Sports", "country": "Portugal", }, ), ] ```

## Build Vector Index with Chroma Vector Store
Here we load the data into the vector store. As mentioned above, both the text and metadata for each node will get converted into corresponding representations in Chroma. We can now run semantic queries and also metadata filtering on this data from Chroma.
``` vector_store = ChromaVectorStore(chroma_collection=chroma_collection) storage_context = StorageContext.from_defaults(vector_store=vector_store) ```

``` index = VectorStoreIndex(nodes, storage_context=storage_context) ```
## Define `VectorIndexAutoRetriever`
We define our core `VectorIndexAutoRetriever` module. The module takes in `VectorStoreInfo`, which contains a structured description of the vector store collection and the metadata filters it supports. This information will then be used in the auto-retrieval prompt where the LLM infers metadata filters.
``` from llama_index.core.retrievers import VectorIndexAutoRetriever from llama_index.core.vector_stores.types import MetadataInfo, VectorStoreInfo

vector_store_info = VectorStoreInfo( content_info="brief biography of celebrities", metadata_info=[ MetadataInfo( name="category", type="str", description=( "Category of the celebrity, one of [Sports, Entertainment," " Business, Music]" ), ), MetadataInfo( name="country", type="str", description=( "Country of the celebrity, one of [United States, Barbados," " Portugal]" ), ), ], ) retriever = VectorIndexAutoRetriever( index, vector_store_info=vector_store_info ) ```

## Running over some sample data
We try running over some sample data. Note how metadata filters are inferred - this helps with more precise retrieval!
``` retriever.retrieve("Tell me about two celebrities from United States") ```
``` INFO:llama_index.indices.vector_store.retrievers.auto_retriever.auto_retriever:Using query str: celebrities Using query str: celebrities INFO:llama_index.indices.vector_store.retrievers.auto_retriever.auto_retriever:Using filters: {'country': 'United States'} Using filters: {'country': 'United States'} INFO:llama_index.indices.vector_store.retrievers.auto_retriever.auto_retriever:Using top_k: 2 Using top_k: 2

[NodeWithScore(node=TextNode(id_='b2ab3b1a-5731-41ec-b884-405016de5a34', embedding=None, metadata={'category': 'Entertainment', 'country': 'United States'}, excluded_embed_metadata_keys=[], excluded_llm_metadata_keys=[], relationships={}, hash='28e1d0d600908a5e9f0c388f0d49b0cd58920dc13e4f2743becd135ac0f18799', text='Angelina Jolie is an American actress, filmmaker, and humanitarian. She has received numerous awards for her acting and is known for her philanthropic work.', start_char_idx=None, end_char_idx=None, text_template='{metadata_str}\n\n{content}', metadata_template='{key}: {value}', metadata_seperator='\n'), score=0.32621567877748514),
NodeWithScore(node=TextNode(id_='e0104b6a-676a-4c83-95b7-b018cb8b39b2', embedding=None, metadata={'category': 'Sports', 'country': 'United States'}, excluded_embed_metadata_keys=[], excluded_llm_metadata_keys=[], relationships={}, hash='7456e8d70b089c3830424e49b2a03c8d6d3f5cd0de42b0669a8ee518eca01012', text='Michael Jordan is a retired professional basketball player, widely regarded as one of the greatest basketball players of all time.', start_char_idx=None, end_char_idx=None, text_template='{metadata_str}\n\n{content}', metadata_template='{key}: {value}', metadata_seperator='\n'), score=0.3734030955060519)]
```
``` retriever.retrieve("Tell me about Sports celebrities from United States") ```
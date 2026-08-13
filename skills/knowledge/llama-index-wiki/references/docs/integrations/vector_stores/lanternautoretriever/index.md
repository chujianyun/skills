# developers.llamaindex.ai/python/framework/integrations/vector_stores/lanternautoretriever/index.md
> https://developers.llamaindex.ai/python/framework/integrations/vector_stores/lanternautoretriever/index.md

--- title: Lantern Vector Store (auto-retriever) | Developer Documentation ---
This guide shows how to perform **auto-retrieval** in LlamaIndex.
Many popular vector DBs support a set of metadata filters in addition to a query string for semantic search. Given a natural language query, we first use the LLM to infer a set of metadata filters as well as the right query string to pass to the vector DB (either can also be blank). This overall query bundle is then executed against the vector DB.
This allows for more dynamic, expressive forms of retrieval beyond top-k semantic search. The relevant context for a given query may only require filtering on a metadata tag, or require a joint combination of filtering + semantic search within the filtered set, or just raw semantic search.
We demonstrate an example with Lantern, but auto-retrieval is also implemented with many other vector DBs (e.g. Pinecone, Chroma, Weaviate, and more).
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.
``` %pip install llama-index-vector-stores-lantern ```
``` !pip install llama-index psycopg2-binary asyncpg ```
``` import logging import sys
logging.basicConfig(stream=sys.stdout, level=logging.INFO) logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout)) ```
``` # set up OpenAI import os
os.environ["OPENAI_API_KEY"] = "<your-api-key>"
import openai
openai.api_key = os.environ["OPENAI_API_KEY"] ```
``` import psycopg2 from sqlalchemy import make_url
connection_string = "postgresql://postgres:postgres@localhost:5432"
url = make_url(connection_string)
db_name = "postgres" conn = psycopg2.connect(connection_string) conn.autocommit = True ```
``` from llama_index.core import VectorStoreIndex, StorageContext from llama_index.vector_stores.lantern import LanternVectorStore ```
``` from llama_index.core.schema import TextNode
nodes = [ TextNode( text=( "Michael Jordan is a retired professional basketball player," " widely regarded as one of the greatest basketball players of all" " time." ), metadata={ "category": "Sports", "country": "United States", }, ), TextNode( text=( "Angelina Jolie is an American actress, filmmaker, and" " humanitarian. She has received numerous awards for her acting" " and is known for her philanthropic work." ), metadata={ "category": "Entertainment", "country": "United States", }, ), TextNode( text=( "Elon Musk is a business magnate, industrial designer, and" " engineer. He is the founder, CEO, and lead designer of SpaceX," " Tesla, Inc., Neuralink, and The Boring Company." ), metadata={ "category": "Business", "country": "United States", }, ), TextNode( text=( "Rihanna is a Barbadian singer, actress, and businesswoman. She" " has achieved significant success in the music industry and is" " known for her versatile musical style."

), metadata={ "category": "Music", "country": "Barbados", }, ), TextNode( text=( "Cristiano Ronaldo is a Portuguese professional footballer who is" " considered one of the greatest football players of all time. He" " has won numerous awards and set multiple records during his" " career." ), metadata={ "category": "Sports", "country": "Portugal", }, ), ] ```

## Build Vector Index with Lantern Vector Store
Here we load the data into the vector store. As mentioned above, both the text and metadata for each node will get converted into corresponding representations in Lantern. We can now run semantic queries and also metadata filtering on this data from Lantern.
``` vector_store = LanternVectorStore.from_params( database=db_name, host=url.host, password=url.password, port=url.port, user=url.username, table_name="famous_people", embed_dim=1536, # openai embedding dimension m=16, # HNSW M parameter ef_construction=128, # HNSW ef construction parameter ef=64, # HNSW ef search parameter )

storage_context = StorageContext.from_defaults(vector_store=vector_store) ```
``` index = VectorStoreIndex(nodes, storage_context=storage_context) ```
## Define `VectorIndexAutoRetriever`
We define our core `VectorIndexAutoRetriever` module. The module takes in `VectorStoreInfo`, which contains a structured description of the vector store collection and the metadata filters it supports. This information will then be used in the auto-retrieval prompt where the LLM infers metadata filters.
``` from llama_index.core.retrievers import VectorIndexAutoRetriever from llama_index.core.vector_stores import MetadataInfo, VectorStoreInfo

vector_store_info = VectorStoreInfo( content_info="brief biography of celebrities", metadata_info=[ MetadataInfo( name="category", type="str", description=( "Category of the celebrity, one of [Sports, Entertainment," " Business, Music]" ), ), MetadataInfo( name="country", type="str", description=( "Country of the celebrity, one of [United States, Barbados," " Portugal]" ), ), ], ) retriever = VectorIndexAutoRetriever( index, vector_store_info=vector_store_info ) ```

## Running over some sample data
We try running over some sample data. Note how metadata filters are inferred - this helps with more precise retrieval!
``` retriever.retrieve("Tell me about two celebrities from United States") ```
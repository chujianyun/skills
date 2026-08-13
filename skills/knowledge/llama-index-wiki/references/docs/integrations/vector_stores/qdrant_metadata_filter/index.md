# developers.llamaindex.ai/python/framework/integrations/vector_stores/qdrant_metadata_filter/index.md
> https://developers.llamaindex.ai/python/framework/integrations/vector_stores/qdrant_metadata_filter/index.md

--- title: Qdrant Vector Store - Metadata Filter | Developer Documentation ---

If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.
``` %pip install llama-index-vector-stores-qdrant ```
``` !pip install llama-index qdrant_client ```
Build the Qdrant VectorStore Client
``` import qdrant_client from llama_index.core import VectorStoreIndex from llama_index.vector_stores.qdrant import QdrantVectorStore

client = qdrant_client.QdrantClient( # you can use :memory: mode for fast and light-weight experiments, # it does not require to have Qdrant deployed anywhere # but requires qdrant-client >= 1.1.1 location=":memory:" # otherwise set Qdrant instance address with: # uri="http://<host>:<port>" # set API KEY for Qdrant Cloud # api_key="<API_KEY>", ) ```

Build the QdrantVectorStore and create a Qdrant Index
``` from llama_index.core.schema import TextNode
nodes = [ TextNode( text="The Shawshank Redemption", metadata={ "author": "Stephen King", "theme": "Friendship", "year": 1994, }, ), TextNode( text="The Godfather", metadata={ "director": "Francis Ford Coppola", "theme": "Mafia", "year": 1972, }, ), TextNode( text="Inception", metadata={ "director": "Christopher Nolan", "theme": "Fiction", "year": 2010, }, ), TextNode( text="To Kill a Mockingbird", metadata={ "author": "Harper Lee", "theme": "Mafia", "year": 1960, }, ), TextNode( text="1984", metadata={ "author": "George Orwell", "theme": "Totalitarianism", "year": 1949, }, ), TextNode( text="The Great Gatsby", metadata={ "author": "F. Scott Fitzgerald", "theme": "The American Dream", "year": 1925, }, ), TextNode( text="Harry Potter and the Sorcerer's Stone", metadata={ "author": "J.K. Rowling", "theme": "Fiction", "year": 1997, }, ), ] ```

``` import os
from llama_index.core import StorageContext

os.environ["OPENAI_API_KEY"] = "sk-..."

vector_store = QdrantVectorStore( client=client, collection_name="test_collection_1" ) storage_context = StorageContext.from_defaults(vector_store=vector_store) index = VectorStoreIndex(nodes, storage_context=storage_context) ```

Define metadata filters
``` from llama_index.core.vector_stores import ( MetadataFilter, MetadataFilters, FilterOperator, )

filters = MetadataFilters( filters=[ MetadataFilter(key="theme", operator=FilterOperator.EQ, value="Mafia"), ] ) ```

Retrieve from vector store with filters
``` retriever = index.as_retriever(filters=filters) retriever.retrieve("What is inception about?") ```

``` [FieldCondition(key='theme', match=MatchValue(value='Mafia'), range=None, geo_bounding_box=None, geo_radius=None, geo_polygon=None, values_count=None)]

[Column 1]
Multiple Metadata Filters with `AND` condition
``` from llama_index.core.vector_stores import FilterOperator, FilterCondition
filters = MetadataFilters( filters=[ MetadataFilter(key="theme", value="Fiction"), MetadataFilter(key="year", value=1997, operator=FilterOperator.GT), ], condition=FilterCondition.AND, )

retriever = index.as_retriever(filters=filters) retriever.retrieve("Harry Potter?") ```

[Column 2]
[NodeWithScore(node=TextNode(id_='050c085d-6d91-4080-9fd6-3f874a528970', embedding=None, metadata={'director': 'Francis Ford Coppola', 'theme': 'Mafia', 'year': 1972}, excluded_embed_metadata_keys=[], excluded_llm_metadata_keys=[], relationships={}, hash='bfa890174187ddaed4876803691ed605463de599f5493f095a03b8d83364f1ef', text='The Godfather', start_char_idx=None, end_char_idx=None, text_template='{metadata_str}\n\n{content}', metadata_template='{key}: {value}', metadata_seperator='\n'), score=0.7620959333946706),
NodeWithScore(node=TextNode(id_='11d0043a-aba3-4ffe-84cb-3f17988759be', embedding=None, metadata={'author': 'Harper Lee', 'theme': 'Mafia', 'year': 1960}, excluded_embed_metadata_keys=[], excluded_llm_metadata_keys=[], relationships={}, hash='3475334d04bbe4606cb77728d5dc0784f16c8db3f190f3692e6310906c821927', text='To Kill a Mockingbird', start_char_idx=None, end_char_idx=None, text_template='{metadata_str}\n\n{content}', metadata_template='{key}: {value}', metadata_seperator='\n'), score=0.7340329162691743)]

``` [FieldCondition(key='theme', match=MatchValue(value='Fiction'), range=None, geo_bounding_box=None, geo_radius=None, geo_polygon=None, values_count=None)] [FieldCondition(key='theme', match=MatchValue(value='Fiction'), range=None, geo_bounding_box=None, geo_radius=None, geo_polygon=None, values_count=None), FieldCondition(key='year', match=None, range=Range(lt=None, gt=1997.0, gte=None, lte=None), geo_bounding_box=None, geo_radius=None, geo_polygon=None, values_count=None)]


[NodeWithScore(node=TextNode(id_='1be42402-518f-4e88-9860-12cfec9f5ed2', embedding=None, metadata={'director': 'Christopher Nolan', 'theme': 'Fiction', 'year': 2010}, excluded_embed_metadata_keys=[], excluded_llm_metadata_keys=[], relationships={}, hash='7937eb153ccc78a3329560f37d90466ba748874df6b0303b3b8dd3c732aa7688', text='Inception', start_char_idx=None, end_char_idx=None, text_template='{metadata_str}\n\n{content}', metadata_template='{key}: {value}', metadata_seperator='\n'), score=0.7649987694994126)]
Use keyword arguments specific to Qdrant
``` retriever = index.as_retriever( vector_store_kwargs={"filter": {"theme": "Mafia"}} ) retriever.retrieve("What is inception about?") ```

``` [NodeWithScore(node=TextNode(id_='1be42402-518f-4e88-9860-12cfec9f5ed2', embedding=None, metadata={'director': 'Christopher Nolan', 'theme': 'Fiction', 'year': 2010}, excluded_embed_metadata_keys=[], excluded_llm_metadata_keys=[], relationships={}, hash='7937eb153ccc78a3329560f37d90466ba748874df6b0303b3b8dd3c732aa7688', text='Inception', start_char_idx=None, end_char_idx=None, text_template='{metadata_str}\n\n{content}', metadata_template='{key}: {value}', metadata_seperator='\n'), score=0.841150534139415),
NodeWithScore(node=TextNode(id_='ee4d3b32-7675-49bc-bc49-04011d62cf7c', embedding=None, metadata={'author': 'J.K. Rowling', 'theme': 'Fiction', 'year': 1997}, excluded_embed_metadata_keys=[], excluded_llm_metadata_keys= [], relationships={}, hash='1b24f5e9fb6f18cc893e833af8d5f28ff805a6361fc0838a3015c287510d29a3', text="Harry Potter and the Sorcerer's Stone", start_char_idx=None, end_char_idx=None, text_template='{metadata_str}\n\n{content}', metadata_template='{key}: {value}', metadata_seperator='\n'), score=0.7661930751179629)]
```
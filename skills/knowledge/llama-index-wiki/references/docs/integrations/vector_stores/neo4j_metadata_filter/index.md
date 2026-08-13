# developers.llamaindex.ai/python/framework/integrations/vector_stores/neo4j_metadata_filter/index.md
> https://developers.llamaindex.ai/python/framework/integrations/vector_stores/neo4j_metadata_filter/index.md

--- title: Neo4j Vector Store - Metadata Filter | Developer Documentation ---
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.
``` %pip install llama-index-vector-stores-neo4jvector ```
``` # !pip install llama-index>=0.9.31 neo4j ```
``` import logging import sys import os
logging.basicConfig(stream=sys.stdout, level=logging.INFO) logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout)) ```
Build a Neo4j vector Index and connect to it
``` import os from llama_index.vector_stores.neo4jvector import Neo4jVectorStore
os.environ["OPENAI_API_KEY"] = "sk-..."
username = "neo4j" password = "password" url = "bolt://localhost:7687" embed_dim = 1536 # Dimensions are for text-embedding-ada-002
vector_store = Neo4jVectorStore(username, password, url, embed_dim) ```
``` INFO:numexpr.utils:Note: NumExpr detected 16 cores but "NUMEXPR_MAX_THREADS" not set, so enforcing safe limit of 8. Note: NumExpr detected 16 cores but "NUMEXPR_MAX_THREADS" not set, so enforcing safe limit of 8. INFO:numexpr.utils:NumExpr defaulting to 8 threads. NumExpr defaulting to 8 threads. ```

Build the VectorStoreIndex
``` from llama_index.core import VectorStoreIndex, StorageContext from llama_index.core.schema import TextNode
nodes = [ TextNode( text="The Shawshank Redemption", metadata={ "author": "Stephen King", "theme": "Friendship", "year": 1994, }, ), TextNode( text="The Godfather", metadata={ "director": "Francis Ford Coppola", "theme": "Mafia", "year": 1972, }, ), TextNode( text="Inception", metadata={ "director": "Christopher Nolan", "theme": "Fiction", "year": 2010, }, ), TextNode( text="To Kill a Mockingbird", metadata={ "author": "Harper Lee", "theme": "Mafia", "year": 1960, }, ), TextNode( text="1984", metadata={ "author": "George Orwell", "theme": "Totalitarianism", "year": 1949, }, ), TextNode( text="The Great Gatsby", metadata={ "author": "F. Scott Fitzgerald", "theme": "The American Dream", "year": 1925, }, ), TextNode( text="Harry Potter and the Sorcerer's Stone", metadata={ "author": "J.K. Rowling", "theme": "Fiction", "year": 1997, }, ), ] ```

``` storage_context = StorageContext.from_defaults(vector_store=vector_store) index = VectorStoreIndex(nodes, storage_context=storage_context) ```
``` INFO:httpx:HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK" HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK" ```
Define metadata filters
``` from llama_index.core.vector_stores import ( MetadataFilter, MetadataFilters, FilterOperator, )

filters = MetadataFilters( filters=[ MetadataFilter( key="theme", operator=FilterOperator.EQ, value="Fiction" ), ] ) ```

Retrieve from vector store with filters
``` retriever = index.as_retriever(filters=filters) retriever.retrieve("What is inception about?") ```

[NodeWithScore(node=TextNode(id_='814e5f2a-2150-4bae-8a59-fa728379e978', embedding=None, metadata={'director': 'Christopher Nolan', 'theme': 'Fiction', 'year': 2010}, excluded_embed_metadata_keys=[], excluded_llm_metadata_keys=[], relationships={}, text='Inception', start_char_idx=None, end_char_idx=None, text_template='{metadata_str}\n\n{content}', metadata_template='{key}: {value}', metadata_seperator='\n'), score=0.9202238321304321),
NodeWithScore(node=TextNode(id_='fc1df8cc-f1d3-4a7b-8c21-f83b18463758', embedding=None, metadata={'author': 'J.K. Rowling', 'theme': 'Fiction', 'year': 1997}, excluded_embed_metadata_keys=[], excluded_llm_metadata_keys= [], relationships={}, text="Harry Potter and the Sorcerer's Stone", start_char_idx=None, end_char_idx=None, text_template='{metadata_str}\n\n{content}', metadata_template='{key}: {value}', metadata_seperator='\n'), score=0.8823964595794678)]
Multiple Metadata Filters with `AND` condition

filters = MetadataFilters( filters=[ MetadataFilter(key="theme", value="Fiction"), MetadataFilter(key="year", value=1997, operator=FilterOperator.GT), ], condition=FilterCondition.AND, )

[Column 1]
Multiple Metadata Filters with `OR` condition
``` from llama_index.core.vector_stores import FilterOperator, FilterCondition
filters = MetadataFilters( filters=[ MetadataFilter(key="theme", value="Fiction"), MetadataFilter(key="year", value=1997, operator=FilterOperator.GT), ], condition=FilterCondition.OR, )

retriever = index.as_retriever(filters=filters) retriever.retrieve("Harry Potter?") ```
``` INFO:httpx:HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK" HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"

[Column 2]
[NodeWithScore(node=TextNode(id_='814e5f2a-2150-4bae-8a59-fa728379e978', embedding=None, metadata={'director': 'Christopher Nolan', 'theme': 'Fiction', 'year': 2010}, excluded_embed_metadata_keys=[], excluded_llm_metadata_keys=[], relationships={}, text='Inception', start_char_idx=None, end_char_idx=None, text_template='{metadata_str}\n\n{content}', metadata_template='{key}: {value}', metadata_seperator='\n'), score=0.8818434476852417)]


[NodeWithScore(node=TextNode(id_='fc1df8cc-f1d3-4a7b-8c21-f83b18463758', embedding=None, metadata={'author': 'J.K. Rowling', 'theme': 'Fiction', 'year': 1997}, excluded_embed_metadata_keys=[], excluded_llm_metadata_keys= [], relationships={}, text="Harry Potter and the Sorcerer's Stone", start_char_idx=None, end_char_idx=None, text_template='{metadata_str}\n\n{content}', metadata_template='{key}: {value}', metadata_seperator='\n'), score=0.9242331385612488),
NodeWithScore(node=TextNode(id_='814e5f2a-2150-4bae-8a59-fa728379e978', embedding=None, metadata={'director': 'Christopher Nolan', 'theme': 'Fiction', 'year': 2010}, excluded_embed_metadata_keys=[], excluded_llm_metadata_keys=[], relationships={}, text='Inception', start_char_idx=None, end_char_idx=None, text_template='{metadata_str}\n\n{content}', metadata_template='{key}: {value}', metadata_seperator='\n'), score=0.8818434476852417)]
```
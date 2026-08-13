# developers.llamaindex.ai/python/framework/integrations/vector_stores/chroma_metadata_filter/index.md
> https://developers.llamaindex.ai/python/framework/integrations/vector_stores/chroma_metadata_filter/index.md

--- title: Chroma Vector Store | Developer Documentation ---
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.
``` %pip install llama-index-vector-stores-chroma ```
``` !pip install llama-index ```
#### Creating a Chroma Index
``` import logging import sys
logging.basicConfig(stream=sys.stdout, level=logging.INFO) logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout)) ```
``` import os import getpass
# os.environ["OPENAI_API_KEY"] = getpass.getpass("OpenAI API Key:") import openai
openai.api_key = "sk-" ```
``` import chromadb ```
``` chroma_client = chromadb.EphemeralClient() chroma_collection = chroma_client.create_collection("quickstart") ```
``` from llama_index.core import VectorStoreIndex from llama_index.vector_stores.chroma import ChromaVectorStore from IPython.display import Markdown, display ```
``` from llama_index.core.schema import TextNode
nodes = [ TextNode( text="The Shawshank Redemption", metadata={ "author": "Stephen King", "theme": "Friendship", "year": 1994, }, ), TextNode( text="The Godfather", metadata={ "director": "Francis Ford Coppola", "theme": "Mafia", "year": 1972, }, ), TextNode( text="Inception", metadata={ "director": "Christopher Nolan", "theme": "Fiction", "year": 2010, }, ), TextNode( text="To Kill a Mockingbird", metadata={ "author": "Harper Lee", "theme": "Mafia", "year": 1960, }, ), TextNode( text="1984", metadata={ "author": "George Orwell", "theme": "Totalitarianism", "year": 1949, }, ), TextNode( text="The Great Gatsby", metadata={ "author": "F. Scott Fitzgerald", "theme": "The American Dream", "year": 1925, }, ), TextNode( text="Harry Potter and the Sorcerer's Stone", metadata={ "author": "J.K. Rowling", "theme": "Fiction", "year": 1997, }, ), ] ```

``` from llama_index.core import StorageContext
vector_store = ChromaVectorStore(chroma_collection=chroma_collection) storage_context = StorageContext.from_defaults(vector_store=vector_store) ```
``` index = VectorStoreIndex(nodes, storage_context=storage_context) ```
## One Exact Match Filter
``` from llama_index.core.vector_stores import ( MetadataFilter, MetadataFilters, FilterOperator, )

filters = MetadataFilters( filters=[ MetadataFilter(key="theme", operator=FilterOperator.EQ, value="Mafia"), ] )

[Column 1]
## Multiple Exact Match Metadata Filters
``` from llama_index.core.vector_stores import ExactMatchFilter, MetadataFilters

filters = MetadataFilters( filters=[ MetadataFilter(key="theme", value="Mafia"), MetadataFilter(key="year", value=1972), ] )

retriever = index.as_retriever(filters=filters) retriever.retrieve("What is inception about?") ```

[Column 2]
[NodeWithScore(node=TextNode(id_='f343294f-4cd5-4f1c-acbf-19490aa95efb', embedding=None, metadata={'director': 'Francis Ford Coppola', 'theme': 'Mafia', 'year': 1972}, excluded_embed_metadata_keys=[], excluded_llm_metadata_keys=[], relationships={}, hash='79563896e320da86be371351f55d903acdcfb3229368a6622f6be6e929e8b7cc', text='The Godfather', start_char_idx=None, end_char_idx=None, text_template='{metadata_str}\n\n{content}', metadata_template='{key}: {value}', metadata_seperator='\n'), score=0.6215522669166147),
NodeWithScore(node=TextNode(id_='7910d5cd-7871-46e5-b71a-0dae1797aee1', embedding=None, metadata={'author': 'Harper Lee', 'theme': 'Mafia', 'year': 1960}, excluded_embed_metadata_keys=[], excluded_llm_metadata_keys=[], relationships={}, hash='0a1875c24455356c77eedd8eddd39035ec622959b59d2296eff56d42019a0c00', text='To Kill a Mockingbird', start_char_idx=None, end_char_idx=None, text_template='{metadata_str}\n\n{content}', metadata_template='{key}: {value}', metadata_seperator='\n'), score=0.5873631114046581)]


[NodeWithScore(node=TextNode(id_='f343294f-4cd5-4f1c-acbf-19490aa95efb', embedding=None, metadata={'director': 'Francis Ford Coppola', 'theme': 'Mafia', 'year': 1972}, excluded_embed_metadata_keys=[], excluded_llm_metadata_keys=[], relationships={}, hash='79563896e320da86be371351f55d903acdcfb3229368a6622f6be6e929e8b7cc', text='The Godfather', start_char_idx=None, end_char_idx=None, text_template='{metadata_str}\n\n{content}', metadata_template='{key}: {value}', metadata_seperator='\n'), score=0.6215522669166147)]
## Multiple Metadata Filters with `AND` condition

filters = MetadataFilters( filters=[ MetadataFilter(key="theme", value="Fiction"), MetadataFilter(key="year", value=1997, operator=FilterOperator.GT), ], condition=FilterCondition.AND, )

[NodeWithScore(node=TextNode(id_='b71ce5e8-353e-42c6-94b3-d0a11370aaba', embedding=None, metadata={'director': 'Christopher Nolan', 'theme': 'Fiction', 'year': 2010}, excluded_embed_metadata_keys=[], excluded_llm_metadata_keys=[], relationships={}, hash='110b4ab08da17685bdc3d53aecf6085a535dd00a43612eed991bce8074aa36a9', text='Inception', start_char_idx=None, end_char_idx=None, text_template='{metadata_str}\n\n{content}', metadata_template='{key}: {value}', metadata_seperator='\n'), score=0.6250006485226994)]
## Multiple Metadata Filters with `OR` condition
``` from llama_index.core.vector_stores import FilterOperator, FilterCondition
filters = MetadataFilters( filters=[ MetadataFilter(key="theme", value="Fiction"), MetadataFilter(key="year", value=1997, operator=FilterOperator.GT), ], condition=FilterCondition.OR, )

retriever = index.as_retriever(filters=filters) retriever.retrieve("Harry Potter?") ```
``` INFO:httpx:HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK" HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"

[NodeWithScore(node=TextNode(id_='6b0e9499-9f4d-4637-ab2a-460e5c870948', embedding=None, metadata={'author': 'J.K. Rowling', 'theme': 'Fiction', 'year': 1997}, excluded_embed_metadata_keys=[], excluded_llm_metadata_keys= [], relationships={}, hash='a2656c2bc96ed472bb0ed3ea81075042e9860987f3156428789d07079e019ed0', text="Harry Potter and the Sorcerer's Stone", start_char_idx=None, end_char_idx=None, text_template='{metadata_str}\n\n{content}', metadata_template='{key}: {value}', metadata_seperator='\n'), score=0.7405548668973673),
NodeWithScore(node=TextNode(id_='b71ce5e8-353e-42c6-94b3-d0a11370aaba', embedding=None, metadata={'director': 'Christopher Nolan', 'theme': 'Fiction', 'year': 2010}, excluded_embed_metadata_keys=[], excluded_llm_metadata_keys=[], relationships={}, hash='110b4ab08da17685bdc3d53aecf6085a535dd00a43612eed991bce8074aa36a9', text='Inception', start_char_idx=None, end_char_idx=None, text_template='{metadata_str}\n\n{content}', metadata_template='{key}: {value}', metadata_seperator='\n'), score=0.6250006485226994)]
```
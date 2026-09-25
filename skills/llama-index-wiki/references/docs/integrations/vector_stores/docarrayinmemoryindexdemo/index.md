# developers.llamaindex.ai/python/framework/integrations/vector_stores/docarrayinmemoryindexdemo/index.md
> https://developers.llamaindex.ai/python/framework/integrations/vector_stores/docarrayinmemoryindexdemo/index.md

--- title: DocArray InMemory Vector Store | Developer Documentation ---
DocArrayInMemoryVectorStore [1] is a document index provided by Docarray [2] that stores documents in memory. It is a great starting point for small datasets, where you may not want to launch a database server.
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.
``` %pip install llama-index-vector-stores-docarray ```
``` !pip install llama-index ```
``` import os import sys import logging import textwrap

import warnings
warnings.filterwarnings("ignore")
# stop huggingface warnings os.environ["TOKENIZERS_PARALLELISM"] = "false"
# Uncomment to see debug logs # logging.basicConfig(stream=sys.stdout, level=logging.INFO) # logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))
from llama_index.core import ( GPTVectorStoreIndex, SimpleDirectoryReader, Document, ) from llama_index.vector_stores.docarray import DocArrayInMemoryVectorStore from IPython.display import Markdown, display ```

``` import os
os.environ["OPENAI_API_KEY"] = "<your openai key>" ```
Download Data
``` !mkdir -p 'data/paul_graham/' !wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt' ```
``` # load documents documents = SimpleDirectoryReader("./data/paul_graham/").load_data() print( "Document ID:", documents[0].doc_id, "Document Hash:", documents[0].doc_hash, ) ```

``` Document ID: 1c21062a-50a3-4133-a0b1-75f837a953e5 Document Hash: 77ae91ab542f3abb308c4d7c77c9bc4c9ad0ccd63144802b7cbe7e1bb3a4094e ```
## Initialization and indexing

vector_store = DocArrayInMemoryVectorStore() storage_context = StorageContext.from_defaults(vector_store=vector_store) index = GPTVectorStoreIndex.from_documents( documents, storage_context=storage_context ) ```
## Querying
``` # set Logging to DEBUG for more detailed outputs query_engine = index.as_query_engine() response = query_engine.query("What did the author do growing up?") print(textwrap.fill(str(response), 100)) ```
``` Token indices sequence length is longer than the specified maximum sequence length for this model (1830 > 1024). Running this sequence through the model will result in indexing errors
Growing up, the author wrote short stories, programmed on an IBM 1401, and nagged his father to buy him a TRS-80 microcomputer. He wrote simple games, a program to predict how high his model rockets would fly, and a word processor. He also studied philosophy in college, but switched to AI after becoming bored with it. He then took art classes at Harvard and applied to art schools, eventually attending RISD. ```
``` response = query_engine.query("What was a hard moment for the author?") print(textwrap.fill(str(response), 100)) ```
``` A hard moment for the author was when he realized that the AI programs of the time were a hoax and that there was an unbridgeable gap between what they could do and actually understanding natural language. He had invested a lot of time and energy into learning about AI and was disappointed to find out that it was not going to get him the results he had hoped for. ```
## Querying with filters
``` from llama_index.core.schema import TextNode
nodes = [ TextNode( text="The Shawshank Redemption", metadata={ "author": "Stephen King", "theme": "Friendship", }, ), TextNode( text="The Godfather", metadata={ "director": "Francis Ford Coppola", "theme": "Mafia", }, ), TextNode( text="Inception", metadata={ "director": "Christopher Nolan", }, ), ] ```

``` from llama_index.core import StorageContext
vector_store = DocArrayInMemoryVectorStore() storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = GPTVectorStoreIndex(nodes, storage_context=storage_context) ```
``` from llama_index.core.vector_stores import ExactMatchFilter, MetadataFilters
filters = MetadataFilters( filters=[ExactMatchFilter(key="theme", value="Mafia")] )
retriever = index.as_retriever(filters=filters) retriever.retrieve("What is inception about?") ```
``` [NodeWithScore(node=Node(text='director: Francis Ford Coppola\ntheme: Mafia\n\nThe Godfather', doc_id='41c99963-b200-4ce6-a9c4-d06ffeabdbc5', embedding=None, doc_hash='b770e43e6a94854a22dc01421d3d9ef6a94931c2b8dbbadf4fdb6eb6fbe41010', extra_info=None, node_info=None, relationships={<DocumentRelationship.SOURCE: '1'>: 'None'}), score=0.7681788983417586)] ```

[1] https://docs.docarray.org/user_guide/storing/index_in_memory/
[2] https://github.com/docarray/docarray
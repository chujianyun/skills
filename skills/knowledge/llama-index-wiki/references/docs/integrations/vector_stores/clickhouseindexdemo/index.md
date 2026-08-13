# developers.llamaindex.ai/python/framework/integrations/vector_stores/clickhouseindexdemo/index.md
> https://developers.llamaindex.ai/python/framework/integrations/vector_stores/clickhouseindexdemo/index.md

--- title: ClickHouse Vector Store | Developer Documentation ---

In this notebook we are going to show a quick demo of using the ClickHouseVectorStore.
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.
``` !pip install llama-index !pip install clickhouse_connect ```

#### Creating a ClickHouse Client
``` import logging import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO) logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout)) ```
``` from os import environ import clickhouse_connect

environ["OPENAI_API_KEY"] = "sk-*"
# initialize client client = clickhouse_connect.get_client( host="localhost", port=8123, username="default", password="", ) ```

#### Load documents, build and store the VectorStoreIndex with ClickHouseVectorStore
Here we will use a set of Paul Graham essays to provide the text to turn into embeddings, store in a `ClickHouseVectorStore` and query to find context for our LLM QnA loop.
``` from llama_index.core import VectorStoreIndex, SimpleDirectoryReader from llama_index.vector_stores.clickhouse import ClickHouseVectorStore ```

``` # load documents documents = SimpleDirectoryReader("../data/paul_graham").load_data() print("Document ID:", documents[0].doc_id) print("Number of Documents: ", len(documents)) ```

``` Document ID: d03ac7db-8dae-4199-bc38-445dec51a534 Number of Documents: 1 ```

Download Data
``` !mkdir -p 'data/paul_graham/' !wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt' ```

``` --2024-02-13 10:08:31-- https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt Resolving raw.githubusercontent.com (raw.githubusercontent.com)... 185.199.111.133, 185.199.109.133, 185.199.110.133, ... Connecting to raw.githubusercontent.com (raw.githubusercontent.com)|185.199.111.133|:443... connected. HTTP request sent, awaiting response... 200 OK Length: 75042 (73K) [text/plain] Saving to: ‘data/paul_graham/paul_graham_essay.txt’

data/paul_graham/pa 100%[===================>] 73.28K --.-KB/s in 0.003s
2024-02-13 10:08:31 (23.9 MB/s) - ‘data/paul_graham/paul_graham_essay.txt’ saved [75042/75042] ```
You can process your files individually using SimpleDirectoryReader:
``` loader = SimpleDirectoryReader("./data/paul_graham/") documents = loader.load_data() for file in loader.input_files: print(file) # Here is where you would do any preprocessing ```

``` data/paul_graham/paul_graham_essay.txt ```
``` # initialize with metadata filter and store indexes from llama_index.core import StorageContext

for document in documents: document.metadata = {"user_id": "123", "favorite_color": "blue"} vector_store = ClickHouseVectorStore(clickhouse_client=client) storage_context = StorageContext.from_defaults(vector_store=vector_store) index = VectorStoreIndex.from_documents( documents, storage_context=storage_context ) ```

#### Query Index
Now ClickHouse vector store supports filter search and hybrid search
You can learn more about query\_engine and retriever.
``` import textwrap
from llama_index.core.vector_stores import ExactMatchFilter, MetadataFilters
# set Logging to DEBUG for more detailed outputs query_engine = index.as_query_engine( filters=MetadataFilters( filters=[ ExactMatchFilter(key="user_id", value="123"), ] ), similarity_top_k=2, vector_store_query_mode="hybrid", ) response = query_engine.query("What did the author learn?") print(textwrap.fill(str(response), 100)) ```

``` The author learned several things during their time at Interleaf, including the importance of having technology companies run by product people rather than sales people, the drawbacks of having too many people edit code, the value of corridor conversations over planned meetings, the challenges of dealing with big bureaucratic customers, and the importance of being the "entry level" option in a market. ```

#### Clear All Indexes
``` for document in documents: index.delete_ref_doc(document.doc_id) ```
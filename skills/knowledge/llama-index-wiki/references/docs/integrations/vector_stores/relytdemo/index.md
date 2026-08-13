# developers.llamaindex.ai/python/framework/integrations/vector_stores/relytdemo/index.md
> https://developers.llamaindex.ai/python/framework/integrations/vector_stores/relytdemo/index.md

--- title: Relyt | Developer Documentation ---

![Open In Colab][2] [1]
Firstly, you will probably need to install dependencies :
``` %pip install llama-index-vector-stores-relyt ```
``` %pip install llama-index "pgvecto_rs[sdk]" ```
Then start the relyt as the official document [3]:
Setup the logger.
``` import logging import os import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO) logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout)) ```
#### Creating a pgvecto\_rs client
``` from pgvecto_rs.sdk import PGVectoRs
URL = "postgresql+psycopg://{username}:{password}@{host}:{port}/{db_name}".format( port=os.getenv("RELYT_PORT", "5432"), host=os.getenv("RELYT_HOST", "localhost"), username=os.getenv("RELYT_USER", "postgres"), password=os.getenv("RELYT_PASS", "mysecretpassword"), db_name=os.getenv("RELYT_NAME", "postgres"), )

client = PGVectoRs( db_url=URL, collection_name="example", dimension=1536, # Using OpenAI’s text-embedding-ada-002 ) ```

#### Setup OpenAI
``` import os
os.environ["OPENAI_API_KEY"] = "sk-..." ```
#### Load documents, build the PGVectoRsStore and VectorStoreIndex
``` from IPython.display import Markdown, display
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex from llama_index.vector_stores.relyt import RelytVectorStore ```
Download Data
``` !mkdir -p 'data/paul_graham/' !wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt' ```

``` # load documents documents = SimpleDirectoryReader("./data/paul_graham").load_data() ```

``` # initialize without metadata filter from llama_index.core import StorageContext

vector_store = RelytVectorStore(client=client) storage_context = StorageContext.from_defaults(vector_store=vector_store) index = VectorStoreIndex.from_documents( documents, storage_context=storage_context ) ```

#### Query Index
``` # set Logging to DEBUG for more detailed outputs query_engine = index.as_query_engine() response = query_engine.query("What did the author do growing up?") ```

``` INFO:httpx:HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK" HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK" INFO:httpx:HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK" HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK" ```

``` display(Markdown(f"<b>{response}</b>")) ```
**The author, growing up, worked on writing and programming. They wrote short stories and also tried writing programs on an IBM 1401 computer. They later got a microcomputer and started programming more extensively, writing simple games and a word processor.**

[1] https://colab.research.google.com/github/run-llama/llama_index/blob/main/docs/examples/vector_stores/PGVectoRsDemo.ipynb
[2] https://colab.research.google.com/assets/colab-badge.svg
[3] https://docs.relyt.cn/docs/vector-engine/use/
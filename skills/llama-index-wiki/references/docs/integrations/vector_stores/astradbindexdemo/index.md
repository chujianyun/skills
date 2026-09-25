# developers.llamaindex.ai/python/framework/integrations/vector_stores/astradbindexdemo/index.md
> https://developers.llamaindex.ai/python/framework/integrations/vector_stores/astradbindexdemo/index.md

--- title: Astra DB | Developer Documentation ---

> DataStax Astra DB [1] is a serverless vector-capable database built on Apache Cassandra and accessed through an easy-to-use JSON API.
To run this notebook you need a DataStax Astra DB instance running in the cloud (you can get one for free at datastax.com [2]).
You should ensure you have `llama-index` and `astrapy` installed:
``` %pip install llama-index-vector-stores-astra-db %pip install llama-index-embeddings-openai ```

``` !pip install llama-index !pip install "astrapy>=1.0" ```

### Please provide database connection parameters and secrets:
``` import os import getpass

api_endpoint = input( "\nPlease enter your Database Endpoint URL (e.g. 'https://4bc...datastax.com'):" )

token = getpass.getpass( "\nPlease enter your 'Database Administrator' Token (e.g. 'AstraCS:...'):" )

os.environ["OPENAI_API_KEY"] = getpass.getpass( "\nPlease enter your OpenAI API Key (e.g. 'sk-...'):" ) ```

### Import needed package dependencies:
``` from llama_index.core import ( VectorStoreIndex, SimpleDirectoryReader, StorageContext, ) from llama_index.embeddings.openai import OpenAIEmbedding from llama_index.vector_stores.astra_db import AstraDBVectorStore ```

### Load some example data:
``` !mkdir -p 'data/paul_graham/' !wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt' ```

### Read the data:
``` # load documents documents = SimpleDirectoryReader("./data/paul_graham/").load_data() print(f"Total documents: {len(documents)}") print(f"First document, id: {documents[0].doc_id}") print(f"First document, hash: {documents[0].hash}") print( "First document, text" f" ({len(documents[0].text)} characters):\n{'='*20}\n{documents[0].text[:360]} ..." ) ```

### Create the Astra DB Vector Store object:
``` astra_db_store = AstraDBVectorStore( token=token, api_endpoint=api_endpoint, collection_name="astra_v_table", embedding_dimension=1536, ) ```

### Build the Index from the Documents:
``` embed_model = OpenAIEmbedding(model_name="text-embedding-3-small")
storage_context = StorageContext.from_defaults(vector_store=astra_db_store)
index = VectorStoreIndex.from_documents( documents, storage_context=storage_context, embed_model=embed_model ) ```

### Query using the index:
``` query_engine = index.as_query_engine() response = query_engine.query("Why did the author choose to work on AI?")

print(response.response) ```

[1] https://docs.datastax.com/en/astra/home/astra.html
[2] https://astra.datastax.com
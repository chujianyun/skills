# developers.llamaindex.ai/python/framework/integrations/vector_stores/databricksvectorsearchdemo/index.md
> https://developers.llamaindex.ai/python/framework/integrations/vector_stores/databricksvectorsearchdemo/index.md

--- title: Databricks Vector Search | Developer Documentation ---

Databricks Vector Search is a vector database that is built into the Databricks Intelligence Platform and integrated with its governance and productivity tools. Full docs here: <https://docs.databricks.com/en/generative- ai/vector-search.html>

Install llama-index and databricks-vectorsearch. You must be inside a Databricks runtime to use the Vector Search python client.
``` %pip install llama-index llama-index-vector-stores-databricks %pip install databricks-vectorsearch ```

Import databricks dependencies
``` from databricks.vector_search.client import ( VectorSearchIndex, VectorSearchClient, ) ```

Import LlamaIndex dependencies
``` from llama_index.core import ( VectorStoreIndex, SimpleDirectoryReader, ServiceContext, StorageContext, ) from llama_index.vector_stores.databricks import DatabricksVectorSearch ```

Load example data

``` !mkdir -p 'data/paul_graham/' !wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt' ```

Read the data
``` # load documents documents = SimpleDirectoryReader("./data/paul_graham/").load_data() print(f"Total documents: {len(documents)}") print(f"First document, id: {documents[0].doc_id}") print(f"First document, hash: {documents[0].hash}") print( "First document, text" f" ({len(documents[0].text)} characters):\n{'='*20}\n{documents[0].text[:360]} ..." ) ```

Create a Databricks Vector Search endpoint which will serve the index
``` # Create a vector search endpoint client = VectorSearchClient() client.create_endpoint( name="llamaindex_dbx_vector_store_test_endpoint", endpoint_type="STANDARD" ) ```

Create the Databricks Vector Search index, and build it from the documents
``` # Create a vector search index # it must be placed inside a Unity Catalog-enabled schema

# We'll use self-managed embeddings (i.e. managed by LlamaIndex) rather than a Databricks-managed index databricks_index = client.create_direct_access_index( endpoint_name="llamaindex_dbx_vector_store_test_endpoint", index_name="my_catalog.my_schema.my_test_table", primary_key="my_primary_key_name", embedding_dimension=1536, # match the embeddings model dimension you're going to use embedding_vector_column="my_embedding_vector_column_name", # you name this anything you want - it'll be picked up by the LlamaIndex class schema={ "my_primary_key_name": "string", "my_embedding_vector_column_name": "array<double>", "text": "string", # one column must match the text_column in the DatabricksVectorSearch instance created below; this will hold the raw node text, "doc_id": "string", # one column must contain the reference document ID (this will be populated by LlamaIndex automatically) # add any other metadata you may have in your nodes (Databricks Vector Search supports metadata filtering) # NOTE THAT THESE FIELDS MUST BE ADDED EXPLICITLY TO BE USED FOR METADATA FILTERING

}, )
databricks_vector_store = DatabricksVectorSearch( index=databricks_index, text_column="text", columns=None, # YOU MUST ALSO RECORD YOUR METADATA FIELD NAMES HERE ) # text_column is required for self-managed embeddings storage_context = StorageContext.from_defaults( vector_store=databricks_vector_store ) index = VectorStoreIndex.from_documents( documents, storage_context=storage_context ) ```

Query the index
``` query_engine = index.as_query_engine() response = query_engine.query("Why did the author choose to work on AI?")

print(response.response) ```
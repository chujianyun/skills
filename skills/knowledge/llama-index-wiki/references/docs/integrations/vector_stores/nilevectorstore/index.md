# developers.llamaindex.ai/python/framework/integrations/vector_stores/nilevectorstore/index.md
> https://developers.llamaindex.ai/python/framework/integrations/vector_stores/nilevectorstore/index.md

--- title: Nile Vector Store (Multi-tenant PostgreSQL) | Developer Documentation ---

This notebook shows how to use the Postgres based vector store `NileVectorStore` to store and query vector embeddings for multi-tenant RAG applications.
## What is Nile?
Nile is a Postgres database that enables all database operations per tenant including auto-scaling, branching, and backups, with full customer isolation.
Multi-tenant RAG applications are increasingly popular, since they provide security and privacy while using large language models.
However, managing the underlying Postgres database is not straightforward. DB-per-tenant is expensive and complex to manage, while shared-DB has security and privacy concerns, and also limits the scalability and performance of the RAG application. Nile re-engineered Postgres to deliver the best of all worlds - the isolation of DB-per-tenant, at the cost, efficiency and developer experience of a shared-DB.
Storing millions of vectors in a shared-DB can be slow and require significant resources to index and query. But if you store 1000 tenants in Nile’s virtual tenant databases, each with 1000 vectors, this can be quite managable. Especially since you can place larger tenants on their own compute, while smaller tenants can efficiently share compute resources and auto-scale as needed.
## Getting Started with Nile
Start by signing up for Nile [1]. Once you’ve signed up for Nile, you’ll be promoted to create your first database. Go ahead and do so. You’ll be redirected to the “Query Editor” page of your new database.
From there, click on “Home” (top icon on the left menu), click on “generate credentials” and copy the resulting connection string. You will need it in a sec.
## Additional Resources
- Nile’s LlamaIndex documentation [2] - Nile’s generative AI and vector embeddings docs [3] - Nile’s pgvector primer [4] - Few things you didn’t know about pgvector [5]

## Before you begin
### Install dependencies
Lets install and import dependencies.
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.
``` %pip install llama-index-vector-stores-nile %pip install /Users/gwen/workspaces/llama_index/llama-index-integrations/vector_stores/llama-index-vector-stores-nile/dist/llama_index_vector_stores_nile-0.1.1.tar.gz ```

``` !pip install llama-index ```
``` import logging
from llama_index.core import SimpleDirectoryReader, StorageContext from llama_index.core import VectorStoreIndex from llama_index.core.vector_stores import ( MetadataFilter, MetadataFilters, FilterOperator, ) from llama_index.vector_stores.nile import NileVectorStore, IndexType ```

### Setup connection to Nile database
Assuming you followed the instructions in the previous section, Getting Started with Nile, you should now have a connection string to your Nile database.
You can set it in an environment variable called `NILEDB_SERVICE_URL`, or in Python directly.
``` %env NILEDB_SERVICE_URL=postgresql://username:password@us-west-2.db.thenile.dev:5432/niledb ```
And now, we’ll create a `NileVectorStore`. Note that in addition to the usual parameters like URL and dimensions, we also set `tenant_aware=True`.
:fire: NileVectorStore supports both tenant-aware vector stores, that isolates the documents for each tenant and a regular store which is typically used for shared data that all tenants can access. Below, we’ll demonstrate the tenant-aware vector store.
``` # Get the service url by reading local .env file with NILE_SERVICE_URL variable import os

NILEDB_SERVICE_URL = os.environ["NILEDB_SERVICE_URL"]
# OR set it explicitly # NILE_SERVICE_URL = "postgresql://nile:password@db.thenile.dev:5432/nile"
vector_store = NileVectorStore( service_url=NILEDB_SERVICE_URL, table_name="documents", tenant_aware=True, num_dimensions=1536, ) ```

### Setup OpenAI
You can set it in an .env file, or in Python directly
``` %env OPENAI_API_KEY=sk-... ```
``` # Uncomment and set it explicitly if you prefer not to use .env # os.environ["OPENAI_API_KEY"] = "sk-..." ```

## Multi-tenant similarity search
To demonstrate multi-tenant similarity search with LlamaIndex and Nile, we will download two documents - each with a transcript from a sales call by a different company. Nexiv provides IT services and ModaMart is in retail. We’ll add tenant identifiers to each document and load them to a tenant-aware vector store. Then, we will query the store for each tenant. You will see how the same question generates two different responses, because it retrieves different documents for each tenant.
### Download data
``` !mkdir -p data !wget "https://raw.githubusercontent.com/niledatabase/niledatabase/main/examples/ai/sales_insight/data/transcripts/nexiv-solutions__0_transcript.txt" -O "data/nexiv-solutions__0_transcript.txt" !wget "https://raw.githubusercontent.com/niledatabase/niledatabase/main/examples/ai/sales_insight/data/transcripts/modamart__0_transcript.txt" -O "data/modamart__0_transcript.txt" ```

### Load documents
We’ll use LlamaIndex’s `SimpleDirectoryReader` to load the documents. Because we want to update the documents with the tenant metadata after loading, we’ll use a separate reader for each tenant
``` reader = SimpleDirectoryReader( input_files=["data/nexiv-solutions__0_transcript.txt"] ) documents_nexiv = reader.load_data()

reader = SimpleDirectoryReader(input_files=["data/modamart__0_transcript.txt"]) documents_modamart = reader.load_data() ```
### Enrich documents with tenant metadata
We are going to create two Nile tenants and the add the tenant ID of each to the document metadata. We are also adding some additional metadata like a custom document ID and a category. This metadata can be used for filtering documents during the retrieval process. Of course, in your own application, you could also load documents for existing tenants and add any metadata information you find useful.
``` tenant_id_nexiv = str(vector_store.create_tenant("nexiv-solutions")) tenant_id_modamart = str(vector_store.create_tenant("modamart"))

# Add the tenant id to the metadata for i, doc in enumerate(documents_nexiv, start=1): doc.metadata["tenant_id"] = tenant_id_nexiv doc.metadata[ "category" ] = "IT" # We will use this to apply additional filters in a later example doc.id_ = f"nexiv_doc_id_{i}" # We are also setting a custom id, this is optional but can be useful

for i, doc in enumerate(documents_modamart, start=1): doc.metadata["tenant_id"] = tenant_id_modamart doc.metadata["category"] = "Retail" doc.id_ = f"modamart_doc_id_{i}" ```

### Creating a VectorStore index with NileVectorStore
We are loading all documents to the same `VectorStoreIndex`. Since we created a tenant-aware `NileVectorStore` when we set things up, Nile will correctly use the `tenant_id` field in the metadata to isolate them.
Loading documents without `tenant_id` to a tenant-aware store will throw a `ValueException`.
``` storage_context = StorageContext.from_defaults(vector_store=vector_store) index = VectorStoreIndex.from_documents( documents_nexiv + documents_modamart, storage_context=storage_context, show_progress=True, ) ```

``` /Users/gwen/.pyenv/versions/3.10.15/lib/python3.10/site-packages/tqdm/auto.py:21: TqdmWarning: IProgress not found. Please update jupyter and ipywidgets. See https://ipywidgets.readthedocs.io/en/stable/user_install.html from .autonotebook import tqdm as notebook_tqdm Parsing nodes: 100%|██████████| 2/2 [00:00<00:00, 1129.32it/s] Generating embeddings: 100%|██████████| 2/2 [00:00<00:00, 4.58it/s] ```

### Querying the index for each tenant
You can see below how we specify the tenant for each query, and therefore we get an answer relevant to that tenant and only for them
``` nexiv_query_engine = index.as_query_engine( similarity_top_k=3, vector_store_kwargs={ "tenant_id": str(tenant_id_nexiv), }, )

print(nexiv_query_engine.query("What were the customer pain points?")) ```
``` The customer pain points were related to managing customer data using multiple platforms, leading to data discrepancies, time-consuming reconciliation efforts, and decreased productivity. ```
``` modamart_query_engine = index.as_query_engine( similarity_top_k=3, vector_store_kwargs={ "tenant_id": str(tenant_id_modamart), }, )

print(modamart_query_engine.query("What were the customer pain points?")) ```
``` The customer's pain points were concerns about the quality and value of the winter jackets, skepticism towards reviews, worries about sizing and fit when ordering clothes online, and the desire for a warm but lightweight jacket. ```

### Querying existing embeddings
In the example above, we created the index by loading and embedding new documents. But what if we already generated the embeddings and stored them in Nile. In that case, you still initialize `NileVectorStore` as above, but instead of `VectorStoreIndex.from_documents(...)` you use this:
``` index = VectorStoreIndex.from_vector_store(vector_store=vector_store) query_engine = index.as_query_engine( vector_store_kwargs={ "tenant_id": str(tenant_id_modamart), }, ) response = query_engine.query("What action items do we need to follow up on?")

print(response) ```
``` The action items to follow up on include sending the customer detailed testimonials about the lightweight and warm qualities of the jackets, providing the customer with a sizing guide, and emailing the customer a 10% discount on their first purchase. ```

## Using ANN indexes for approximate nearest neighbor search
Nile supports all indexes supported by pgvector - IVFFlat and HNSW. IVFFlat is faster, uses fewer resources and is simple to tune. HNSW uses more resources to create and use, and is more challenging to tune but has great accuracy/speed tradeoffs. Lets see how to use indexes, even though a 2-document example doesn’t actually require them.
### IVFFlat Index
IVFFlat indexes work by separating the vector space into regions called “lists”, first finding the nearest lists and then searching for the nearest neighbors within these lists. You specify the number of lists (`nlists`) during index creation, and then when querying, you can specify how many nearest lists will be used in the search (`ivfflat_probes`).
``` try: vector_store.create_index(index_type=IndexType.PGVECTOR_IVFFLAT, nlists=10) except Exception as e: # This will throw an error if the index already exists, which may be expected print(e)

nexiv_query_engine = index.as_query_engine( similarity_top_k=3, vector_store_kwargs={ "tenant_id": str(tenant_id_nexiv), "ivfflat_probes": 10, }, )

print( nexiv_query_engine.query("What action items do we need to follow up on?") )

``` Index documents_embedding_idx already exists ```
### HNSW Index
HNSW indexes work by separating the vector space into a multi-layer graph where each layer contains connections between points at varying levels of granularity. During a search, it navigates from coarse to finer layers, identifying the nearest neighbors in the data. During index creation, you specify the maximum number of connections in a layer (`m`) and the number of candidate vectors considered when building the graph (`ef_construction`). While querying, you can specify the size of the candidate list that will be searched (`hnsw_ef`).
``` try: vector_store.create_index( index_type=IndexType.PGVECTOR_HNSW, m=16, ef_construction=64 ) except Exception as e: # This will throw an error if the index already exists, which may be expected print(e)

nexiv_query_engine = index.as_query_engine( similarity_top_k=3, vector_store_kwargs={ "tenant_id": str(tenant_id_nexiv), "hnsw_ef": 10, }, )

print(nexiv_query_engine.query("Did we mention any pricing?"))
vector_store.drop_index() ```
## Additional VectorStore operations
### Metadata Filters
`NileVectorStore` also supports filtering vectors based on metadata. For example, when we loaded the documents, we included `category` metadata for each document. We can now use this information to filter the retrieved documents. Note that this filtering is **in addition** to the tenant filter. In a tenant-aware vector store, the tenant filter is mandatory, in order to prevent accidental data leaks.
``` filters = MetadataFilters( filters=[ MetadataFilter( key="category", operator=FilterOperator.EQ, value="Retail" ), ] )

nexiv_query_engine_filtered = index.as_query_engine( similarity_top_k=3, filters=filters, vector_store_kwargs={"tenant_id": str(tenant_id_nexiv)}, ) print( "test query on nexiv with filter on category = Retail (should return empty): ", nexiv_query_engine_filtered.query("What were the customer pain points?"), ) ```

``` test query on nexiv with filter on category = Retail (should return empty): Empty Response ```
### Deleting Documents
Deleting documents can be quite important. Especially if some of your tenants are in a region where GDPR is required.
``` ref_doc_id = "nexiv_doc_id_1" vector_store.delete(ref_doc_id, tenant_id=tenant_id_nexiv)

# Query the data again print( "test query on nexiv after deletion (should return empty): ", nexiv_query_engine.query("What were the customer pain points?"), ) ```

``` test query on nexiv after deletion (should return empty): Empty Response ```

[1] https://console.thenile.dev/?utm_campaign=partnerlaunch\&utm_source=llamaindex\&utm_medium=docs
[2] https://www.thenile.dev/docs/partners/llama
[3] https://www.thenile.dev/docs/ai-embeddings
[4] https://www.thenile.dev/docs/ai-embeddings/pg_vector
[5] https://www.thenile.dev/blog/pgvector_myth_debunking
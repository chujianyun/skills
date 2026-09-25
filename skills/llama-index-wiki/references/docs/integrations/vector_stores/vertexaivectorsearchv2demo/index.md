# developers.llamaindex.ai/python/framework/integrations/vector_stores/vertexaivectorsearchv2demo/index.md
> https://developers.llamaindex.ai/python/framework/integrations/vector_stores/vertexaivectorsearchv2demo/index.md

--- title: Google Vertex AI Vector Search v2.0 | Developer Documentation ---
This notebook demonstrates how to use **Vertex AI Vector Search v2.0** with LlamaIndex.

> Vertex AI Vector Search v2.0 [1] introduces a simplified **collection-based architecture** that eliminates the need for separate index creation and endpoint deployment.

## v2.0 vs v1.0
| Feature | v1.0 | v2.0 | | ------------- | --------------------------------- | ----------------- | | Architecture | Index + Endpoint | Collection | | Setup Steps | Create index → Deploy to endpoint | Create collection | | GCS Bucket | Required for batch updates | Not needed | | Hybrid Search | Not supported | Supported |

**Note**: For v1.0 usage, see VertexAIVectorSearchDemo.ipynb
## Install Dependencies
Install LlamaIndex with v2 support:
> **Note**: V2 support requires `llama-index-vector-stores-vertexaivectorsearch` version that supports Vertex AI Vector Search v2.0 API.
``` # Install with v2 support (the [v2] extra installs google-cloud-vectorsearch) # !pip install 'llama-index-vector-stores-vertexaivectorsearch[v2]' llama-index-embeddings-vertex llama-index-llms-vertex ```

### Authentication (if using Colab):
``` # Colab authentication. import sys

if "google.colab" in sys.modules: from google.colab import auth
auth.authenticate_user() print("Authenticated") ```
## Configuration
Set your Google Cloud project details:
``` # Google Cloud Configuration PROJECT_ID = "your-project-id" # @param {type:"string"} REGION = "us-central1" # @param {type:"string"} COLLECTION_ID = "llamaindex-demo-collection" # @param {type:"string"}

# Embedding dimensions (768 for text-embedding-004) EMBEDDING_DIMENSION = 768 ```
## Create a v2 Collection
Unlike v1.0 which requires creating an index and deploying it to an endpoint, v2.0 only requires creating a collection.
**Important for Hybrid Search:** The collection schema below is configured to support all hybrid search features:
- **Text Search**: String fields (`text`, `category`, `color`) can be searched with keywords - **Semantic Search**: The `vertex_embedding_config` enables auto-embeddings for `SEMANTIC_HYBRID` mode - **Filtering**: Numeric (`price`) and string fields support metadata filtering
``` from google.cloud import vectorsearch_v1beta
# Initialize the client client = vectorsearch_v1beta.VectorSearchServiceClient()
# Check if collection already exists parent = f"projects/{PROJECT_ID}/locations/{REGION}" collection_name = f"{parent}/collections/{COLLECTION_ID}"

# Collection schema that supports: # - Dense vector search (embedding field) # - Text search on text, category, color fields (for HYBRID mode) # - Semantic search with auto-embeddings (for SEMANTIC_HYBRID mode) # - Filtering on price, category, color fields collection_config = { "data_schema": { "type": "object", "properties": { "text": {"type": "string"}, # Main text content (searchable) "ref_doc_id": {"type": "string"}, # Document reference "price": {"type": "number"}, # Filterable numeric field "color": {"type": "string"}, # Filterable/searchable string "category": {"type": "string"}, # Filterable/searchable string }, }, "vector_schema": { "embedding": { "dense_vector": { "dimensions": EMBEDDING_DIMENSION, # Auto-embedding config enables SEMANTIC_HYBRID mode # Vertex AI will auto-generate embeddings for semantic search "vertex_embedding_config": { "model_id": "text-embedding-004", "text_template": "{text}", "task_type": "RETRIEVAL_DOCUMENT", }, } }, }, }

try: request = vectorsearch_v1beta.GetCollectionRequest(name=collection_name) collection = client.get_collection(request=request) print(f"Collection already exists: {collection.name}") print( "Note: If you need hybrid search features, delete and recreate with the schema above." ) except Exception as e: if "404" in str(e) or "NotFound" in str(e): print(f"Creating collection: {COLLECTION_ID}") print( "Schema includes: text search fields, auto-embedding config for semantic search" )

request = vectorsearch_v1beta.CreateCollectionRequest( parent=parent, collection_id=COLLECTION_ID, collection=collection_config, ) operation = client.create_collection(request=request) collection = operation.result() print(f"Collection created: {collection.name}") else: raise e ```

## Set Up LlamaIndex Components
``` # Imports from llama_index.core import Settings, StorageContext, VectorStoreIndex from llama_index.core.schema import TextNode from llama_index.core.vector_stores.types import ( MetadataFilters, MetadataFilter, FilterOperator, ) from llama_index.embeddings.vertex import VertexTextEmbedding from llama_index.llms.vertex import Vertex from llama_index.vector_stores.vertexaivectorsearch import VertexAIVectorStore

# Authentication - get default credentials import google.auth
credentials, project = google.auth.default() print(f"Authenticated with project: {project}") ```
``` # Configure embedding model embed_model = VertexTextEmbedding( model_name="text-embedding-004", project=PROJECT_ID, location=REGION, credentials=credentials, )

# Configure LLM llm = Vertex( model="gemini-2.0-flash", project=PROJECT_ID, location=REGION, credentials=credentials, )

# Set as defaults Settings.embed_model = embed_model Settings.llm = llm

print("Embedding model and LLM configured successfully!") ```
## Create v2 Vector Store
Creating a v2 vector store is simple - just specify `api_version="v2"` and your `collection_id`:
``` # Create v2 vector store vector_store = VertexAIVectorStore( api_version="v2", # Use v2 API project_id=PROJECT_ID, region=REGION, collection_id=COLLECTION_ID, # No index_id, endpoint_id, or gcs_bucket_name needed! )

print(f"Vector store created with api_version={vector_store.api_version}") ```
## Add Documents
### Simple Text Nodes
``` # Create some sample text nodes texts = [ "LlamaIndex is a data framework for LLM applications.", "Vertex AI Vector Search provides scalable vector similarity search.", "RAG combines retrieval with generation for better AI responses.", "Embeddings convert text into numerical vectors for similarity matching.", ]

# Create nodes with embeddings nodes = [ TextNode(text=text, embedding=embed_model.get_text_embedding(text)) for text in texts ]

# Add to vector store ids = vector_store.add(nodes) print(f"Added {len(ids)} nodes to vector store") ```

### Nodes with Metadata
Add nodes with metadata for filtering and hybrid search:
``` # Sample product data with metadata products = [ { "text": "Comfortable blue cotton t-shirt, perfect for casual wear", "color": "blue", "category": "tops", "price": 29.99, }, { "text": "Professional black dress pants for office meetings", "color": "black", "category": "bottoms", "price": 79.99, }, { "text": "Warm green wool sweater for cold winter days", "color": "green", "category": "tops", "price": 59.99, }, { "text": "Lightweight blue running shorts with pockets", "color": "blue", "category": "bottoms", "price": 34.99, }, { "text": "Elegant red silk blouse for formal occasions", "color": "red", "category": "tops", "price": 89.99, }, ]

# Create nodes with metadata # Note: Include "text" in metadata for TEXT_SEARCH to work on the text field product_nodes = [ TextNode( text=p["text"], embedding=embed_model.get_text_embedding(p["text"]), metadata={ "text": p["text"], "color": p["color"], "category": p["category"], "price": p["price"], }, ) for p in products ]

# Add to vector store product_ids = vector_store.add(product_nodes) print(f"Added {len(product_ids)} product nodes with metadata") ```

## Query the Vector Store
### Simple Similarity Search
``` # Create index from vector store storage_context = StorageContext.from_defaults(vector_store=vector_store) index = VectorStoreIndex.from_vector_store( vector_store=vector_store, embed_model=embed_model )

# Create retriever retriever = index.as_retriever(similarity_top_k=3)
# Query results = retriever.retrieve("comfortable clothing for everyday wear")
print("Search Results:") print("-" * 60) for result in results: print(f"Score: {result.get_score():.3f}") print(f"Text: {result.get_text()[:100]}...") print(f"Metadata: {result.metadata}") print("-" * 60) ```

### Search with Metadata Filters
``` # Filter by color filters = MetadataFilters(filters=[MetadataFilter(key="color", value="blue")])

retriever = index.as_retriever(filters=filters, similarity_top_k=3) results = retriever.retrieve("casual clothing")
print("Blue items only:") print("-" * 60) for result in results: print( f"Score: {result.get_score():.3f} | Color: {result.metadata.get('color')}" ) print(f"Text: {result.get_text()[:80]}...") print("-" * 60) ```

``` # Filter by price range filters = MetadataFilters( filters=[ MetadataFilter(key="price", operator=FilterOperator.LT, value=50.0), ] )

retriever = index.as_retriever(filters=filters, similarity_top_k=3) results = retriever.retrieve("clothing")
print("Items under $50:") print("-" * 60) for result in results: print( f"Score: {result.get_score():.3f} | Price: ${result.metadata.get('price')}" ) print(f"Text: {result.get_text()[:80]}...") print("-" * 60) ```

## RAG Query with LLM
Use the vector store with an LLM for retrieval-augmented generation:
``` # Create query engine query_engine = index.as_query_engine(similarity_top_k=3)

# Ask a question response = query_engine.query( "What blue clothing items do you have and what are their prices?" )

print( "Question: What blue clothing items do you have and what are their prices?" ) print("-" * 60) print(f"Answer: {response.response}") print("-" * 60) print("Sources:") for node in response.source_nodes: print(f" - {node.text[:60]}... (score: {node.score:.3f})") ```

## v2-Only Features
### Delete Specific Nodes
``` # Delete specific nodes by ID # vector_store.delete_nodes(node_ids=["node_id_1", "node_id_2"]) print("delete_nodes() - Delete specific nodes by their IDs") ```

### Clear All Data (v2 only)
v2 supports clearing all data from a collection - this is NOT available in v1:
``` # Clear all data from the collection # WARNING: This deletes ALL data in the collection! # vector_store.clear() print("clear() - Clears all data from collection (v2 only!)") ```

## Hybrid Search (v2 Only)

v2 supports **hybrid search**, combining vector similarity with text-based search for improved retrieval quality. This is particularly useful when you want to leverage both semantic understanding (vectors) and exact keyword matching (text search).

### Supported Query Modes
| Mode | Description | Use Case | | ----------------- | ------------------------------ | ------------------------------ | | `DEFAULT` | Dense vector similarity search | Standard semantic search | | `TEXT_SEARCH` | Full-text keyword search | Exact keyword matching | | `HYBRID` | Vector + Text with RRF fusion | Best of both worlds | | `SEMANTIC_HYBRID` | Vector + Semantic search | Auto-embedding semantic search |

### Ranker Options
| Ranker | Description | | --------------- | ------------------------------------------- | | `rrf` (default) | Reciprocal Rank Fusion with alpha weighting | | `vertex` | AI-powered semantic ranking via Vertex AI |

### Create Hybrid-Enabled Vector Store
To enable hybrid search, set `enable_hybrid=True` and specify which fields to use for text search:
``` # Create hybrid-enabled vector store hybrid_vector_store = VertexAIVectorStore( api_version="v2", project_id=PROJECT_ID, region=REGION, collection_id=COLLECTION_ID, enable_hybrid=True, text_search_fields=["text", "category", "color"], # Fields for text search default_hybrid_alpha=0.5, # Balance between vector and text (0=text only, 1=vector only) )

print( f"Hybrid vector store created with enable_hybrid={hybrid_vector_store.enable_hybrid}" ) ```

### TEXT\_SEARCH Mode - Keyword Search
Use `TEXT_SEARCH` mode for full-text keyword matching. This is useful when you want exact keyword matches rather than semantic similarity:
``` from llama_index.core.vector_stores.types import ( VectorStoreQuery, VectorStoreQueryMode, )

# TEXT_SEARCH: Full-text keyword search only text_query = VectorStoreQuery( query_str="blue cotton", # Keywords to search for mode=VectorStoreQueryMode.TEXT_SEARCH, similarity_top_k=3, )

results = hybrid_vector_store.query(text_query)
print("TEXT_SEARCH Results (keyword matching):") print("-" * 60) for i, node in enumerate(results.nodes): print(f"{i+1}. {node.text[:80]}...") print(f" Metadata: {node.metadata}") print() ```

### HYBRID Mode - Vector + Text Search
Use `HYBRID` mode to combine vector similarity with text search. The `alpha` parameter controls the balance:
- `alpha=1.0` - Pure vector search - `alpha=0.5` - Balanced - `alpha=0.0` - Pure text search
``` # Compare different alpha values print("Comparing alpha values:") print("=" * 60)

for alpha in [1.0, 0.5, 0.0]: query = VectorStoreQuery( query_embedding=embed_model.get_query_embedding( "warm winter clothing" ), query_str="sweater green", # Keywords favor green sweater mode=VectorStoreQueryMode.HYBRID, alpha=alpha, similarity_top_k=2, ) results = hybrid_vector_store.query(query)

label = ( "vector only" if alpha == 1.0 else "text only" if alpha == 0.0 else "balanced" ) print(f"\nalpha={alpha} ({label}):") for node in results.nodes: print(f" - {node.text[:60]}... | color={node.metadata.get('color')}") ```

### SEMANTIC\_HYBRID Mode

`SEMANTIC_HYBRID` combines your dense vector search with Vertex AI’s built-in semantic search. This requires the collection to have `vertex_embedding_config` configured for auto-embeddings.

``` # SEMANTIC_HYBRID: Vector + Vertex AI's semantic search # Note: Requires collection with vertex_embedding_config

semantic_query = VectorStoreQuery( query_embedding=embed_model.get_query_embedding( "professional work attire" ), query_str="formal office clothing", # Semantic search text mode=VectorStoreQueryMode.SEMANTIC_HYBRID, similarity_top_k=3, )

try: results = hybrid_vector_store.query(semantic_query) print("SEMANTIC_HYBRID Results:") print("-" * 60) for i, node in enumerate(results.nodes): print(f"{i+1}. {node.text[:80]}...") except Exception as e: print( f"SEMANTIC_HYBRID requires collection with vertex_embedding_config: {e}" ) ```

### Using VertexRanker
Instead of RRF, you can use Vertex AI’s semantic ranker for AI-powered result ranking:
``` # Create vector store with VertexRanker vertex_ranker_store = VertexAIVectorStore( api_version="v2", project_id=PROJECT_ID, region=REGION, collection_id=COLLECTION_ID, enable_hybrid=True, text_search_fields=["text", "category"], hybrid_ranker="vertex", # Use Vertex AI's semantic ranker vertex_ranker_model="semantic-ranker-default@latest", vertex_ranker_title_field="category", # Field to use as title vertex_ranker_content_field="text", # Field to use as content )

# Query with VertexRanker query = VectorStoreQuery( query_embedding=embed_model.get_query_embedding("casual everyday wear"), query_str="comfortable shirt", mode=VectorStoreQueryMode.HYBRID, similarity_top_k=3, )

results = vertex_ranker_store.query(query)
print("HYBRID with VertexRanker Results:") print("-" * 60) for i, node in enumerate(results.nodes): print(f"{i+1}. {node.text[:80]}...") print(f" Category: {node.metadata.get('category')}") print() ```

### Hybrid Search with Query Engine (RAG)
You can also use hybrid search with the standard LlamaIndex query engine for RAG applications:
``` # Create index with hybrid-enabled vector store hybrid_storage_context = StorageContext.from_defaults( vector_store=hybrid_vector_store ) hybrid_index = VectorStoreIndex.from_vector_store( vector_store=hybrid_vector_store, embed_model=embed_model, )

# Create query engine with hybrid mode hybrid_query_engine = hybrid_index.as_query_engine( vector_store_query_mode=VectorStoreQueryMode.HYBRID, similarity_top_k=3, alpha=0.7, # Favor vector search slightly )

# Ask a question using RAG with hybrid retrieval response = hybrid_query_engine.query( "What comfortable blue clothing options are available?" )

print("Question: What comfortable blue clothing options are available?") print("-" * 60) print(f"Answer: {response.response}") print("-" * 60) print("Sources:") for node in response.source_nodes: print(f" - {node.text[:60]}... (score: {node.score:.3f})") ```

### Hybrid Search Parameters Reference
| Parameter | Type | Default | Description | | ----------------------------- | ----------- | ---------------------------------- | ------------------------------------- | | `enable_hybrid` | `bool` | `False` | Enable hybrid search modes | | `text_search_fields` | `List[str]` | `None` | Data fields for text search | | `embedding_field` | `str` | `"embedding"` | Vector field name | | `default_hybrid_alpha` | `float` | `0.5` | Default RRF weight (0=text, 1=vector) | | `hybrid_ranker` | `str` | `"rrf"` | Ranker: “rrf” or “vertex” | | `semantic_task_type` | `str` | `"RETRIEVAL_QUERY"` | Task type for SemanticSearch | | `vertex_ranker_model` | `str` | `"semantic-ranker-default@latest"` | VertexRanker model | | `vertex_ranker_title_field` | `str` | `None` | Title field for VertexRanker | | `vertex_ranker_content_field` | `str` | `None` | Content field for VertexRanker |

## Clean Up
Delete the collection when done to avoid charges:
``` CLEANUP = False # Set to True to delete the collection
if CLEANUP: from google.cloud import vectorsearch_v1beta
client = vectorsearch_v1beta.VectorSearchServiceClient() collection_name = ( f"projects/{PROJECT_ID}/locations/{REGION}/collections/{COLLECTION_ID}" )

print(f"Deleting collection: {collection_name}") client.delete_collection(name=collection_name) print("Collection deleted.") ```

## Summary
This notebook demonstrated:
1. **Simple Setup**: v2 only requires a collection - no index/endpoint deployment
2. **Easy Integration**: Just add `api_version="v2"` to use the new API
3. **Same Interface**: All LlamaIndex operations (add, query, delete) work the same
4. **New Features**: v2 adds `clear()` method not available in v1
5. **Hybrid Search**: Combine vector and text search for better retrieval:
- `TEXT_SEARCH` - Full-text keyword search - `HYBRID` - Vector + text with RRF fusion - `SEMANTIC_HYBRID` - Vector + semantic search - VertexRanker for AI-powered ranking

### Migration from v1
``` # v1 (old) vector_store = VertexAIVectorStore( project_id="...", region="...", index_id="projects/.../indexes/123", endpoint_id="projects/.../indexEndpoints/456", gcs_bucket_name="my-bucket" )

# v2 (new) vector_store = VertexAIVectorStore( api_version="v2", project_id="...", region="...", collection_id="my-collection" )

# v2 with hybrid search vector_store = VertexAIVectorStore( api_version="v2", project_id="...", region="...", collection_id="my-collection", enable_hybrid=True, text_search_fields=["text", "title"], ) ```

For detailed migration instructions, see V2\_MIGRATION.md [2]

[1] https://cloud.google.com/vertex-ai/docs/vector-search/overview
[2] https://github.com/run-llama/llama_index/blob/main/llama-index-integrations/vector_stores/llama-index-vector-stores-vertexaivectorsearch/V2_MIGRATION.md
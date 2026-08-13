# developers.llamaindex.ai/python/framework/integrations/vector_stores/vectorxdemo/index.md
> https://developers.llamaindex.ai/python/framework/integrations/vector_stores/vectorxdemo/index.md

--- title: 1. Installation | Developer Documentation ---
``` !pip install vecx-llamaindex ```
# 2. Setting up VectorX and OpenAI credentials
``` import os from llama_index.embeddings.openai import OpenAIEmbedding from vecx.vectorx import VectorX
# Set API keys os.environ["OPENAI_API_KEY"] = "sk-proj..." vecx_api_token = "..."
# Initialize VectorX client vx = VectorX(token=vecx_api_token) ```
``` encryption_key = vx.generate_key() # Make sure to save this key securely - you'll need it to access your encrypted vectors print("Encryption key:", encryption_key) ```
# 3. Creating Sample Documents
``` from llama_index.core import Document

# Create sample documents with different categories and metadata documents = [ Document( text="Python is a high-level, interpreted programming language known for its readability and simplicity.", metadata={ "category": "programming", "language": "python", "difficulty": "beginner", }, ), Document( text="JavaScript is a scripting language that enables interactive web pages and is an essential part of web applications.", metadata={ "category": "programming", "language": "javascript", "difficulty": "intermediate", }, ), Document( text="Machine learning is a subset of artificial intelligence that provides systems the ability to automatically learn and improve from experience.", metadata={ "category": "ai", "field": "machine_learning", "difficulty": "advanced", }, ), Document( text="Deep learning is part of a broader family of machine learning methods based on artificial neural networks with representation learning.", metadata={ "category": "ai", "field": "deep_learning", "difficulty": "advanced", }, ), Document( text="Vector databases are specialized database systems designed to store and query high-dimensional vectors for similarity search.",

metadata={ "category": "database", "type": "vector", "difficulty": "intermediate", }, ), Document( text="VectorX is an encrypted vector database that provides secure and private vector search capabilities.", metadata={ "category": "database", "type": "vector", "product": "vectorx", "difficulty": "intermediate", }, ), ]

print(f"Created {len(documents)} sample documents") ```
``` vx.delete_index("llamaIndex_testing") ```
``` vx.list_indexes() ```
``` index = vx.get_index("llamaIndex_testing", encryption_key) index.describe() ```
# 4. Setting up VectorX with LlamaIndex
``` from vecx_llamaindex import VectorXVectorStore from llama_index.core import StorageContext import time
# Create a unique index name with timestamp to avoid conflicts timestamp = int(time.time()) index_name = f"llamaIndex_testing"
# Set up the embedding model embed_model = OpenAIEmbedding()
# Get the embedding dimension dimension = 1536 # OpenAI's default embedding dimension
# Initialize the VectorX vector store vector_store = VectorXVectorStore.from_params( api_token=vecx_api_token, encryption_key=encryption_key, index_name=index_name, dimension=dimension, space_type="cosine", # Can be "cosine", "l2", or "ip" )

# Create storage context with our vector store storage_context = StorageContext.from_defaults(vector_store=vector_store)
print(f"Initialized VectorX vector store with index: {index_name}") ```
# 5. Creating a Vector Index from Documents
``` from llama_index.core import VectorStoreIndex
# Create a vector index index = VectorStoreIndex.from_documents( documents, storage_context=storage_context, embed_model=embed_model )
print("Vector index created successfully") ```
``` def reconnect_to_index(api_token, encryption_key, index_name): # Initialize the vector store with existing index vector_store = VectorXVectorStore.from_params( api_token=api_token, encryption_key=encryption_key, index_name=index_name, )

return index ```
``` # Create a query engine index = reconnect_to_index(vecx_api_token, encryption_key, index_name) query_engine = index.as_query_engine()
# Ask a question response = query_engine.query("Which is the tallest mountain in the world?")
# print("Query: What are javascript?") print("Response:") print(response) ```
# 6. Basic Retrieval with Query Engine
``` query_embedding = embed_model.get_text_embedding( "What is programming language?" )
vec_index = vx.get_index(index_name, encryption_key)
results = vec_index.query( vector=query_embedding, top_k=1, include_vectors=True ) ```
``` print(results) ```
``` text = "Mount Kilimanjaro is the tallest mountain in africa"
vector = embed_model.get_text_embedding(text)
vec_index.upsert( [ { "id": "vector_1", "vector": vector, "meta": { text: text, }, } ] ) ```

# 7. Using Metadata Filters
``` from llama_index.core.vector_stores.types import ( MetadataFilters, MetadataFilter, FilterOperator, )
# Create a filtered retriever to only search within AI-related documents ai_filter = MetadataFilter( key="category", value="ai", operator=FilterOperator.EQ ) ai_filters = MetadataFilters(filters=[ai_filter])
# Create a filtered query engine filtered_query_engine = index.as_query_engine(filters=ai_filters)
# Ask a general question but only using AI documents response = filtered_query_engine.query("What is vector database?")
# print("Filtered Query (AI category only): What is learning from data?") print("Response:") print(response) ```
# 8. Advanced Filtering with Multiple Conditions
``` # Create a more complex filter: database category AND intermediate difficulty category_filter = MetadataFilter( key="category", value="ai", operator=FilterOperator.EQ ) difficulty_filter = MetadataFilter( key="difficulty", value="intermediate", operator=FilterOperator.EQ )

complex_filters = MetadataFilters(filters=[category_filter, difficulty_filter])
# Create a query engine with the complex filters complex_filtered_engine = index.as_query_engine(filters=complex_filters)
# Query with the complex filters response = complex_filtered_engine.query("what is ML")
print( "Complex Filtered Query (database category AND intermediate difficulty): Tell me about databases" ) print("Response:") print(response) ```
# 9. Custom Retriever Setup
``` from llama_index.core.retrievers import VectorIndexRetriever
# Create a retriever with custom parameters retriever = VectorIndexRetriever( index=index, similarity_top_k=3, # Return top 3 most similar results filters=ai_filters, # Use our AI category filter from before )
# Retrieve nodes for a query nodes = retriever.retrieve("What is deep learning?")
print( f"Retrieved {len(nodes)} nodes for query: 'What is deep learning?' (with AI category filter)" ) print("\nRetrieved content:") for i, node in enumerate(nodes): print(f"\nNode {i+1}:") print(f"Text: {node.node.text}") print(f"Metadata: {node.node.metadata}") print(f"Score: {node.score:.4f}") ```

# 10. Using a Custom Retriever with a Query Engine
``` from llama_index.core.query_engine import RetrieverQueryEngine
# Create a query engine with our custom retriever custom_query_engine = RetrieverQueryEngine.from_args( retriever=retriever, verbose=True, # Enable verbose mode to see the retrieved nodes )
# Query using the custom retriever query engine response = custom_query_engine.query( "Explain the difference between machine learning and deep learning" )
print("\nFinal Response:") print(response) ```
# 11. Direct VectorStore Querying
``` from llama_index.core.vector_stores.types import VectorStoreQuery
# Generate an embedding for our query query_text = "What are vector databases?" query_embedding = embed_model.get_text_embedding(query_text)
# Create a VectorStoreQuery vector_store_query = VectorStoreQuery( query_embedding=query_embedding, similarity_top_k=2, filters=MetadataFilters( filters=[ MetadataFilter( key="category", value="database", operator=FilterOperator.EQ ) ] ), )

# Execute the query directly on the vector store query_result = vector_store.query(vector_store_query)
print(f"Direct VectorStore query: '{query_text}'") print( f"Retrieved {len(query_result.nodes)} results with database category filter:" ) for i, (node, score) in enumerate( zip(query_result.nodes, query_result.similarities) ): print(f"\nResult {i+1}:") print(f"Text: {node.text}") print(f"Metadata: {node.metadata}") print(f"Similarity score: {score:.4f}") ```

``` # To reconnect to an existing index in a future session, you would use: def reconnect_to_index(api_token, encryption_key, index_name): # Initialize the vector store with existing index vector_store = VectorXVectorStore.from_params( api_token=api_token, encryption_key=encryption_key, index_name=index_name, )

# Create storage context storage_context = StorageContext.from_defaults(vector_store=vector_store)
# Load the index index = VectorStoreIndex.from_vector_store( vector_store, embed_model=OpenAIEmbedding() )
return index
# Example usage (commented out as we already have our index) # reconnected_index = reconnect_to_index(vecx_api_token, encryption_key, index_name) # query_engine = reconnected_index.as_query_engine() # response = query_engine.query("What is VectorX?") # print(response)
print(f"To reconnect to this index in the future, use:\n") print(f"API Token: {vecx_api_token}") print(f"Encryption Key: {encryption_key}") print(f"Index Name: {index_name}") ```
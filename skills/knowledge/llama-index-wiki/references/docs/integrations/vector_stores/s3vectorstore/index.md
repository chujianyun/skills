# developers.llamaindex.ai/python/framework/integrations/vector_stores/s3vectorstore/index.md
> https://developers.llamaindex.ai/python/framework/integrations/vector_stores/s3vectorstore/index.md

--- title: S3VectorStore Integration | Developer Documentation ---
This is a vector store integration for LlamaIndex that uses S3Vectors.

Find out more about S3Vectors [1].

This notebook will assume that you have already created a S3 vector bucket (and possibly also an index).
## Installation
``` %pip install llama-index-vector-stores-s3 llama-index-embeddings-openai ```
## Usage
### Creating the vector store object
You can create a new vector index in an existing S3 bucket.
If you don’t have S3 credentials configured in your environment, you can provide a boto3 session with credentials.

vector_store = S3VectorStore.create_index_from_bucket( # S3 bucket name or ARN bucket_name_or_arn="test-bucket", # Name for the new index index_name="my-index", # Vector dimension (e.g., 1536 for OpenAI embeddings) dimension=1536, # Distance metric: "cosine", "euclidean", etc. distance_metric="cosine", # Data type for vectors data_type="float32", # Batch size for inserting vectors (max 500) insert_batch_size=500, # Metadata keys that won't be filterable non_filterable_metadata_keys=["custom_field"], # Optional: provide a boto3 session for custom AWS configuration # sync_session=boto3.Session(...) ) ```

Or, you can use an existing vector index in an existing S3 bucket.
``` from llama_index.vector_stores.s3 import S3VectorStore import boto3

vector_store = S3VectorStore( # Index name or ARN index_name_or_arn="my-index", # S3 bucket name or ARN bucket_name_or_arn="test-bucket", # Data type for vectors (must match index) data_type="float32", # Distance metric (must match index) distance_metric="cosine", # Batch size for inserting vectors (max 500) insert_batch_size=500, # Optional: specify metadata field containing text if you already have a populated index # text_field="content", # Optional: provide a boto3 session for custom AWS configuration # sync_session=boto3.Session(...), ) ```

### Using the vector store with an index
Once you have a vector store, you can use it with an index:
``` from llama_index.core import ( VectorStoreIndex, StorageContext, SimpleDirectoryReader, Document, ) from llama_index.embeddings.openai import OpenAIEmbedding

# Load some data # documents = SimpleDirectoryReader("data").load_data()
# Or create new documents documents = [ Document(text="Hello, world!", metadata={"key": "1"}), Document(text="Hello, world! 2", metadata={"key": "2"}), ]

# Create a new index index = VectorStoreIndex.from_documents( documents, storage_context=StorageContext.from_defaults(vector_store=vector_store), # optional: set the embed model embed_model=OpenAIEmbedding(model="text-embedding-3-small", api_key="..."), )

# Or reload from an existing index # index = VectorStoreIndex.from_vector_store( # vector_store=vector_store, # # optional: set the embed model # # embed_model=embed_model, # ) ```

``` nodes = index.as_retriever(similarity_top_k=1).retrieve("Hello, world!") print(nodes[0].text) ```

You can also use filters to help you retrieve the correct nodes!
``` from llama_index.core.vector_stores.types import ( MetadataFilters, MetadataFilter, FilterOperator, FilterCondition, )

nodes = index.as_retriever( similarity_top_k=2, filters=MetadataFilters( filters=[ MetadataFilter( key="key", value="2", operator=FilterOperator.EQ, ), ], condition=FilterCondition.AND, ), ).retrieve("Hello, world!")

print(nodes[0].text) ```
``` Hello, world! 2 ```
### Using the vector store directly
You can also use the vector store directly:
``` from llama_index.core.schema import TextNode from llama_index.core.vector_stores.types import VectorStoreQuery from llama_index.embeddings.openai import OpenAIEmbedding
# embed nodes nodes = [ TextNode(text="Hello, world!"), TextNode(text="Hello, world! 2"), ]

embed_model = OpenAIEmbedding(model="text-embedding-3-small", api_key="...") embeddings = embed_model.get_text_embedding_batch([n.text for n in nodes]) for node, embedding in zip(nodes, embeddings): node.embedding = embedding
# add nodes to the vector store vector_store.add(nodes)
# query the vector store query = VectorStoreQuery( query_embedding=embed_model.get_query_embedding("Hello, world!"), similarity_top_k=2, ) results = vector_store.query(query) print(results.nodes[0].text) ```

``` Hello, world! ```

[1] https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-vectors-getting-started.html
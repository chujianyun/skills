# developers.llamaindex.ai/python/framework/integrations/embeddings/isaacus/index.md
> https://developers.llamaindex.ai/python/framework/integrations/embeddings/isaacus/index.md

--- title: Isaacus Embeddings | Developer Documentation ---

The `llama-index-embeddings-isaacus` package contains LlamaIndex integrations for building applications with Isaacus’ legal AI embedding models. This integration allows you to easily connect to and use the **Kanon 2 Embedder** - the world’s most accurate legal embedding model on the Massive Legal Embedding Benchmark (MLEB) [1].

Isaacus embeddings support task-specific optimization:
- `task="retrieval/query"`: Optimize embeddings for search queries - `task="retrieval/document"`: Optimize embeddings for documents to be indexed
In this notebook, we will demonstrate using Isaacus Embeddings for legal document retrieval.
## Installation
Install the necessary integrations.
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.
``` %pip install llama-index-embeddings-isaacus %pip install llama-index-llms-openai ```

``` %pip install llama-index ```
## Setup
### Get your Isaacus API key
1. Create an account at Isaacus Platform [2] 2. Add a payment method [3] to claim your free credits [4] 3. Create an API key [5]

# Set your Isaacus API key isaacus_api_key = "<API_KEY>" os.environ["ISAACUS_API_KEY"] = isaacus_api_key ```

## Basic Usage
### Get a Single Embedding
``` from llama_index.embeddings.isaacus import IsaacusEmbedding
# Initialize the Isaacus Embedding model embed_model = IsaacusEmbedding( api_key=isaacus_api_key, model="kanon-2-embedder", )

# Get a single embedding embedding = embed_model.get_text_embedding( "This agreement shall be governed by the laws of Delaware." )

print(f"Embedding dimension: {len(embedding)}") print(f"First 5 values: {embedding[:5]}") ```
### Get Batch Embeddings
``` # Get embeddings for multiple legal texts legal_texts = [ "The parties agree to binding arbitration.", "Confidential information shall not be disclosed.", "This contract may be terminated with 30 days notice.", ]

embeddings = embed_model.get_text_embedding_batch(legal_texts)
print(f"Number of embeddings: {len(embeddings)}") print(f"Each embedding has {len(embeddings[0])} dimensions") ```
## Task-Specific Embeddings
Isaacus embeddings support different tasks for optimal performance:
- **`retrieval/document`**: For documents to be indexed - **`retrieval/query`**: For search queries
Using the appropriate task improves retrieval accuracy.
``` # For documents (use when indexing) doc_embed_model = IsaacusEmbedding( api_key=isaacus_api_key, task="retrieval/document", )

doc_embedding = doc_embed_model.get_text_embedding( "The Company has the right to terminate this agreement." )

print(f"Document embedding dimension: {len(doc_embedding)}") ```
``` # For queries (automatically used by get_query_embedding) query_embedding = embed_model.get_query_embedding( "What are the termination conditions?" )

print(f"Query embedding dimension: {len(query_embedding)}") ```
## Dimensionality Reduction
You can reduce the embedding dimensionality for faster search and lower storage costs:
``` # Use reduced dimensions (default is 1792) embed_model_512 = IsaacusEmbedding( api_key=isaacus_api_key, dimensions=512, )

embedding_512 = embed_model_512.get_text_embedding("Legal text example")
print(f"Reduced embedding dimension: {len(embedding_512)}") ```
## Full RAG Example with Legal Documents
Now let’s build a complete RAG pipeline using Isaacus embeddings with a legal document (Uber’s 10-K SEC filing).
``` import logging import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO) logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader from llama_index.llms.openai import OpenAI from llama_index.core.response.notebook_utils import display_source_node from IPython.display import Markdown, display ```

### Download Legal Document Data
We’ll use Uber’s 10-K SEC filing, which contains legal and regulatory information - perfect for demonstrating Kanon 2’s legal domain expertise.
``` !mkdir -p 'data/10k/' !wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/10k/uber_2021.pdf' -O 'data/10k/uber_2021.pdf' ```

### Load the Legal Document
``` documents = SimpleDirectoryReader("./data/10k/").load_data() print(f"Loaded {len(documents)} document(s)") ```

### Build Index with Document Task
We use `task="retrieval/document"` when building the index to optimize embeddings for document storage.
``` # Initialize embedding model for documents embed_model = IsaacusEmbedding( api_key=isaacus_api_key, model="kanon-2-embedder", task="retrieval/document", )

# Build the index index = VectorStoreIndex.from_documents( documents=documents, embed_model=embed_model, ) ```

### Query with Legal Questions

Now we’ll query the index with legal-specific questions. Note that `get_query_embedding` automatically uses `task="retrieval/query"` for optimal query performance.

``` # Create a retriever retriever = index.as_retriever(similarity_top_k=3)
# Query about risk factors retrieved_nodes = retriever.retrieve( "What are the main risk factors mentioned in the document?" )

### Query about Legal Proceedings
``` # Query about legal proceedings retrieved_nodes = retriever.retrieve( "What legal proceedings or litigation is the company involved in?" )

print(f"Retrieved {len(retrieved_nodes)} nodes\n")
for i, node in enumerate(retrieved_nodes): print(f"\n--- Node {i+1} (Score: {node.score:.4f}) ---") display_source_node(node, source_length=500) ```

### Build a Query Engine with LLM
Combine Isaacus embeddings with an LLM for complete question answering:
``` import os
# Set your OpenAI API key openai_api_key = "<API_KEY>" os.environ["OPENAI_API_KEY"] = openai_api_key ```

``` # Set up LLM llm = OpenAI(model="gpt-4o-mini", temperature=0)

# Create query engine query_engine = index.as_query_engine( llm=llm, similarity_top_k=5, )

# Ask a legal question response = query_engine.query( "What are the company's main regulatory and legal risks?" )

### Another Legal Query
``` response = query_engine.query( "What intellectual property does the company rely on?" )

display(Markdown(f"**Answer:** {response}")) ```
## Async Usage
Isaacus embeddings also support async operations for better performance in async applications:
``` import asyncio

async def get_embeddings_async(): embed_model = IsaacusEmbedding( api_key=isaacus_api_key, )
# Get async single embedding embedding = await embed_model.aget_text_embedding( "Async legal document text" )
# Get async batch embeddings embeddings = await embed_model.aget_text_embedding_batch( ["Text 1", "Text 2", "Text 3"] )
return embedding, embeddings

# Run async function embedding, embeddings = await get_embeddings_async()
print(f"Async single embedding dimension: {len(embedding)}") print( f"Async batch: {len(embeddings)} embeddings of {len(embeddings[0])} dimensions each" ) ```

## Summary
In this notebook, we demonstrated:
1. **Basic usage** - Getting single and batch embeddings 2. **Task-specific optimization** - Using `retrieval/document` for indexing and `retrieval/query` for searching 3. **Dimensionality reduction** - Reducing embedding size for efficiency 4. **Legal RAG pipeline** - Building a complete retrieval system with legal documents (Uber 10-K) 5. **Async operations** - Using async methods for better performance

The Kanon 2 Embedder excels at legal document understanding and retrieval, making it ideal for legal tech applications, compliance tools, contract analysis, and more.

## Additional Resources
- Isaacus Documentation [6] - Kanon 2 Embedder Announcement [7] - Massive Legal Embedding Benchmark (MLEB) [1] - Isaacus Platform [8]

[1] https://isaacus.com/blog/introducing-mleb
[2] https://platform.isaacus.com/accounts/signup/
[3] https://platform.isaacus.com/billing/
[4] https://docs.isaacus.com/pricing/credits
[5] https://platform.isaacus.com/users/api-keys/
[6] https://docs.isaacus.com
[7] https://isaacus.com/blog/introducing-kanon-2-embedder
[8] https://platform.isaacus.com
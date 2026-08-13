# developers.llamaindex.ai/python/framework/integrations/vector_stores/pineconeindexdemo-hybrid/index.md
> https://developers.llamaindex.ai/python/framework/integrations/vector_stores/pineconeindexdemo-hybrid/index.md

--- title: Pinecone Vector Store - Hybrid Search | Developer Documentation ---
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.
``` %pip install llama-index-vector-stores-pinecone "transformers[torch]" ```
#### Creating a Pinecone Index
``` from pinecone import Pinecone, ServerlessSpec ```
``` import os
os.environ["PINECONE_API_KEY"] = "..." os.environ["OPENAI_API_KEY"] = "sk-..."
api_key = os.environ["PINECONE_API_KEY"]
pc = Pinecone(api_key=api_key) ```
``` # delete if needed pc.delete_index("quickstart") ```
``` # dimensions are for text-embedding-ada-002 # NOTE: needs dotproduct for hybrid search
pc.create_index( name="quickstart", dimension=1536, metric="dotproduct", spec=ServerlessSpec(cloud="aws", region="us-east-1"), )

# If you need to create a PodBased Pinecone index, you could alternatively do this: # # from pinecone import Pinecone, PodSpec # # pc = Pinecone(api_key='xxx') # # pc.create_index( # name='my-index', # dimension=1536, # metric='cosine', # spec=PodSpec( # environment='us-east1-gcp', # pod_type='p1.x1', # pods=1 # ) # ) # ```

``` pinecone_index = pc.Index("quickstart") ```
Download Data

``` !mkdir -p 'data/paul_graham/' !wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt' ```

#### Load documents, build the PineconeVectorStore
When `add_sparse_vector=True`, the `PineconeVectorStore` will compute sparse vectors for each document.
By default, it is using simple token frequency for the sparse vectors. But, you can also specify a custom sparse embedding model.
``` from llama_index.core import VectorStoreIndex, SimpleDirectoryReader from llama_index.vector_stores.pinecone import PineconeVectorStore from IPython.display import Markdown, display ```

``` # load documents documents = SimpleDirectoryReader("./data/paul_graham/").load_data() ```

``` # set add_sparse_vector=True to compute sparse vectors during upsert from llama_index.core import StorageContext

if "OPENAI_API_KEY" not in os.environ: raise EnvironmentError(f"Environment variable OPENAI_API_KEY is not set")
vector_store = PineconeVectorStore( pinecone_index=pinecone_index, add_sparse_vector=True, ) storage_context = StorageContext.from_defaults(vector_store=vector_store) index = VectorStoreIndex.from_documents( documents, storage_context=storage_context ) ```

``` huggingface/tokenizers: The current process just got forked, after parallelism has already been used. Disabling parallelism to avoid deadlocks... To disable this warning, you can either: - Avoid using `tokenizers` before the fork if possible - Explicitly set the environment variable TOKENIZERS_PARALLELISM=(true | false)

Upserted vectors: 0%| | 0/22 [00:00<?, ?it/s] ```
#### Query Index
May need to wait a minute or two for the index to be ready
``` # set Logging to DEBUG for more detailed outputs query_engine = index.as_query_engine(vector_store_query_mode="hybrid") response = query_engine.query("What happened at Viaweb?") ```

``` display(Markdown(f"<b>{response}</b>")) ```

**Paul Graham started Viaweb because he needed money. As the company grew, he realized he didn’t want to run a big company and decided to build a subset of the vision as an open source project. Eventually, Viaweb was bought by Yahoo in the summer of 1998, which was a huge relief for Paul Graham.**

## Changing the sparse embedding model
``` %pip install llama-index-sparse-embeddings-fastembed ```
``` # Clear the vector store vector_store.clear() ```
``` from llama_index.sparse_embeddings.fastembed import FastEmbedSparseEmbedding
sparse_embedding_model = FastEmbedSparseEmbedding( model_name="prithivida/Splade_PP_en_v1" )
vector_store = PineconeVectorStore( pinecone_index=pinecone_index, add_sparse_vector=True, sparse_embedding_model=sparse_embedding_model, ) ```
``` Fetching 5 files: 0%| | 0/5 [00:00<?, ?it/s] ```
``` index = VectorStoreIndex.from_documents( documents, storage_context=storage_context ) ```
``` Upserted vectors: 0%| | 0/22 [00:00<?, ?it/s] ```
Wait a mininute for things to upload..
``` response = query_engine.query("What happened at Viaweb?") display(Markdown(f"<b>{response}</b>")) ```

**Paul Graham started Viaweb because he needed money. He recruited a team to work on building software and services, with a focus on creating an application builder and network infrastructure. However, halfway through the summer, Paul realized he didn’t want to run a big company and decided to shift his focus to building a subset of the project as an open source project. This led to the development of a new dialect of Lisp called Arc. Ultimately, Viaweb was sold to Yahoo in the summer of 1998, providing relief to Paul Graham and allowing him to transition to a new phase in his life.**
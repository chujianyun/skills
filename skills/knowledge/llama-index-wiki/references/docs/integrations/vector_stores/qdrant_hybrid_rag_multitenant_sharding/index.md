# developers.llamaindex.ai/python/framework/integrations/vector_stores/qdrant_hybrid_rag_multitenant_sharding/index.md
> https://developers.llamaindex.ai/python/framework/integrations/vector_stores/qdrant_hybrid_rag_multitenant_sharding/index.md

--- title: Hybrid RAG with Qdrant: multi-tenancy, custom sharding, distributed setup | Developer Documentation ---

## What you’ll build
This notebook implements a production-style Hybrid RAG on Qdrant using LlamaIndex, designed for multitenancy and scale-out via custom sharding.
- Hybrid search: dense embeddings + sparse BM25 for higher recall and precision. - Multitenancy: isolate tenants using payload filters and shard routing. - Custom sharding: keep each tenant local for performance and cost efficiency. - Distributed Qdrant: multi-node setup with replication for high availability and throughput.

This notebook walks through an end to end Retrieval Augmented Generation workflow that uses Qdrant as a distributed hybrid search backend and LlamaIndex as the orchestration layer. You will build a tenant aware RAG that combines dense vectors with sparse signals, you will isolate data per tenant with filters, and you will route data and queries with a custom shard key for scale.

## Install dependencies
### About the dependencies
- llama-index: orchestration layer for ingestion, indexing, and retrieval. - llama-index-vector-stores-qdrant: Qdrant integration with hybrid support. - fastembed: lightweight CPU-friendly embedding/sparse models
``` %pip install -U llama-index llama-index-vector-stores-qdrant fastembed ```
Make sure you have a distributed Qdrant cluster up and running. Here is a `compose.yaml` file:
``` services: qdrant_primary: image: "qdrant/qdrant:latest" ports: - "6333:6333" environment: QDRANT__CLUSTER__ENABLED: "true" command: ["./qdrant", "--uri", "http://qdrant_primary:6335"] restart: always qdrant_secondary: image: "qdrant/qdrant:latest" environment: QDRANT__CLUSTER__ENABLED: "true" command: ["./qdrant", "--bootstrap", "http://qdrant_primary:6335"] restart: always ```

## Imports and global settings
### Settings and connectivity
- Embeddings: `FastEmbedEmbedding('BAAI/bge-base-en-v1.5')` is a compact, high-quality baseline. - Connection: `QDRANT_URL` defaults to an HTTP endpoint; set `QDRANT_API_KEY` for secured/cloud setups.
``` import os
from qdrant_client import AsyncQdrantClient, QdrantClient from qdrant_client import models
from llama_index.core import ( Settings, VectorStoreIndex, Document, StorageContext, ) from llama_index.vector_stores.qdrant import QdrantVectorStore from llama_index.embeddings.fastembed import FastEmbedEmbedding

# Embeddings, small and fast Settings.embed_model = FastEmbedEmbedding(model_name="BAAI/bge-base-en-v1.5")
# Qdrant connection, local by default, set QDRANT_URL and QDRANT_API_KEY for cloud QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333") QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

client: QdrantClient = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY) aclient: AsyncQdrantClient = AsyncQdrantClient( url=QDRANT_URL, api_key=QDRANT_API_KEY ) COLLECTION = "hybrid_rag_multitenant_sharding_demo" ```

## Create distributed-ready collection
### Configure dual-vector schema (dense + sparse)
- Define vector field names: `dense` for embeddings and `sparse` for BM25‑style signals.
- Dense config:
- Determine embedding dimensionality at runtime by probing `Settings.embed_model` (avoids hardcoding). - Use cosine distance for semantic similarity.
- Sparse config: - Enable an in‑memory sparse index (`on_disk=False`) to support hybrid scoring.
- These settings establish the collection’s dual‑index layout used later by QdrantVectorStore for hybrid retrieval.
``` dense_vector_name = "dense" dense_config = models.VectorParams( size=len(Settings.embed_model.get_text_embedding("probe")), distance=models.Distance.COSINE, ) sparse_vector_name = "sparse" sparse_config = models.SparseVectorParams( index=models.SparseIndexParams(on_disk=False) ) ```

### Shard keys and selector contract
- `shard_keys`: \[‘tenant\_a’, ‘tenant\_b’] — predefined partitions used with custom sharding to keep each tenant local. - `payload_indexes`: keyword index on `tenant_id` to accelerate filter-based queries. - `shard_key_selector_fn(tenant_id) -> tenant_id`: returns the shard key used for both writes and reads.
``` shard_keys = ["tenant_a", "tenant_b"] payload_indexes = [ { "field_name": "tenant_id", "field_schema": models.PayloadSchemaType.KEYWORD, } ]

def shard_key_selector_fn(tenant_id: str) -> models.ShardKeySelector: return tenant_id ```
### Initialize hybrid Qdrant store with custom sharding
This step creates or attaches to the collection named in `COLLECTION` and configures a dual‑vector hybrid store:
- Hybrid search: `enable_hybrid=True` with `dense_vector_name='dense'` and `sparse_vector_name='sparse'`.
- Dense config: `dense_config` uses cosine distance and derives size from `Settings.embed_model`.
- Sparse config: `sparse_config` enables an in‑memory sparse index; `fastembed_sparse_model='Qdrant/bm25'` supplies BM25‑style signals.
- Distributed topology:
- `sharding_method=Custom` with `shard_keys=['tenant_a','tenant_b']`. - `shard_key_selector_fn(tenant_id) -> tenant_id` routes both writes and reads. - `shard_number=6`, `replication_factor=2` for scale and High availability.
- Payload index: `payload_indexes` accelerates filtering on `tenant_id`.
Idempotent behavior: the vector store will create the collection if missing and reuse it on subsequent runs.
``` vector_store = QdrantVectorStore( collection_name=COLLECTION, client=client, aclient=aclient, dense_vector_name=dense_vector_name, sparse_vector_name=sparse_vector_name, enable_hybrid=True, dense_config=dense_config, sparse_config=sparse_config, fastembed_sparse_model="Qdrant/bm25", shard_number=6, sharding_method=models.ShardingMethod.CUSTOM, shard_key_selector_fn=shard_key_selector_fn, shard_keys=shard_keys, replication_factor=2, payload_indexes=payload_indexes, ) ```

## Prepare multi-tenant dataset
We create two tenants with small document sets. Each Document carries tenant\_id, tags, and a doc\_id.
### Dataset design and extensibility
We simulate two tenants with a few short documents each. Every `Document` carries:
- `tenant_id` for isolation and shard routing, - `tags` for quick filtering and debugging, - `text` content used for dense/sparse indexing.
``` TENANT_DOCS: dict[str, list[Document]] = { "tenant_a": [ Document( text="Solar panels reduce electricity bills and carbon footprint", metadata={"tenant_id": "tenant_a", "tags": ["energy", "solar"]}, ), Document( text="Inverters convert DC power to AC for home appliances", metadata={"tenant_id": "tenant_a", "tags": ["energy", "hardware"]}, ), Document( text="Net metering policies vary by region and utility provider", metadata={ "tenant_id": "tenant_a", "tags": ["policy", "regulation"], }, ), ], "tenant_b": [ Document( text="Kubernetes orchestrates containers across a cluster", metadata={"tenant_id": "tenant_b", "tags": ["cloud", "k8s"]}, ), Document( text="Service meshes add observability and traffic management", metadata={ "tenant_id": "tenant_b", "tags": ["cloud", "networking"], }, ), Document( text="Helm charts package and deploy Kubernetes applications", metadata={"tenant_id": "tenant_b", "tags": ["cloud", "devops"]}, ), ], } ```

## Ingest with shard key for locality

Here we embed text with the active Settings.embed\_model, then upsert each point with payload and a shard key. This keeps each tenant local to a shard group in a cluster.

### Embedding strategy
- FastEmbed keeps this demo CPU-friendly. For production, consider a service (e.g., text-embedding-3-large or in-house model) and cache embeddings. - If you change the model, update `dense_config.size` to match and consider reindexing. - Avoid embedding on every run in notebooks; persist or cache to speed up iterations.
``` def create_dense_embeddings(docs: list[Document]) -> list[Document]: for doc in docs: doc.embedding = Settings.embed_model.get_text_embedding(doc.text) return docs ```

### Ingestion flow and locality guarantees
- We embed each doc with the configured embedding model (dense) and rely on the vector store to build the sparse representation. - Writes use `shard_identifier=tenant_id`, ensuring documents live on the intended shard group.
Tip: For large batches, prefer the async ingestion APIs and chunk documents for backpressure control.
``` for tenant_id, docs in TENANT_DOCS.items(): docs = create_dense_embeddings(docs) await vector_store.async_add(docs, shard_identifier=tenant_id) ```

### Index wrapping and reusability
`StorageContext.from_defaults(vector_store=vector_store)` binds the Qdrant collection to LlamaIndex’s `VectorStoreIndex` without re-ingesting data.
Benefits:
- Reuse the same physical collection for multiple retrievers or query pipelines. - Swap retrieval modes (dense-only, sparse-only, hybrid) via retriever config, not data layout. - Keep ingestion concerns (sharding, replication) decoupled from application query logic.
``` storage_context = StorageContext.from_defaults(vector_store=vector_store) index = VectorStoreIndex.from_vector_store( vector_store, storage_context=storage_context ) ```

## Multi-tenant retrieval
Use a tenant-scoped hybrid retriever and keep queries shard-local. You can also use metadata filters if you want to filter within the tenant’s data.
### Retrieval tips for hybrid mode
- Set `vector_store_query_mode=HYBRID` to combine dense and sparse. Tune `similarity_top_k`, `sparse_top_k`, and `hybrid_top_k`. - Pass `vector_store_kwargs={"shard_identifier": tenant_id}` to keep queries within the tenant’s shard. - Add metadata filters (e.g., on `tenant_id` or `tags`) to further narrow candidates when needed.
``` from llama_index.core.retrievers import VectorIndexRetriever from llama_index.core.vector_stores.types import VectorStoreQueryMode

def create_retriever_for_tenant(tenant_id: str) -> VectorIndexRetriever: if tenant_id not in shard_keys: raise ValueError( f"Unknown tenant_id: {tenant_id}. Expected one of {shard_keys}" ) return VectorIndexRetriever( index=index, vector_store_query_mode=VectorStoreQueryMode.HYBRID, similarity_top_k=5, sparse_top_k=5, hybrid_top_k=5, vector_store_kwargs={"shard_identifier": tenant_id}, )

tenant_id = "tenant_b" retriever = create_retriever_for_tenant(tenant_id)
query = "manage microservices traffic and observability" results = retriever.retrieve(query)
print(f"Tenant: {tenant_id} | Query: {query}") for i, r in enumerate(results, 1): meta = r.node.metadata print( f"{i}. score={r.score:.4f} | tags={meta.get('tags')} | text={r.node.get_content()}" ) ```
``` Tenant: tenant_b | Query: manage microservices traffic and observability 1. score=4.6271 | tags=['cloud', 'networking'] | text=Service meshes add observability and traffic management 2. score=0.1213 | tags=['cloud', 'k8s'] | text=Kubernetes orchestrates containers across a cluster 3. score=0.0000 | tags=['cloud', 'devops'] | text=Helm charts package and deploy Kubernetes applications ```
### Interpreting results
- The printout shows the hybrid score, tags (metadata), and snippet of the matched text. - Verify tenant isolation by switching `tenant_id` and observing that results come only from that tenant’s documents.
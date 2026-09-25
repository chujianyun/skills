# developers.llamaindex.ai/python/framework/module_guides/querying/retriever/retrievers/index.md
> https://developers.llamaindex.ai/python/framework/module_guides/querying/retriever/retrievers/index.md

--- title: Retriever Modules | Developer Documentation ---
We are actively adding more tailored retrieval guides. In the meanwhile, please take a look at the API References.
## Index Retrievers
Please see the retriever modes for more details on how to get a retriever from any given index.
If you want to import the corresponding retrievers directly, please check out our API reference.
## Comprehensive Retriever Guides
Check out our comprehensive guides on various retriever modules, many of which cover advanced concepts (auto-retrieval, routing, ensembling, and more).
### Advanced Retrieval and Search

These guides contain advanced retrieval techniques. Some are common like keyword/hybrid search, reranking, and more. Some are specific to LLM + RAG workflows, like small-to-big and auto-merging retrieval.

- Define Custom Retriever - BM25 Hybrid Retriever - Simple Query Fusion - Reciprocal Rerank Fusion - Auto Merging Retriever - Metadata Replacement - Composable Retrievers

### Auto-Retrieval
These retrieval techniques perform **semi-structured** queries, combining semantic search with structured filtering.
- Auto-Retrieval (with Pinecone) - Auto-Retrieval (with Lantern) - Auto-Retrieval (with Chroma) - Auto-Retrieval (with BagelDB) - Auto-Retrieval (with Vectara) - Multi-Doc Auto-Retrieval

### Knowledge Graph Retrievers
- Knowledge Graph RAG Retriever
### Composed Retrievers
These are retrieval techniques that are composed on top of other retrieval techniques - providing higher-level capabilities like hierarchical retrieval and query decomposition.
- Query Fusion - Recursive Table Retrieval - Recursive Node Retrieval - Braintrust - Router Retriever - Ensemble Retriever - Multi-Doc Auto-Retrieval

### Managed Retrievers
- Google - Vectara - VideoDB - Amazon Bedrock

### Other Retrievers
These are guides that don’t fit neatly into a category but should be highlighted regardless.
- Multi-Doc Hybrid - You Retriever - Text-to-SQL - DeepMemory (Activeloop) - Pathway
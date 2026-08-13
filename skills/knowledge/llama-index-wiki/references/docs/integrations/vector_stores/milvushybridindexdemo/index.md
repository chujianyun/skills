# developers.llamaindex.ai/python/framework/integrations/vector_stores/milvushybridindexdemo/index.md
> https://developers.llamaindex.ai/python/framework/integrations/vector_stores/milvushybridindexdemo/index.md

--- title: Milvus Vector Store With Hybrid Search | Developer Documentation ---

Hybrid search leverages the strengths of both semantic retrieval and keyword matching to deliver more accurate and contextually relevant results. By combining the advantages of semantic search and keyword matching, hybrid search is particularly effective in complex information retrieval tasks.
This notebook demonstrates how to use Milvus for hybrid search in LlamaIndex RAG pipelines. We’ll begin with the recommended default hybrid search (semantic + BM25) and then explore other alternative sparse embedding methods and customization of hybrid reranker.
## Prerequisites
**Install dependencies**
Before getting started, make sure you have the following dependencies installed:
``` ! pip install llama-index-vector-stores-milvus ! pip install llama-index-embeddings-openai ! pip install llama-index-llms-openai ```

> If you’re using Google Colab, you may need to **restart the runtime** (Navigate to the “Runtime” menu at the top of the interface, and select “Restart session” from the dropdown menu.)
**Set up accounts**
This tutorial uses OpenAI for text embeddings and answer generation. You need to prepare the OpenAI API key [1].
``` import openai
openai.api_key = "sk-" ```
To use the Milvus vector store, specify your Milvus server `URI` (and optionally with the `TOKEN`). To start a Milvus server, you can set up a Milvus server by following the [Milvus installation guide] [3] or simply trying Zilliz Cloud [2] for free.
> Full-text search is currently supported in Milvus Standalone, Milvus Distributed, and Zilliz Cloud, but not yet in Milvus Lite (planned for future implementation). Reach out <support@zilliz.com> for more information.
``` URI = "http://localhost:19530" # TOKEN = "" ```

**Load example data**
Run the following commands to download sample documents into the “data/paul\_graham” directory:
``` ! mkdir -p 'data/paul_graham/' ! wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt' ```

Then use `SimpleDirectoryReaderLoad` to load the essay “What I Worked On” by Paul Graham:
``` from llama_index.core import SimpleDirectoryReader
documents = SimpleDirectoryReader("./data/paul_graham/").load_data()
# Let's take a look at the first document print("Example document:\n", documents[0]) ```
``` Example document: Doc ID: f9cece8c-9022-46d8-9d0e-f29d70e1dbbe Text: What I Worked On February 2021 Before college the two main things I worked on, outside of school, were writing and programming. I didn't write essays. I wrote what beginning writers were supposed to write then, and probably still are: short stories. My stories were awful. They had hardly any plot, just characters with strong feelings, which I ... ```

## Hybrid Search with BM25
This section shows how to perform a hybrid search using BM25. To get started, we will initialize the `MilvusVectorStore` and create an index for the example documents. The default configuration uses:
- Dense embeddings from the default embedding model (OpenAI’s `text-embedding-ada-002`) - BM25 for full-text search if enable\_sparse is True - RRFRanker with k=60 for combining results if hybrid search is enabled
``` # Create an index over the documnts from llama_index.vector_stores.milvus import MilvusVectorStore from llama_index.core import StorageContext, VectorStoreIndex

vector_store = MilvusVectorStore( uri=URI, # token=TOKEN, dim=1536, # vector dimension depends on the embedding model enable_sparse=True, # enable the default full-text search using BM25 overwrite=True, # drop the collection if it already exists ) storage_context = StorageContext.from_defaults(vector_store=vector_store) index = VectorStoreIndex.from_documents( documents, storage_context=storage_context ) ```

``` 2025-04-17 03:38:16,645 [DEBUG][_create_connection]: Created new connection using: cf0f4df74b18418bb89ec512063c1244 (async_milvus_client.py:547) Sparse embedding function is not provided, using default. Default sparse embedding function: BM25BuiltInFunction(input_field_names='text', output_field_names='sparse_embedding'). ```

Here is more information about the arguments for configuring dense and sparse fields in the `MilvusVectorStore`:
**dense field**
- `enable_dense (bool)`: A boolean flag to enable or disable dense embedding. Defaults to True. - `dim (int, optional)`: The dimension of the embedding vectors for the collection. - `embedding_field (str, optional)`: The name of the dense embedding field for the collection, defaults to DEFAULT\_EMBEDDING\_KEY. - `index_config (dict, optional)`: The configuration used for building the dense embedding index. Defaults to None. - `search_config (dict, optional)`: The configuration used for searching the Milvus dense index. Note that this must be compatible with the index type specified by `index_config`. Defaults to None. - `similarity_metric (str, optional)`: The similarity metric to use for dense embedding, currently supports IP, COSINE and L2.

**sparse field**
- `enable_sparse (bool)`: A boolean flag to enable or disable sparse embedding. Defaults to False. - `sparse_embedding_field (str)`: The name of sparse embedding field, defaults to DEFAULT\_SPARSE\_EMBEDDING\_KEY. - `sparse_embedding_function (Union[BaseSparseEmbeddingFunction, BaseMilvusBuiltInFunction], optional)`: If enable\_sparse is True, this object should be provided to convert text to a sparse embedding. If None, the default sparse embedding function (BM25BuiltInFunction) will be used, or use BGEM3SparseEmbedding given existing collection without built-in functions. - `sparse_index_config (dict, optional)`: The configuration used to build the sparse embedding index. Defaults to None.

To enable hybrid search during the querying stage, set `vector_store_query_mode` to “hybrid”. This will combine and rerank search results from both semantic search and full-text search. Let’s test with a sample query: “What did the author learn at Viaweb?”:
``` import textwrap
query_engine = index.as_query_engine( vector_store_query_mode="hybrid", similarity_top_k=5 ) response = query_engine.query("What did the author learn at Viaweb?") print(textwrap.fill(str(response), 100)) ```

``` The author learned about retail, the importance of user feedback, and the significance of growth rate as the ultimate test of a startup at Viaweb. ```

### Customize text analyzer
Analyzers play a vital role in full-text search by breaking sentences into tokens and performing lexical processing, such as stemming and stop-word removal. They are typically language-specific. For more details, refer to Milvus Analyzer Guide [4].
Milvus supports two types of analyzers: **Built-in Analyzers** and **Custom Analyzers**. By default, if `enable_sparse` is set to True, `MilvusVectorStore` utilizes the `BM25BuiltInFunction` with default configurations, employing the standard built-in analyzer that tokenizes text based on punctuation.
To use a different analyzer or customize the existing one, you can provide values to the `analyzer_params` argument when building the `BM25BuiltInFunction`. Then, set this function as the `sparse_embedding_function` in `MilvusVectorStore`.
``` from llama_index.vector_stores.milvus.utils import BM25BuiltInFunction
bm25_function = BM25BuiltInFunction( analyzer_params={ "tokenizer": "standard", "filter": [ "lowercase", # Built-in filter {"type": "length", "max": 40}, # Custom cap size of a single token {"type": "stop", "stop_words": ["of", "to"]}, # Custom stopwords ], }, enable_match=True, )

vector_store = MilvusVectorStore( uri=URI, # token=TOKEN, dim=1536, enable_sparse=True, sparse_embedding_function=bm25_function, # BM25 with custom analyzer overwrite=True, ) ```

``` 2025-04-17 03:38:48,085 [DEBUG][_create_connection]: Created new connection using: 61afd81600cb46ee89f887f16bcbfe55 (async_milvus_client.py:547) ```
## Hybrid Search with Other Sparse Embedding
Besides combining semantic search with BM25, Milvus also supports hybrid search using a sparse embedding function such as BGE-M3 [5]. The following example uses the built-in `BGEM3SparseEmbeddingFunction` to generate sparse embeddings.
First, we need to install the `FlagEmbedding` package:
``` ! pip install -q FlagEmbedding ```
Then let’s build the vector store and index using the default OpenAI model for densen embedding and the built-in BGE-M3 for sparse embedding:
``` from llama_index.vector_stores.milvus.utils import BGEM3SparseEmbeddingFunction
vector_store = MilvusVectorStore( uri=URI, # token=TOKEN, dim=1536, enable_sparse=True, sparse_embedding_function=BGEM3SparseEmbeddingFunction(), overwrite=True, )

storage_context = StorageContext.from_defaults(vector_store=vector_store) index = VectorStoreIndex.from_documents( documents, storage_context=storage_context ) ```

``` Fetching 30 files: 100%|██████████| 30/30 [00:00<00:00, 68871.99it/s] 2025-04-17 03:39:02,074 [DEBUG][_create_connection]: Created new connection using: ff4886e2f8da44e08304b748d9ac9b51 (async_milvus_client.py:547) Chunks: 100%|██████████| 1/1 [00:00<00:00, 1.07it/s] ```

Now let’s perform a hybrid search query with a sample question:
``` query_engine = index.as_query_engine( vector_store_query_mode="hybrid", similarity_top_k=5 ) response = query_engine.query("What did the author learn at Viaweb??") print(textwrap.fill(str(response), 100)) ```

``` Chunks: 100%|██████████| 1/1 [00:00<00:00, 17.29it/s]

The author learned about retail, the importance of user feedback, the value of growth rate in a startup, the significance of pricing strategy, the benefits of working on things that weren't prestigious, and the challenges and rewards of running a startup. ```

### Customize Sparse Embedding Function
You can also customize the sparse embedding function as long as it inherits from `BaseSparseEmbeddingFunction`, including the following methods:
- `encode_queries`: This method converts texts into list of sparse embeddings for queries. - `encode_documents`: This method converts text into list of sparse embeddings for documents.
The output of each method should follow the format of the sparse embedding, which is a list of dictionaries. Each dictionary should have a key (an integer) representing the dimension, and a corresponding value (a float) representing the embedding’s magnitude in that dimension (e.g., {1: 0.5, 2: 0.3}).
For example, here’s a custom sparse embedding function implementation using BGE-M3:
``` from FlagEmbedding import BGEM3FlagModel from typing import List from llama_index.vector_stores.milvus.utils import BaseSparseEmbeddingFunction

[Column 1]
class ExampleEmbeddingFunction(BaseSparseEmbeddingFunction): def __init__(self): self.model = BGEM3FlagModel("BAAI/bge-m3", use_fp16=False)

def encode_queries(self, queries: List[str]): outputs = self.model.encode( queries, return_dense=False, return_sparse=True, return_colbert_vecs=False, )["lexical_weights"] return [self._to_standard_dict(output) for output in outputs]

def encode_documents(self, documents: List[str]): outputs = self.model.encode( documents, return_dense=False, return_sparse=True, return_colbert_vecs=False, )["lexical_weights"] return [self._to_standard_dict(output) for output in outputs]

def _to_standard_dict(self, raw_output): result = {} for k in raw_output: result[int(k)] = raw_output[k] return result ```

## Customize hybrid reranker

- `hybrid_ranker_params (dict, optional)`: Configuration parameters for the hybrid ranker. The structure of this dictionary depends on the specific ranker being used:
- For “RRFRanker”, it should include: - “k” (int): A parameter used in Reciprocal Rank Fusion (RRF). This value is used to calculate the rank scores as part of the RRF algorithm, which combines multiple ranking strategies into a single score to improve search relevance. The default value is 60 if not specified.
- For “WeightedRanker”, it expects:
- “weights” (list of float): A list of exactly two weights:
1. The weight for the dense embedding component. 2. The weight for the sparse embedding component. These weights are used to balance the significance of the dense and sparse components of the embeddings in the hybrid retrieval process. The default weights are \ [1.0, 1.0] if not specified.
``` vector_store = MilvusVectorStore( uri=URI, # token=TOKEN, dim=1536, overwrite=False, # Use the existing collection created in the previous example enable_sparse=True, hybrid_ranker="WeightedRanker", hybrid_ranker_params={"weights": [1.0, 0.5]}, ) index = VectorStoreIndex.from_vector_store(vector_store) query_engine = index.as_query_engine( vector_store_query_mode="hybrid", similarity_top_k=5 ) response = query_engine.query("What did the author learn at Viaweb?") print(textwrap.fill(str(response), 100)) ```

``` 2025-04-17 03:44:00,419 [DEBUG][_create_connection]: Created new connection using: 09c051fb18c04f97a80f07958856587b (async_milvus_client.py:547) Sparse embedding function is not provided, using default. No built-in function detected, using BGEM3SparseEmbeddingFunction(). Fetching 30 files: 100%|██████████| 30/30 [00:00<00:00, 136622.28it/s] Chunks: 100%|██████████| 1/1 [00:00<00:00, 1.07it/s]

[Column 2]
Milvus supports two types of reranking strategies [6]: Reciprocal Rank Fusion (RRF) and Weighted Scoring. The default ranker in `MilvusVectorStore` hybrid search is RRF with k=60. To customize the hybrid ranker, modify the following parameters:
- `hybrid_ranker (str)`: Specifies the type of ranker used in hybrid search queries. Currently only supports \[“RRFRanker”, “WeightedRanker”]. Defaults to “RRFRanker”.


The author learned several valuable lessons at Viaweb, including the importance of understanding growth rate as the ultimate test of a startup, the significance of user feedback in shaping the software, and the realization that web applications were the future of software development. Additionally, the experience at Viaweb taught the author about the challenges and rewards of running a startup, the value of simplicity in software design, and the impact of pricing strategies on attracting customers. ```

[1] https://platform.openai.com/api-keys
[2] https://docs.zilliz.com/docs/register-with-zilliz-cloud
[3] https://milvus.io/docs/install-overview.md
[4] https://milvus.io/docs/analyzer-overview.md#Analyzer-Overview
[5] https://arxiv.org/abs/2402.03216
[6] https://milvus.io/docs/reranking.md
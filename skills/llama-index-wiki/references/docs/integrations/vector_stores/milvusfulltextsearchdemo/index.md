# developers.llamaindex.ai/python/framework/integrations/vector_stores/milvusfulltextsearchdemo/index.md
> https://developers.llamaindex.ai/python/framework/integrations/vector_stores/milvusfulltextsearchdemo/index.md

--- title: Milvus Vector Store with Full-Text Search | Developer Documentation ---

**Full-text search** uses exact keyword matching, often leveraging algorithms like BM25 to rank documents by relevance. In **Retrieval-Augmented Generation (RAG)** systems, this method retrieves pertinent text to enhance AI-generated responses.
Meanwhile, **semantic search** interprets contextual meaning to provide broader results. Combining both approaches creates a **hybrid search** that improves information retrieval—especially in cases where a single method falls short.
With Milvus 2.5 [1]’s Sparse-BM25 approach, raw text is automatically converted into sparse vectors. This eliminates the need for manual sparse embedding generation and enables a hybrid search strategy that balances semantic understanding with keyword relevance.
In this tutorial, you’ll learn how to use LlamaIndex and Milvus to build a RAG system using full-text search and hybrid search. We’ll start by implementing full-text search alone and then enhance it by integrating semantic search for more comprehensive results.
> Before proceeding with this tutorial, ensure you are familiar with full-text search [2] and the [basics of using Milvus in LlamaIndex] [3].
## Prerequisites
**Install dependencies**
Before getting started, make sure you have the following dependencies installed:
``` %pip install llama-index-vector-stores-milvus %pip install llama-index-embeddings-openai %pip install llama-index-llms-openai ```

> If you’re using Google Colab, you may need to **restart the runtime** (Navigate to the “Runtime” menu at the top of the interface, and select “Restart session” from the dropdown menu.)
**Set up accounts**
This tutorial uses OpenAI for text embeddings and answer generation. You need to prepare the OpenAI API key [4].
``` import openai
openai.api_key = "sk-" ```
To use the Milvus vector store, specify your Milvus server `URI` (and optionally with the `TOKEN`). To start a Milvus server, you can set up a Milvus server by following the [Milvus installation guide] [6] or simply trying Zilliz Cloud [5] for free.
> Full-text search is currently supported in Milvus Standalone, Milvus Distributed, and Zilliz Cloud, but not yet in Milvus Lite (planned for future implementation). Reach out <support@zilliz.com> for more information.
``` URI = "http://localhost:19530" # TOKEN = "" ```

**Download example data**
Run the following commands to download sample documents into the “data/paul\_graham” directory:
``` %mkdir -p 'data/paul_graham/' %wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt' ```

``` --2025-03-27 07:49:01-- https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt Resolving raw.githubusercontent.com (raw.githubusercontent.com)... 185.199.108.133, 185.199.109.133, 185.199.110.133, ... Connecting to raw.githubusercontent.com (raw.githubusercontent.com)|185.199.108.133|:443... connected. HTTP request sent, awaiting response... 200 OK Length: 75042 (73K) [text/plain] Saving to: ‘data/paul_graham/paul_graham_essay.txt’

data/paul_graham/pa 100%[===================>] 73.28K --.-KB/s in 0.07s
2025-03-27 07:49:01 (1.01 MB/s) - ‘data/paul_graham/paul_graham_essay.txt’ saved [75042/75042] ```
## RAG with Full-Text Search
Integrating full-text search into a RAG system balances semantic search with precise and predictable keyword-based retrieval. You can also choose to only use full text search though it’s recommended to combine full text search with semantic search for better search results. Here for demonstration purpose we will show full text search alone and hybrid search.
To get started, use `SimpleDirectoryReaderLoad` to load the essay “What I Worked On” by Paul Graham:
``` from llama_index.core import SimpleDirectoryReader
documents = SimpleDirectoryReader("./data/paul_graham/").load_data()
# Let's take a look at the first document print("Example document:\n", documents[0]) ```
``` Example document: Doc ID: 16b7942f-bf1a-4197-85e1-f31d51ea25a9 Text: What I Worked On February 2021 Before college the two main things I worked on, outside of school, were writing and programming. I didn't write essays. I wrote what beginning writers were supposed to write then, and probably still are: short stories. My stories were awful. They had hardly any plot, just characters with strong feelings, which I ... ```

### Full-Text Search with BM25
LlamaIndex’s `MilvusVectorStore` supports full-text search, enabling efficient keyword-based retrieval. By using a built-in function as the `sparse_embedding_function`, it applies BM25 scoring to rank search results.
In this section, we’ll demonstrate how to implement a RAG system using BM25 for full-text search.
``` from llama_index.core import VectorStoreIndex, StorageContext from llama_index.vector_stores.milvus import MilvusVectorStore from llama_index.vector_stores.milvus.utils import BM25BuiltInFunction from llama_index.core import Settings

# Skip dense embedding model Settings.embed_model = None
# Build Milvus vector store creating a new collection vector_store = MilvusVectorStore( uri=URI, # token=TOKEN, enable_dense=False, enable_sparse=True, # Only enable sparse to demo full text search sparse_embedding_function=BM25BuiltInFunction(), overwrite=True, )

# Store documents in Milvus storage_context = StorageContext.from_defaults(vector_store=vector_store) index = VectorStoreIndex.from_documents( documents, storage_context=storage_context ) ```

``` Embeddings have been explicitly disabled. Using MockEmbedding. ```
The above code inserts example documents into Milvus and builds an index to enable BM25 ranking for full-text search. It disables dense embedding and utilizes `BM25BuiltInFunction` with default parameters.
You can specify the input and output fields in the `BM25BuiltInFunction` parameters:
- `input_field_names (str)`: The input text field (default: “text”). It indicates which text field the BM25 algorithm applied to. Change this if using your own collection with a different text field name. - `output_field_names (str)`: The field where outputs of this BM25 function are stored (default: “sparse\_embedding”).
Once the vector store is set up, you can perform full-text search queries using Milvus with query mode “sparse” or “text\_search”:
``` import textwrap
query_engine = index.as_query_engine( vector_store_query_mode="sparse", similarity_top_k=5 ) answer = query_engine.query("What did the author learn at Viaweb?") print(textwrap.fill(str(answer), 100)) ```

``` The author learned several important lessons at Viaweb. They learned about the importance of growth rate as the ultimate test of a startup, the value of building stores for users to understand retail and software usability, and the significance of being the "entry level" option in a market. Additionally, they discovered the accidental success of making Viaweb inexpensive, the challenges of hiring too many people, and the relief felt when the company was acquired by Yahoo. ```

#### Customize text analyzer
Analyzers play a vital role in full-text search by breaking sentences into tokens and performing lexical processing, such as stemming and stop-word removal. They are typically language-specific. For more details, refer to Milvus Analyzer Guide [7].
Milvus supports two types of analyzers: **Built-in Analyzers** and **Custom Analyzers**. By default, the `BM25BuiltInFunction` uses the standard built-in analyzer, which tokenizes text based on punctuation.
To use a different analyzer or customize the existing one, you can pass value to the `analyzer_params` argument:
``` bm25_function = BM25BuiltInFunction( analyzer_params={ "tokenizer": "standard", "filter": [ "lowercase", # Built-in filter {"type": "length", "max": 40}, # Custom cap size of a single token {"type": "stop", "stop_words": ["of", "to"]}, # Custom stopwords ], }, enable_match=True, ) ```

### Hybrid Search with Reranker
A hybrid search system combines semantic search and full-text search, optimizing retrieval performance in a RAG system.
The following example uses OpenAI embedding for semantic search and BM25 for full-text search:
``` # Create index over the documnts vector_store = MilvusVectorStore( uri=URI, # token=TOKEN, # enable_dense=True, # enable_dense defaults to True dim=1536, enable_sparse=True, sparse_embedding_function=BM25BuiltInFunction(), overwrite=True, # hybrid_ranker="RRFRanker", # hybrid_ranker defaults to "RRFRanker" # hybrid_ranker_params={}, # hybrid_ranker_params defaults to {} )

storage_context = StorageContext.from_defaults(vector_store=vector_store) index = VectorStoreIndex.from_documents( documents, storage_context=storage_context, embed_model="default", # "default" will use OpenAI embedding ) ```

**How it works**
This approach stores documents in a Milvus collection with both vector fields:
- `embedding`: Dense embeddings generated by OpenAI embedding model for semantic search. - `sparse_embedding`: Sparse embeddings computed using BM25BuiltInFunction for full-text search.
In addition, we have applied a reranking strategy using “RRFRanker” with its default parameters. To customize reranker, you are able to configure `hybrid_ranker` and `hybrid_ranker_params` following the Milvus Reranking Guide [8].
Now, let’s test the RAG system with a sample query:
``` # Query query_engine = index.as_query_engine( vector_store_query_mode="hybrid", similarity_top_k=5 ) answer = query_engine.query("What did the author learn at Viaweb?") print(textwrap.fill(str(answer), 100)) ```

``` The author learned several important lessons at Viaweb. These included the importance of understanding growth rate as the ultimate test of a startup, the impact of hiring too many people, the challenges of being at the mercy of investors, and the relief experienced when Yahoo bought the company. Additionally, the author learned about the significance of user feedback, the value of building stores for users, and the realization that growth rate is crucial for the long-term success of a startup. ```

This hybrid approach ensures more accurate, context-aware responses in a RAG system by leveraging both semantic and keyword-based retrieval.

[1] https://milvus.io/blog/introduce-milvus-2-5-full-text-search-powerful-metadata-filtering-and-more.md
[2] https://milvus.io/docs/full-text-search.md#Full-Text-Search
[3] https://milvus.io/docs/integrate_with_llamaindex.md
[4] https://platform.openai.com/api-keys
[5] https://docs.zilliz.com/docs/register-with-zilliz-cloud
[6] https://milvus.io/docs/install-overview.md
[7] https://milvus.io/docs/analyzer-overview.md#Analyzer-Overview
[8] https://milvus.io/docs/reranking.md
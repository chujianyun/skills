# developers.llamaindex.ai/python/framework/integrations/vector_stores/milvusindexdemo/index.md
> https://developers.llamaindex.ai/python/framework/integrations/vector_stores/milvusindexdemo/index.md

--- title: Milvus Vector Store | Developer Documentation ---

This guide demonstrates how to build a Retrieval-Augmented Generation (RAG) system using LlamaIndex and Milvus.
The RAG system combines a retrieval system with a generative model to generate new text based on a given prompt. The system first retrieves relevant documents from a corpus using a vector similarity search engine like Milvus, and then uses a generative model to generate new text based on the retrieved documents.
Milvus [1] is the world’s most advanced open-source vector database, built to power embedding similarity search and AI applications.
In this notebook we are going to show a quick demo of using the MilvusVectorStore.
## Before you begin
### Install dependencies
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.
``` %pip install llama-index-vector-stores-milvus ```
``` %pip install llama-index ```
This notebook will use Milvus Lite [2] requiring a higher version of pymilvus:
``` %pip install pymilvus>=2.4.2 ```
> If you are using Google Colab, to enable dependencies just installed, you may need to **restart the runtime** (click on the “Runtime” menu at the top of the screen, and select “Restart session” from the dropdown menu).
### Setup OpenAI
Lets first begin by adding the openai api key. This will allow us to access chatgpt.
``` import openai
openai.api_key = "<API_KEY>" ```
### Prepare data
You can download sample data with the following commands:
``` ! mkdir -p "data/" ! wget "https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt" -O "data/paul_graham_essay.txt" ! wget "https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/10k/uber_2021.pdf" -O "data/uber_2021.pdf" ```

## Getting Started
### Generate our data
As a first example, lets generate a document from the file `paul_graham_essay.txt`. It is a single essay from Paul Graham titled `What I Worked On`. To generate the documents we will use the SimpleDirectoryReader.
``` from llama_index.core import SimpleDirectoryReader
# load documents documents = SimpleDirectoryReader( input_files=["./data/paul_graham_essay.txt"] ).load_data()

print("Document ID:", documents[0].doc_id) ```
``` Document ID: 95f25e4d-f270-4650-87ce-006d69d82033 ```
### Create an index across the data
Now that we have a document, we can can create an index and insert the document. For the index we will use a MilvusVectorStore. MilvusVectorStore takes in a few arguments:
**basic args**
- `uri (str, optional)`: The URI to connect to, comes in the form of “<https://address:port>” for Milvus or Zilliz Cloud service, or “path/to/local/milvus.db” for the lite local Milvus. Defaults to ”./milvus\_llamaindex.db”. - `token (str, optional)`: The token for log in. Empty if not using rbac, if using rbac it will most likely be “username:password”. - `collection_name (str, optional)`: The name of the collection where data will be stored. Defaults to “llamalection”. - `overwrite (bool, optional)`: Whether to overwrite existing collection with the same name. Defaults to False.

**scalar fields including doc id & text**
- `doc_id_field (str, optional)`: The name of the doc\_id field for the collection. Defaults to DEFAULT\_DOC\_ID\_KEY. - `text_key (str, optional)`: What key text is stored in in the passed collection. Used when bringing your own collection. Defaults to DEFAULT\_TEXT\_KEY. - `scalar_field_names (list, optional)`: The names of the extra scalar fields to be included in the collection schema. - `scalar_field_types (list, optional)`: The types of the extra scalar fields.

**dense field**
- `enable_dense (bool)`: A boolean flag to enable or disable dense embedding. Defaults to True. - `dim (int, optional)`: The dimension of the embedding vectors for the collection. Required when creating a new collection with enable\_sparse is False. - `embedding_field (str, optional)`: The name of the dense embedding field for the collection, defaults to DEFAULT\_EMBEDDING\_KEY. - `index_config (dict, optional)`: The configuration used for building the dense embedding index. Defaults to None. - `search_config (dict, optional)`: The configuration used for searching the Milvus dense index. Note that this must be compatible with the index type specified by `index_config`. Defaults to None. - `similarity_metric (str, optional)`: The similarity metric to use for dense embedding, currently supports IP, COSINE and L2.

**sparse field**
- `enable_sparse (bool)`: A boolean flag to enable or disable sparse embedding. Defaults to False. - `sparse_embedding_field (str)`: The name of sparse embedding field, defaults to DEFAULT\_SPARSE\_EMBEDDING\_KEY. - `sparse_embedding_function (Union[BaseSparseEmbeddingFunction, BaseMilvusBuiltInFunction], optional)`: If enable\_sparse is True, this object should be provided to convert text to a sparse embedding. If None, the default sparse embedding function (BM25BuiltInFunction) will be used. - `sparse_index_config (dict, optional)`: The configuration used to build the sparse embedding index. Defaults to None.

**hybrid ranker**
- `hybrid_ranker (str)`: Specifies the type of ranker used in hybrid search queries. Currently only supports \[“RRFRanker”, “WeightedRanker”]. Defaults to “RRFRanker”.
- `hybrid_ranker_params (dict, optional)`: Configuration parameters for the hybrid ranker. The structure of this dictionary depends on the specific ranker being used:
- For “RRFRanker”, it should include: - “k” (int): A parameter used in Reciprocal Rank Fusion (RRF). This value is used to calculate the rank scores as part of the RRF algorithm, which combines multiple ranking strategies into a single score to improve search relevance.
- For “WeightedRanker”, it expects:
- “weights” (list of float): A list of exactly two weights:
1. The weight for the dense embedding component. 2. The weight for the sparse embedding component. These weights are used to adjust the importance of the dense and sparse components of the embeddings in the hybrid retrieval process. Defaults to an empty dictionary, implying that the ranker will operate with its predefined default settings.
**others**
- `collection_properties (dict, optional)`: The collection properties such as TTL (Time-To-Live) and MMAP (memory mapping). Defaults to None. It could include:
- “collection.ttl.seconds” (int): Once this property is set, data in the current collection expires in the specified time. Expired data in the collection will be cleaned up and will not be involved in searches or queries. - “mmap.enabled” (bool): Whether to enable memory-mapped storage at the collection level.
- `index_management (IndexManagement)`: Specifies the index management strategy to use. Defaults to “create\_if\_not\_exists”.
- `batch_size (int)`: Configures the number of documents processed in one batch when inserting data into Milvus. Defaults to DEFAULT\_BATCH\_SIZE.
- `consistency_level (str, optional)`: Which consistency level to use for a newly created collection. Defaults to “Session”.
``` # Create an index over the documents from llama_index.core import VectorStoreIndex, StorageContext from llama_index.vector_stores.milvus import MilvusVectorStore

[Column 1]
vector_store = MilvusVectorStore( uri="./milvus_demo.db", dim=1536, overwrite=True ) storage_context = StorageContext.from_defaults(vector_store=vector_store) index = VectorStoreIndex.from_documents( documents, storage_context=storage_context ) ```

### Query the data
``` query_engine = index.as_query_engine() res = query_engine.query("What did the author learn?") print(res) ```
``` The author learned that philosophy courses in college were boring to him, leading him to switch his focus to studying AI. ```
``` res = query_engine.query( "What challenges did the disease pose for the author?" ) print(res) ```
``` The disease posed challenges for the author as it affected his mother's health, leading to a stroke caused by colon cancer. This resulted in her losing her balance and needing to be placed in a nursing home. The author and his sister were determined to help their mother get out of the nursing home and back to her house. ```
This next test shows that overwriting removes the previous data.
``` from llama_index.core import Document

[Column 2]
> For the parameters of `MilvusVectorStore`: > > - Setting the `uri` as a local file, e.g.`./milvus.db`, is the most convenient method, as it automatically utilizes Milvus Lite [2] to store all data in this file. > - If you have large scale of data, you can set up a more performant Milvus server on docker or kubernetes [3]. In this setup, please use the server uri, e.g.`http://localhost:19530`, as your `uri`. > - If you want to use Zilliz Cloud [4], the fully managed cloud service for Milvus, adjust the `uri` and `token`, which correspond to the [Public Endpoint and Api key] [5] in Zilliz Cloud.
Now that we have our document stored in the index, we can ask questions against the index. The index will use the data stored in itself as the knowledge base for chatgpt.


vector_store = MilvusVectorStore( uri="./milvus_demo.db", dim=1536, overwrite=True ) storage_context = StorageContext.from_defaults(vector_store=vector_store) index = VectorStoreIndex.from_documents( [Document(text="The number that is being searched for is ten.")], storage_context, ) query_engine = index.as_query_engine() res = query_engine.query("Who is the author?") print(res) ```

``` The author is the individual who created the context information. ```
The next test shows adding additional data to an already existing index.
``` del index, vector_store, storage_context, query_engine
vector_store = MilvusVectorStore(uri="./milvus_demo.db", overwrite=False) storage_context = StorageContext.from_defaults(vector_store=vector_store) index = VectorStoreIndex.from_documents( documents, storage_context=storage_context ) query_engine = index.as_query_engine() res = query_engine.query("What is the number?") print(res) ```

``` The number is ten. ```
``` res = query_engine.query("Who is the author?") print(res) ```

``` Paul Graham ```
## Metadata filtering
We can generate results by filtering specific sources. The following example illustrates loading all documents from the directory and subsequently filtering them based on metadata.
``` from llama_index.core.vector_stores import ExactMatchFilter, MetadataFilters
# Load all the two documents loaded before documents_all = SimpleDirectoryReader("./data/").load_data()
vector_store = MilvusVectorStore( uri="./milvus_demo.db", dim=1536, overwrite=True ) storage_context = StorageContext.from_defaults(vector_store=vector_store) index = VectorStoreIndex.from_documents(documents_all, storage_context) ```

We want to only retrieve documents from the file `uber_2021.pdf`.
``` filters = MetadataFilters( filters=[ExactMatchFilter(key="file_name", value="uber_2021.pdf")] ) query_engine = index.as_query_engine(filters=filters) res = query_engine.query( "What challenges did the disease pose for the author?" )

``` The disease posed challenges related to the adverse impact on the business and operations, including reduced demand for Mobility offerings globally, affecting travel behavior and demand. Additionally, the pandemic led to driver supply constraints, impacted by concerns regarding COVID-19, with uncertainties about when supply levels would return to normal. The rise of the Omicron variant further affected travel, resulting in advisories and restrictions that could adversely impact both driver supply and consumer demand for Mobility offerings.
```
We get a different result this time when retrieve from the file `paul_graham_essay.txt`.
``` filters = MetadataFilters( filters=[ExactMatchFilter(key="file_name", value="paul_graham_essay.txt")] ) query_engine = index.as_query_engine(filters=filters) res = query_engine.query( "What challenges did the disease pose for the author?" )

print(res) ```
``` The disease posed challenges for the author as it affected his mother's health, leading to a stroke caused by colon cancer. This resulted in his mother losing her balance and needing to be placed in a nursing home. The author and his sister were determined to help their mother get out of the nursing home and back to her house. ```

[1] https://milvus.io/
[2] https://milvus.io/docs/milvus_lite.md
[3] https://milvus.io/docs/quickstart.md
[4] https://zilliz.com/cloud
[5] https://docs.zilliz.com/docs/on-zilliz-cloud-console#free-cluster-details
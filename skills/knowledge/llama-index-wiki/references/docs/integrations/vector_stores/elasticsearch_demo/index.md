# developers.llamaindex.ai/python/framework/integrations/vector_stores/elasticsearch_demo/index.md
> https://developers.llamaindex.ai/python/framework/integrations/vector_stores/elasticsearch_demo/index.md

--- title: Elasticsearch | Developer Documentation ---
> Elasticsearch [1] is a search database, that supports full text and vector searches.
## Basic Example
In this basic example, we take the a Paul Graham essay, split it into chunks, embed it using an open-source embedding model, load it into Elasticsearch, and then query it. For an example using different retrieval strategies see Elasticsearch Vector Store [2].
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.
``` %pip install -qU llama-index-vector-stores-elasticsearch llama-index-embeddings-huggingface llama-index ```
``` # import from llama_index.core import VectorStoreIndex, SimpleDirectoryReader from llama_index.vector_stores.elasticsearch import ElasticsearchStore from llama_index.core import StorageContext ```

``` # set up OpenAI import os import getpass
os.environ["OPENAI_API_KEY"] = getpass.getpass("OpenAI API Key:") ```
Download Data
``` !mkdir -p 'data/paul_graham/' !wget -nv 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt' ```
``` 2024-05-13 15:10:43 URL:https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt [75042/75042] -> "data/paul_graham/paul_graham_essay.txt" [1] ```
``` from llama_index.embeddings.huggingface import HuggingFaceEmbedding from llama_index.core import Settings
# define embedding function Settings.embed_model = HuggingFaceEmbedding( model_name="BAAI/bge-small-en-v1.5" ) ```
``` # load documents documents = SimpleDirectoryReader("./data/paul_graham/").load_data()
# define index vector_store = ElasticsearchStore( es_url="http://localhost:9200", # see Elasticsearch Vector Store for more authentication options index_name="paul_graham_essay", ) storage_context = StorageContext.from_defaults(vector_store=vector_store) index = VectorStoreIndex.from_documents( documents, storage_context=storage_context ) ```

``` # Query Data query_engine = index.as_query_engine() response = query_engine.query("What did the author do growing up?") print(response) ```

``` The author worked on writing and programming outside of school. They wrote short stories and tried writing programs on an IBM 1401 computer. They also built a microcomputer kit and started programming on it, writing simple games and a word processor. ```

[1] http://www.github.com/elastic/elasticsearch
[2] https://docs.llamaindex.ai/en/stable/examples/vector_stores/elasticsearchindexdemo/
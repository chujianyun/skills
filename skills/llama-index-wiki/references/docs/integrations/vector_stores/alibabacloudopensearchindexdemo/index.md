# developers.llamaindex.ai/python/framework/integrations/vector_stores/alibabacloudopensearchindexdemo/index.md
> https://developers.llamaindex.ai/python/framework/integrations/vector_stores/alibabacloudopensearchindexdemo/index.md

--- title: Alibaba Cloud OpenSearch Vector Store | Developer Documentation ---

> Alibaba Cloud OpenSearch Vector Search Edition [1] is a large-scale distributed search engine that is developed by Alibaba Group. Alibaba Cloud OpenSearch Vector Search Edition provides search services for the entire Alibaba Group, including Taobao, Tmall, Cainiao, Youku, and other e-commerce platforms that are provided for customers in regions outside the Chinese mainland. Alibaba Cloud OpenSearch Vector Search Edition is also a base engine of Alibaba Cloud OpenSearch. After years of development, Alibaba Cloud OpenSearch Vector Search Edition has met the business requirements for high availability, high timeliness, and cost-effectiveness. Alibaba Cloud OpenSearch Vector Search Edition also provides an automated O\&M system on which you can build a custom search service based on your business features.

To run, you should have a instance.
### Setup
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.
``` %pip install llama-index-vector-stores-alibabacloud-opensearch ```
``` %pip install llama-index ```
``` import logging import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO) logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout)) ```
### Please provide OpenAI access key
In order use embeddings by OpenAI you need to supply an OpenAI API Key:
``` import openai
OPENAI_API_KEY = getpass.getpass("OpenAI API Key:") openai.api_key = OPENAI_API_KEY ```
#### Download Data
``` !mkdir -p 'data/paul_graham/' !wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt' ```

#### Load documents
``` from llama_index.core import SimpleDirectoryReader from IPython.display import Markdown, display ```

``` # load documents documents = SimpleDirectoryReader("./data/paul_graham").load_data() print(f"Total documents: {len(documents)}") ```

``` Total documents: 1 ```
### Create the Alibaba Cloud OpenSearch Vector Store object:
To run the next step, you should have a Alibaba Cloud OpenSearch Vector Service instance, and configure a table.
``` # if run fllowing cells raise async io exception, run this import nest_asyncio

nest_asyncio.apply() ```
``` # initialize without metadata filter from llama_index.core import StorageContext, VectorStoreIndex from llama_index.vector_stores.alibabacloud_opensearch import ( AlibabaCloudOpenSearchStore, AlibabaCloudOpenSearchConfig, )

config = AlibabaCloudOpenSearchConfig( endpoint="*****", instance_id="*****", username="your_username", password="your_password", table_name="llama", )

vector_store = AlibabaCloudOpenSearchStore(config) storage_context = StorageContext.from_defaults(vector_store=vector_store) index = VectorStoreIndex.from_documents( documents, storage_context=storage_context ) ```

#### Query Index
``` # set Logging to DEBUG for more detailed outputs query_engine = index.as_query_engine() response = query_engine.query("What did the author do growing up?") ```

``` display(Markdown(f"<b>{response}</b>")) ```
**Before college, the author worked on writing and programming. They wrote short stories and tried writing programs on the IBM 1401 in 9th grade using an early version of Fortran.**
### Connecting to an existing store
Since this store is backed by Alibaba Cloud OpenSearch, it is persistent by definition. So, if you want to connect to a store that was created and populated previously, here is how:
``` from llama_index.core import VectorStoreIndex from llama_index.vector_stores.alibabacloud_opensearch import ( AlibabaCloudOpenSearchStore, AlibabaCloudOpenSearchConfig, )

config = AlibabaCloudOpenSearchConfig( endpoint="***", instance_id="***", username="your_username", password="your_password", table_name="llama", )

vector_store = AlibabaCloudOpenSearchStore(config)
# Create index from existing stored vectors index = VectorStoreIndex.from_vector_store(vector_store) query_engine = index.as_query_engine() response = query_engine.query( "What did the author study prior to working on AI?" )

display(Markdown(f"<b>{response}</b>")) ```
### Metadata filtering
The Alibaba Cloud OpenSearch vector store support metadata filtering at query time. The following cells, which work on a brand new table, demonstrate this feature.
In this demo, for the sake of brevity, a single source document is loaded (the `../data/paul_graham/paul_graham_essay.txt` text file). Nevertheless, you will attach some custom metadata to the document to illustrate how you can can restrict queries with conditions on the metadata attached to the documents.
``` from llama_index.core import StorageContext, VectorStoreIndex from llama_index.vector_stores.alibabacloud_opensearch import ( AlibabaCloudOpenSearchStore, AlibabaCloudOpenSearchConfig, )

config = AlibabaCloudOpenSearchConfig( endpoint="****", instance_id="****", username="your_username", password="your_password", table_name="llama", )

md_storage_context = StorageContext.from_defaults( vector_store=AlibabaCloudOpenSearchStore(config) )

def my_file_metadata(file_name: str): """Depending on the input file name, associate a different metadata.""" if "essay" in file_name: source_type = "essay" elif "dinosaur" in file_name: # this (unfortunately) will not happen in this demo source_type = "dinos" else: source_type = "other" return {"source_type": source_type}

# Load documents and build index md_documents = SimpleDirectoryReader( "../data/paul_graham", file_metadata=my_file_metadata ).load_data() md_index = VectorStoreIndex.from_documents( md_documents, storage_context=md_storage_context ) ```

Add filter to query engine:
``` from llama_index.core.vector_stores import MetadataFilter, MetadataFilters
md_query_engine = md_index.as_query_engine( filters=MetadataFilters( filters=[MetadataFilter(key="source_type", value="essay")] ) ) md_response = md_query_engine.query( "How long it took the author to write his thesis?" )

display(Markdown(f"<b>{md_response}</b>")) ```
To test that the filtering is at play, try to change it to use only `"dinos"` documents… there will be no answer this time :)

[1] https://help.aliyun.com/zh/open-search/vector-search-edition/product-overview
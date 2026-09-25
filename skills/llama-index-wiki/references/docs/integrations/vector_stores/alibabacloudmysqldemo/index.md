# developers.llamaindex.ai/python/framework/integrations/vector_stores/alibabacloudmysqldemo/index.md
> https://developers.llamaindex.ai/python/framework/integrations/vector_stores/alibabacloudmysqldemo/index.md

--- title: Alibaba Cloud MySQL | Developer Documentation ---

> Alibaba Cloud MySQL, also named as ApsaraDB RDS for MySQL [1]. ApsaraDB RDS for MySQL is an online database service that is based on a branch of MySQL source code and offers high performance. ApsaraDB RDS for MySQL is a proven solution that has handled large volumes of concurrent traffic during Double 11. ApsaraDB RDS for MySQL provides basic features such as whitelist configuration, backup and recovery, Transparent Data Encryption (TDE), data migration, and management of instances, accounts, and databases. For more information, see [RDS MySQL Feature Overview] [2].

To run this notebook you need a ApsaraDB RDS MySQL instance running in the cloud, create an account and create needed databases. You can refer to this link [3].

In this notebook, we need to create databases called `llama_index_test` and `llama_index_meta_test` in your ApsaraDB RDS MySQL instance.
## Setup
If you’re opening this Notebook on colab, you will probably need to ensure you have `llama-index` installed:
``` !pip install llama-index ```
``` %pip install llama-index-vector-stores-alibabacloud-mysql ```
``` # choose dashscope as embedding and llm model, your can also use default openai or other model to test %pip install llama-index-embeddings-dashscope %pip install llama-index-llms-dashscope ```

Config dashscope embedding and llm model, your can also use default openai or other model to test. If you choose to use dashscope model, you can get your api key here [4], and set it in the following code:

``` !export DASHSCOPE_API_KEY="<API_KEY>" ```
## Download example data

``` !mkdir -p 'data/paul_graham/' !wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt' ```

## RAG Demo using Alibaba Cloud MySQL
### Simple Query
#### Load Data for Simple Query

print( """ ################# # simple generate vector #################""" ) client = AlibabaCloudMySQLVectorStore.from_params( host="rm-***.mysql.***.rds.aliyuncs.com", port=3306, user="user", password="password", database="llama_index_test", distance_method="COSINE", ) storage_context = StorageContext.from_defaults(vector_store=client) VectorStoreIndex.from_documents( documents, storage_context=storage_context, show_progress=True ) ```

print( """ ################# # Basic Querying including Search Test ################# """ ) client = AlibabaCloudMySQLVectorStore.from_params( host="rm-***.mysql.eu-west-1.rds.***.com", port=3306, user="user", password="password", database="llama_index_test", distance_method="COSINE", ) index = VectorStoreIndex.from_vector_store( vector_store=client, embed_model=embed_model )

QUESTION = "What did the author do growing up?" # Set Retriever vector_retriever = index.as_retriever() # search source_nodes = vector_retriever.retrieve(QUESTION) # check source_nodes print(f"Question: {QUESTION}") for node in source_nodes: print(f"---------------------------------------------") print("Search Test") print(f"---------------------------------------------") print(f"Score: {node.score:.3f}") print(node.get_content()) print(f"---------------------------------------------")

# run query query_engine = index.as_query_engine(llm=dashscope_llm) res = query_engine.query(QUESTION) print(f"Answer: {res.response}") print(f"---------------------------------------------\n\n") ```
### Metadata Filtering
#### Load Data for Metadata Filtering

from llama_index.core import ( VectorStoreIndex, SimpleDirectoryReader, StorageContext, ) from llama_index.vector_stores.alibabacloud_mysql.base import ( AlibabaCloudMySQLVectorStore, )

Settings.embed_model = DashScopeEmbedding(api_key=DASHSCOPE_API_KEY)

documents = SimpleDirectoryReader("data/paul_graham/").load_data() print(f"Total documents: {len(documents)}") print(f"First document, id: {documents[0].doc_id}") print(f"First document, hash: {documents[0].hash}") print( "First document, text" f" ({len(documents[0].text)} characters):\n{'='*20}\n{documents[0].text[:360]} ..." )

print( """ ################# # generate vector with some metadata for Metadata Filtering #################""" ) client = AlibabaCloudMySQLVectorStore.from_params( host="rm-***.mysql.***.rds.aliyuncs.com", port=3306, user="user", password="password", database="llama_index_meta_test", distance_method="COSINE", ) storage_context = StorageContext.from_defaults(vector_store=client) index = VectorStoreIndex.from_documents( documents, storage_context=storage_context, show_progress=True )

from llama_index.core import Document import regex as re
# Split the text into paragraphs. text_chunks = documents[0].text.split("\n\n")
# Create a document for each footnote footnotes = [ Document( text=chunk, id=documents[0].doc_id, metadata={ "is_footnote": bool(re.search(r"^\s*\[\d+\]\s*", chunk)), "mark_id": i, }, ) for i, chunk in enumerate(text_chunks) if bool(re.search(r"^\s*\[\d+\]\s*", chunk)) ]

# Insert the footnotes into the index for f in footnotes: index.insert(f) ```
#### Query using AlibabaCloudMySQL with Search Test
``` import os
DASHSCOPE_API_KEY = os.environ.get("DASHSCOPE_API_KEY")
from llama_index.core import VectorStoreIndex from llama_index.vector_stores.alibabacloud_mysql.base import ( AlibabaCloudMySQLVectorStore, )
# set Embbeding model from llama_index.core import Settings from llama_index.embeddings.dashscope import DashScopeEmbedding
embed_model = DashScopeEmbedding(api_key=DASHSCOPE_API_KEY) # Global Settings Settings.embed_model = embed_model
# config llm model from llama_index.llms.dashscope import DashScope, DashScopeGenerationModels
dashscope_llm = DashScope( model_name=DashScopeGenerationModels.QWEN_MAX, api_key=DASHSCOPE_API_KEY )
print( """ ################# # Querying with Metadata Filtering including Search Test ################# """ ) client = AlibabaCloudMySQLVectorStore.from_params( host="rm-***.mysql.***.rds.aliyuncs.com", port=3306, user="user", password="password", database="llama_index_meta_test", distance_method="COSINE", ) index = VectorStoreIndex.from_vector_store( vector_store=client, embed_model=embed_model )

from llama_index.core.vector_stores import ( MetadataFilters, MetadataFilter, FilterOperator, FilterCondition, )
QUESTION = "What did the author about space aliens and lisp?" print(f"---------------------------------------------") print(f"Question: {QUESTION}") filters = MetadataFilters( filters=[ MetadataFilter( key="is_footnote", value="true", operator=FilterOperator.EQ ), MetadataFilter(key="mark_id", value=0, operator=FilterOperator.GTE), ], condition=FilterCondition.AND, ) print(f"---------------------------------------------") for i in range(len(filters.filters)): print(f"Filter[{i}]: {filters.filters[i]}") print(f"Filter Condition: {filters.condition}") print(f"---------------------------------------------") retriever = index.as_retriever( filters=filters, ) result = retriever.retrieve(QUESTION) for node in result: print("Search Test") print(f"---------------------------------------------") print(f"Score: {node.score:.3f}") print(node.get_content()) print(f"---------------------------------------------")

# Create a query engine that only searches certain footnotes. footnote_query_engine = index.as_query_engine( filters=filters, llm=dashscope_llm, )
res = footnote_query_engine.query(QUESTION) print(f"Answer: {res.response}") print(f"---------------------------------------------\n\n") ```

[1] https://www.alibabacloud.com/help/en/rds/apsaradb-rds-for-mysql/overview-3
[2] https://www.alibabacloud.com/help/en/rds/apsaradb-rds-for-mysql/features
[3] https://www.alibabacloud.com/help/en/rds/apsaradb-rds-for- mysql/step-1-create-an-apsaradb-rds-for-mysql-instance-and-configure-databases
[4] https://modelstudio.console.aliyun.com/? tab=dashboard#/api-key
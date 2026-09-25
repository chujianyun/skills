# developers.llamaindex.ai/python/framework/integrations/vector_stores/analyticdbdemo/index.md
> https://developers.llamaindex.ai/python/framework/integrations/vector_stores/analyticdbdemo/index.md

[Column 1]
--- title: AnalyticDB | Developer Documentation ---

You should ensure you have `llama-index` installed:
``` %pip install llama-index-vector-stores-analyticdb ```
``` !pip install llama-index ```
### Please provide parameters:
``` import os import getpass

# alibaba cloud ram ak and sk: alibaba_cloud_ak = "" alibaba_cloud_sk = ""

# instance information: region_id = "cn-hangzhou" # region id of the specific instance instance_id = "gp-xxxx" # adb instance id account = "test_account" # instance account name created by API or 'Account Management' at the instance detail web page account_password = "" # instance account password ```

### Import needed package dependencies:
``` from llama_index.core import ( VectorStoreIndex, SimpleDirectoryReader, StorageContext, ) from llama_index.vector_stores.analyticdb import AnalyticDBVectorStore ```

### Load some example data:
``` !mkdir -p 'data/paul_graham/' !wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt' ```

### Read the data:
``` # load documents documents = SimpleDirectoryReader("./data/paul_graham/").load_data() print(f"Total documents: {len(documents)}") print(f"First document, id: {documents[0].doc_id}") print(f"First document, hash: {documents[0].hash}") print( "First document, text" f" ({len(documents[0].text)} characters):\n{'='*20}\n{documents[0].text[:360]} ..." ) ```

### Create the AnalyticDB Vector Store object:
``` analytic_db_store = AnalyticDBVectorStore.from_params( access_key_id=alibaba_cloud_ak, access_key_secret=alibaba_cloud_sk, region_id=region_id, instance_id=instance_id, account=account, account_password=account_password, namespace="llama", collection="llama", metrics="cosine", embedding_dimension=1536, ) ```

### Build the Index from the Documents:
``` storage_context = StorageContext.from_defaults(vector_store=analytic_db_store)
index = VectorStoreIndex.from_documents( documents, storage_context=storage_context ) ```

### Query using the index:
``` query_engine = index.as_query_engine() response = query_engine.query("Why did the author choose to work on AI?")

print(response.response) ```
### Delete the collection:
``` analytic_db_store.delete_collection() ```

[Column 2]
> AnalyticDB for PostgreSQL [1] is a massively parallel processing (MPP) data warehousing service that is designed to analyze large volumes of data online.
To run this notebook you need a AnalyticDB for PostgreSQL instance running in the cloud (you can get one at common-buy.aliyun.com [2]).
After creating the instance, you should create a manager account by API [3] or ‘Account Management’ at the instance detail web page.


[1] https://www.alibabacloud.com/help/en/analyticdb-for-postgresql/product-overview/overview-product-overview
[2] https://common-buy.aliyun.com/?commodityCode=GreenplumPost\&regionId=cn- hangzhou\&request=%7B%22instance_rs_type%22%3A%22ecs%22%2C%22engine_version%22%3A%226.0%22%2C%22seg_node_num%22%3A%224%22%2C%22SampleData%22%3A%22false%22%2C%22vector_optimizor%22%3A%22Y%22%7D
[3] https://www.alibabacloud.com/help/en/analyticdb-for-postgresql/developer-reference/api-gpdb-2016-05-03-createaccount
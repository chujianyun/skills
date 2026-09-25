# developers.llamaindex.ai/python/framework/integrations/vector_stores/tidbvector/index.md
> https://developers.llamaindex.ai/python/framework/integrations/vector_stores/tidbvector/index.md

--- title: TiDB Vector Store | Developer Documentation ---

> TiDB Cloud [1], is a comprehensive Database-as-a-Service (DBaaS) solution, that provides dedicated and serverless options. TiDB Serverless is now integrating a built-in vector search into the MySQL landscape. With this enhancement, you can seamlessly develop AI applications using TiDB Serverless without the need for a new database or additional technical stacks. Create a free TiDB Serverless cluster and start using the vector search feature at <https://pingcap.com/ai>.
This notebook provides a detailed guide on utilizing the tidb vector search in LlamaIndex.
## Setting up environments
``` %pip install llama-index-vector-stores-tidbvector %pip install llama-index ```

``` import textwrap
from llama_index.core import SimpleDirectoryReader, StorageContext from llama_index.core import VectorStoreIndex from llama_index.vector_stores.tidbvector import TiDBVectorStore ```

Configuring your OpenAI Key
``` import getpass import os

os.environ["OPENAI_API_KEY"] = getpass.getpass("Input your OpenAI API key:") ```
Configure TiDB connection setting that you will need. To connect to your TiDB Cloud Cluster, follow these steps:
- Go to your TiDB Cloud cluster Console and navigate to the `Connect` page. - Select the option to connect using `SQLAlchemy` with `PyMySQL`, and copy the provided connection URL (without password). - Paste the connection URL into your code, replacing the `tidb_connection_string_template` variable. - Type your password.

``` # replace with your tidb connect string from tidb cloud console tidb_connection_string_template = "mysql+pymysql://<USER>:<PASSWORD>@<HOST>:4000/<DB>?ssl_ca=/etc/ssl/cert.pem&ssl_verify_cert=true&ssl_verify_identity=true" # type your tidb password tidb_password = getpass.getpass("Input your TiDB password:") tidb_connection_url = tidb_connection_string_template.replace( "<PASSWORD>", tidb_password ) ```

Prepare data that used to show case
``` !mkdir -p 'data/paul_graham/' !wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt' ```

``` documents = SimpleDirectoryReader("./data/paul_graham").load_data() print("Document ID:", documents[0].doc_id) for index, document in enumerate(documents): document.metadata = {"book": "paul_graham"} ```

``` Document ID: 86e12675-2e9a-4097-847c-8b981dd41806 ```
## Create TiDB Vectore Store
The code snippet below creates a table named `VECTOR_TABLE_NAME` in TiDB, optimized for vector searching. Upon successful execution of this code, you will be able to view and access the `VECTOR_TABLE_NAME` table directly within your TiDB database environment
``` VECTOR_TABLE_NAME = "paul_graham_test" tidbvec = TiDBVectorStore( connection_string=tidb_connection_url, table_name=VECTOR_TABLE_NAME, distance_strategy="cosine", vector_dimension=1536, drop_existing_table=False, ) ```

Create a query engine based on tidb vectore store
``` storage_context = StorageContext.from_defaults(vector_store=tidbvec) index = VectorStoreIndex.from_documents( documents, storage_context=storage_context, show_progress=True ) ```

Note: If you encounter errors during this process due to the MySQL protocol’s packet size limitation, such as when trying to insert a large number of vectors (e.g., 2000 rows) , you can mitigate this issue by splitting the insertion into smaller batches. For example, you can set the `insert_batch_size` parameter to a smaller value (e.g., 1000) to avoid exceeding the packet size limit, ensuring smooth insertion of your data into the TiDB vector store:
``` storage_context = StorageContext.from_defaults(vector_store=tidbvec) index = VectorStoreIndex.from_documents( documents, storage_context=storage_context, insert_batch_size=1000, show_progress=True ) ```

## Semantic similarity search
This section focus on vector search basics and refining results using metadata filters. Please note that tidb vector only supports Deafult VectorStoreQueryMode.
``` query_engine = index.as_query_engine() response = query_engine.query("What did the author do?") print(textwrap.fill(str(response), 100)) ```

``` The author wrote a book. ```
### Filter with metadata
perform searches using metadata filters to retrieve a specific number of nearest-neighbor results that align with the applied filters.

query_engine = index.as_query_engine( filters=MetadataFilters( filters=[ MetadataFilter(key="book", value="paul_graham", operator="!="), ] ), similarity_top_k=2, ) response = query_engine.query("What did the author learn?") print(textwrap.fill(str(response), 100)) ```

Query again
``` from llama_index.core.vector_stores.types import ( MetadataFilter, MetadataFilters, )

query_engine = index.as_query_engine( filters=MetadataFilters( filters=[ MetadataFilter(key="book", value="paul_graham", operator="=="), ] ), similarity_top_k=2, ) response = query_engine.query("What did the author learn?") print(textwrap.fill(str(response), 100)) ```

``` The author learned valuable lessons from his experiences. ```
## Delete documents
``` tidbvec.delete(documents[0].doc_id) ```
Check whether the documents had been deleted
``` query_engine = index.as_query_engine() response = query_engine.query("What did the author learn?") print(textwrap.fill(str(response), 100)) ```

``` Empty Response ```

[1] https://www.pingcap.com/tidb-serverless/
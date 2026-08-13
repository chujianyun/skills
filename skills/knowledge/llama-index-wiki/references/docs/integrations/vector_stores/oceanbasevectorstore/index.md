# developers.llamaindex.ai/python/framework/integrations/vector_stores/oceanbasevectorstore/index.md
> https://developers.llamaindex.ai/python/framework/integrations/vector_stores/oceanbasevectorstore/index.md

--- title: OceanBase Vector Store | Developer Documentation ---

> OceanBase Database [1] is a distributed relational database. It is developed entirely by Ant Group. The OceanBase Database is built on a common server cluster. Based on the Paxos protocol and its distributed structure, the OceanBase Database provides high availability and linear scalability. The OceanBase Database is not dependent on specific hardware architectures.

This notebook describes in detail how to use the OceanBase vector store functionality in LlamaIndex.
#### Setup
``` %pip install llama-index-vector-stores-oceanbase %pip install llama-index # choose dashscope as embedding and llm model, your can also use default openai or other model to test %pip install llama-index-embeddings-dashscope %pip install llama-index-llms-dashscope ```

#### Deploy a standalone OceanBase server with docker
``` %docker run --name=ob433 -e MODE=slim -p 2881:2881 -d oceanbase/oceanbase-ce:4.3.3.0-100000142024101215 ```
#### Creating ObVecClient
``` from pyobvector import ObVecClient
client = ObVecClient() client.perform_raw_text_sql( "ALTER SYSTEM ob_vector_memory_limit_percentage = 30" ) ```

Config dashscope embedding model and LLM.
``` # set Embbeding model import os from llama_index.core import Settings from llama_index.embeddings.dashscope import DashScopeEmbedding

# Global Settings Settings.embed_model = DashScopeEmbedding()
# config llm model from llama_index.llms.dashscope import DashScope, DashScopeGenerationModels
dashscope_llm = DashScope( model_name=DashScopeGenerationModels.QWEN_MAX, api_key=os.environ.get("DASHSCOPE_API_KEY", ""), ) ```

#### Load documents
``` from llama_index.core import ( SimpleDirectoryReader, load_index_from_storage, VectorStoreIndex, StorageContext, ) from llama_index.vector_stores.oceanbase import OceanBaseVectorStore ```

Download Data & Load Data

``` !mkdir -p 'data/paul_graham/' !wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt' ```

``` # load documents documents = SimpleDirectoryReader("./data/paul_graham/").load_data() ```
``` oceanbase = OceanBaseVectorStore( client=client, dim=1536, drop_old=True, normalize=True, )
storage_context = StorageContext.from_defaults(vector_store=oceanbase) index = VectorStoreIndex.from_documents( documents, storage_context=storage_context ) ```
#### Query Index
``` # set Logging to DEBUG for more detailed outputs query_engine = index.as_query_engine(llm=dashscope_llm) res = query_engine.query("What did the author do growing up?") res.response ```

``` 'Growing up, the author worked on two main activities outside of school: writing and programming. They wrote short stories, which they admits were not particularly good, lacking plot but containing characters with strong emotions. They also started programming at a young age, initially on an IBM 1401 computer using an early version of Fortran, though they found it challenging due to the limitations of punch card input and their lack of data to process. Their programming journey真正 took off when microcomputers became available, allowing them to write more interactive programs such as games, a rocket flight predictor, and a simple word processor.'

```
#### Metadata Filtering
OceanBase Vector Store supports metadata filtering in the form of `=`、 `>`、`<`、`!=`、`>=`、`<=`、`in`、`not in`、`like`、`IS NULL` at query time.
``` from llama_index.core.vector_stores import ( MetadataFilters, MetadataFilter, )

query_engine = index.as_query_engine( llm=dashscope_llm, filters=MetadataFilters( filters=[ MetadataFilter(key="book", value="paul_graham", operator="!="), ] ), similarity_top_k=10, )

res = query_engine.query("What did the author learn?") res.response ```

#### Delete Documents
``` oceanbase.delete(documents[0].doc_id)
query_engine = index.as_query_engine(llm=dashscope_llm) res = query_engine.query("What did the author do growing up?") res.response ```

``` 'Empty Response' ```

[1] https://github.com/oceanbase/oceanbase
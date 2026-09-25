# developers.llamaindex.ai/python/framework/integrations/vector_stores/simpleindexons3/index.md
> https://developers.llamaindex.ai/python/framework/integrations/vector_stores/simpleindexons3/index.md

--- title: S3/R2 Storage | Developer Documentation ---
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.
``` !pip install llama-index ```
``` import logging import sys
logging.basicConfig(stream=sys.stdout, level=logging.INFO) logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))
from llama_index.core import ( VectorStoreIndex, SimpleDirectoryReader, load_index_from_storage, StorageContext, ) from IPython.display import Markdown, display ```

``` INFO:numexpr.utils:Note: NumExpr detected 32 cores but "NUMEXPR_MAX_THREADS" not set, so enforcing safe limit of 8. Note: NumExpr detected 32 cores but "NUMEXPR_MAX_THREADS" not set, so enforcing safe limit of 8. INFO:numexpr.utils:NumExpr defaulting to 8 threads. NumExpr defaulting to 8 threads.

/home/hua/code/llama_index/.hermit/python/lib/python3.10/site-packages/tqdm/auto.py:21: TqdmWarning: IProgress not found. Please update jupyter and ipywidgets. See https://ipywidgets.readthedocs.io/en/stable/user_install.html from .autonotebook import tqdm as notebook_tqdm ```
``` import dotenv import s3fs import os
dotenv.load_dotenv("../../../.env")
AWS_KEY = os.environ["AWS_ACCESS_KEY_ID"] AWS_SECRET = os.environ["AWS_SECRET_ACCESS_KEY"] R2_ACCOUNT_ID = os.environ["R2_ACCOUNT_ID"]
assert AWS_KEY is not None and AWS_KEY != ""
s3 = s3fs.S3FileSystem( key=AWS_KEY, secret=AWS_SECRET, endpoint_url=f"https://{R2_ACCOUNT_ID}.r2.cloudflarestorage.com", s 3_additional_kwargs={"ACL": "public-read"}, ) ```
Download Data
``` !mkdir -p 'data/paul_graham/' !wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt' ```
``` # load documents documents = SimpleDirectoryReader("./data/paul_graham/").load_data() print(len(documents)) ```
``` 1 ```
``` index = VectorStoreIndex.from_documents(documents, fs=s3) ```
``` INFO:llama_index.token_counter.token_counter:> [build_index_from_nodes] Total LLM token usage: 0 tokens > [build_index_from_nodes] Total LLM token usage: 0 tokens INFO:llama_index.token_counter.token_counter:> [build_index_from_nodes] Total embedding token usage: 20729 tokens > [build_index_from_nodes] Total embedding token usage: 20729 tokens ```
``` # save index to disk index.set_index_id("vector_index") index.storage_context.persist("llama-index/storage_demo", fs=s3) ```
``` s3.listdir("llama-index/storage_demo") ```
``` [{'Key': 'llama-index/storage_demo/docstore.json', 'LastModified': datetime.datetime(2023, 5, 14, 20, 23, 53, 213000, tzinfo=tzutc()), 'ETag': '"3993f79a6f7cf908a8e53450a2876cf0"', 'Size': 107529, 'StorageClass': 'STANDARD', 'type': 'file', 'size': 107529, 'name': 'llama-index/storage_demo/docstore.json'}, {'Key': 'llama-index/storage_demo/index_store.json', 'LastModified': datetime.datetime(2023, 5, 14, 20, 23, 53, 783000, tzinfo=tzutc()), 'ETag': '"5b084883bf0b08e3c2b979af7c16be43"', 'Size': 3105, 'StorageClass': 'STANDARD', 'type': 'file', 'size': 3105, 'name': 'llama-index/storage_demo/index_store.json'}, {'Key': 'llama-index/storage_demo/vector_store.json', 'LastModified': datetime.datetime(2023, 5, 14, 20, 23, 54, 232000, tzinfo=tzutc()), 'ETag': '"75535cf22c23bcd8ead21b8a52e9517a"', 'Size': 829290, 'StorageClass': 'STANDARD', 'type': 'file', 'size': 829290, 'name': 'llama-index/storage_demo/vector_store.json'}] ```

``` # load index from s3 sc = StorageContext.from_defaults( persist_dir="llama-index/storage_demo", fs=s3 ) ```
``` index2 = load_index_from_storage(sc, "vector_index") ```
``` INFO:llama_index.indices.loading:Loading indices with ids: ['vector_index'] Loading indices with ids: ['vector_index'] ```
``` index2.docstore.docs.keys() ```
``` dict_keys(['f8891670-813b-4cfa-9025-fcdc8ba73449', '985a2c69-9da5-40cf-ba30-f984921187c1', 'c55f077c-0bfb-4036-910c-6fd5f26f7372', 'b47face6-f25b-4381-bb8d-164f179d6888', '16304ef7-2378-4776-b86d-e8ed64c8fb58', '62dfdc7a- 6a2f-4d5f-9033-851fbc56c14a', 'a51ef189-3924-494b-84cf-e23df673e29c', 'f94aca2b-34ac-4ec4-ac41-d31cd3b7646f', 'ad89e2fb-e0fc-4615-a380-8245bd6546af', '3dbba979-ca08-4321-b4de-be5236ac2e11', '634b2d6d-0bff-4384-898f- b521470db8ac', 'ee9551ba-7a44-493d-997b-8eeab9c04e25', 'b21fe2b5-d8e3-4895-8424-fa9e3da76711', 'bd2609e8-8b52-49e8-8ee7-41b64b3ce9e1', 'a08b739e-efd9-4a61-8517-c4f9cea8cf7d', '8d4babaf-37f1-454a-8be4-b67e1b8e428f', '05389153-4567-4e53-a2ea-bc3e020ee1b2', 'd29531a5-c5d2-4e1d-ab99-56f2b4bb7f37', '2ccb3c63-3407-4acf-b5bb-045caa588bbc', 'a0b1bebb-3dcd-4bf8-9ebb-a4cd2cb82d53', '21517b34-6c1b-4607-bf89-7ab59b85fba6', 'f2487d52-1e5e-4482- a182-218680ef306e', '979998ce-39ee-41bc-a9be-b3ed68d7c304', '3e658f36-a13e-407a-8624-0adf9e842676'])
```
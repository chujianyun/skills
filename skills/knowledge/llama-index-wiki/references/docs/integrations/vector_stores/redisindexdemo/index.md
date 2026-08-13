# developers.llamaindex.ai/python/framework/integrations/vector_stores/redisindexdemo/index.md
> https://developers.llamaindex.ai/python/framework/integrations/vector_stores/redisindexdemo/index.md

--- title: Redis Vector Store | Developer Documentation ---

In this notebook we are going to show a quick demo of using the RedisVectorStore.
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.
``` %pip install -U llama-index llama-index-vector-stores-redis llama-index-embeddings-cohere llama-index-embeddings-openai ```
``` import os import getpass import sys import logging import textwrap import warnings

warnings.filterwarnings("ignore")
# Uncomment to see debug logs logging.basicConfig(stream=sys.stdout, level=logging.INFO)
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader from llama_index.vector_stores.redis import RedisVectorStore ```
### Start Redis
The easiest way to start Redis is using the Redis Stack [1] docker image or quickly signing up for a FREE Redis Cloud [2] instance.
To follow every step of this tutorial, launch the image as follows:
Terminal window
``` docker run --name redis-vecdb -d -p 6379:6379 -p 8001:8001 redis/redis-stack:latest ```
This will also launch the RedisInsight UI on port 8001 which you can view at <http://localhost:8001>.
### Setup OpenAI
Lets first begin by adding the openai api key. This will allow us to access openai for embeddings and to use chatgpt.
``` oai_api_key = getpass.getpass("OpenAI API Key:") os.environ["OPENAI_API_KEY"] = oai_api_key ```

Download Data
``` !mkdir -p 'data/paul_graham/' !wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt' ```

``` --2024-04-10 19:35:33-- https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt Resolving raw.githubusercontent.com (raw.githubusercontent.com)... 2606:50c0:8003::154, 2606:50c0:8000::154, 2606:50c0:8002::154, ... Connecting to raw.githubusercontent.com (raw.githubusercontent.com)|2606:50c0:8003::154|:443... connected. HTTP request sent, awaiting response... 200 OK Length: 75042 (73K) [text/plain] Saving to: ‘data/paul_graham/paul_graham_essay.txt’

data/paul_graham/pa 100%[===================>] 73.28K --.-KB/s in 0.03s
2024-04-10 19:35:33 (2.15 MB/s) - ‘data/paul_graham/paul_graham_essay.txt’ saved [75042/75042] ```
### Read in a dataset
Here we will use a set of Paul Graham essays to provide the text to turn into embeddings, store in a `RedisVectorStore` and query to find context for our LLM QnA loop.
``` # load documents documents = SimpleDirectoryReader("./data/paul_graham").load_data() print( "Document ID:", documents[0].id_, "Document Filename:", documents[0].metadata["file_name"], ) ```

``` Document ID: 7056f7ba-3513-4ef4-9792-2bd28040aaed Document Filename: paul_graham_essay.txt ```
### Initialize the default Redis Vector Store
Now we have our documents prepared, we can initialize the Redis Vector Store with **default** settings. This will allow us to store our vectors in Redis and create an index for real-time search.
``` from llama_index.core import StorageContext from redis import Redis

# create a Redis client connection redis_client = Redis.from_url("redis://localhost:6379")
# create the vector store wrapper vector_store = RedisVectorStore(redis_client=redis_client, overwrite=True)
# load storage context storage_context = StorageContext.from_defaults(vector_store=vector_store)
# build and load index from documents and storage context index = VectorStoreIndex.from_documents( documents, storage_context=storage_context ) # index = VectorStoreIndex.from_vector_store(vector_store=vector_store) ```

``` 19:39:17 llama_index.vector_stores.redis.base INFO Using default RedisVectorStore schema. 19:39:19 httpx INFO HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK" 19:39:19 llama_index.vector_stores.redis.base INFO Added 22 documents to index llama_index ```

### Query the default vector store
Now that we have our data stored in the index, we can ask questions against the index.
The index will use the data as the knowledge base for an LLM. The default setting for as\_query\_engine() utilizes OpenAI embeddings and GPT as the language model. Therefore, an OpenAI key is required unless you opt for a customized or local language model.
Below we will test searches against out index and then full RAG with an LLM.
``` query_engine = index.as_query_engine() retriever = index.as_retriever() ```

``` result_nodes = retriever.retrieve("What did the author learn?") for node in result_nodes: print(node) ```

``` 19:39:22 httpx INFO HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK" 19:39:22 llama_index.vector_stores.redis.base INFO Querying index llama_index with filters * 19:39:22 llama_index.vector_stores.redis.base INFO Found 2 results for query with id ['llama_index/vector_adb6b7ce-49bb-4961-8506-37082c02a389', 'llama_index/vector_e39be1fe-32d0-456e-b211-4efabd191108'] Node ID: adb6b7ce-49bb-4961-8506-37082c02a389 Text: What I Worked On February 2021 Before college the two main things I worked on, outside of school, were writing and programming. I didn't write essays. I wrote what beginning writers were supposed to write then, and probably still are: short stories. My stories were awful. They had hardly any plot, just characters with strong feelings, which I ... Score: 0.820

Node ID: e39be1fe-32d0-456e-b211-4efabd191108 Text: Except for a few officially anointed thinkers who went to the right parties in New York, the only people allowed to publish essays were specialists writing about their specialties. There were so many essays that had never been written, because there had been no way to publish them. Now they could be, and I was going to write them. [12] I've wor... Score: 0.819 ```

``` response = query_engine.query("What did the author learn?") print(textwrap.fill(str(response), 100)) ```

``` 19:39:25 httpx INFO HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK" 19:39:25 llama_index.vector_stores.redis.base INFO Querying index llama_index with filters * 19:39:25 llama_index.vector_stores.redis.base INFO Found 2 results for query with id ['llama_index/vector_adb6b7ce-49bb-4961-8506-37082c02a389', 'llama_index/vector_e39be1fe-32d0-456e-b211-4efabd191108'] 19:39:27 httpx INFO HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK" The author learned that working on things that weren't prestigious often led to valuable discoveries and indicated the right kind of motives. Despite the lack of initial prestige, pursuing such work could be a sign of genuine potential and appropriate motivations, steering clear of the common pitfall of being driven solely by the desire to impress others. ```

``` result_nodes = retriever.retrieve("What was a hard moment for the author?") for node in result_nodes: print(node) ```

``` 19:39:27 httpx INFO HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK" 19:39:27 llama_index.vector_stores.redis.base INFO Querying index llama_index with filters * 19:39:27 llama_index.vector_stores.redis.base INFO Found 2 results for query with id ['llama_index/vector_adb6b7ce-49bb-4961-8506-37082c02a389', 'llama_index/vector_e39be1fe-32d0-456e-b211-4efabd191108'] Node ID: adb6b7ce-49bb-4961-8506-37082c02a389 Text: What I Worked On February 2021 Before college the two main things I worked on, outside of school, were writing and programming. I didn't write essays. I wrote what beginning writers were supposed to write then, and probably still are: short stories. My stories were awful. They had hardly any plot, just characters with strong feelings, which I ... Score: 0.802

Node ID: e39be1fe-32d0-456e-b211-4efabd191108 Text: Except for a few officially anointed thinkers who went to the right parties in New York, the only people allowed to publish essays were specialists writing about their specialties. There were so many essays that had never been written, because there had been no way to publish them. Now they could be, and I was going to write them. [12] I've wor... Score: 0.799 ```

``` response = query_engine.query("What was a hard moment for the author?") print(textwrap.fill(str(response), 100)) ```

``` 19:39:29 httpx INFO HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK" 19:39:29 llama_index.vector_stores.redis.base INFO Querying index llama_index with filters * 19:39:29 llama_index.vector_stores.redis.base INFO Found 2 results for query with id ['llama_index/vector_adb6b7ce-49bb-4961-8506-37082c02a389', 'llama_index/vector_e39be1fe-32d0-456e-b211-4efabd191108'] 19:39:31 httpx INFO HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK" A hard moment for the author was when one of his programs on the IBM 1401 mainframe didn't terminate, leading to a technical error and an uncomfortable situation with the data center manager. ```

``` index.vector_store.delete_index() ```
``` 19:39:34 llama_index.vector_stores.redis.base INFO Deleting index llama_index ```
### Use a custom index schema
In most use cases, you need the ability to customize the underling index configuration and specification. For example, this is handy in order to define specific metadata filters you wish to enable.
With Redis, this is as simple as defining an index schema object (from file or dict) and passing it through to the vector store client wrapper.
For this example, we will:
1. switch the embedding model to Cohere 2. add an additional metadata field for the document `updated_at` timestamp 3. index the existing `file_name` metadata field
``` from llama_index.core.settings import Settings from llama_index.embeddings.cohere import CohereEmbedding

# set up Cohere Key co_api_key = getpass.getpass("Cohere API Key:") os.environ["CO_API_KEY"] = co_api_key

# set llamaindex to use Cohere embeddings Settings.embed_model = CohereEmbedding() ```
``` from redisvl.schema import IndexSchema

custom_schema = IndexSchema.from_dict( { # customize basic index specs "index": { "name": "paul_graham", "prefix": "essay", "key_separator": ":", }, # customize fields that are indexed "fields": [ # required fields for llamaindex {"type": "tag", "name": "id"}, {"type": "tag", "name": "doc_id"}, {"type": "text", "name": "text"}, # custom metadata fields {"type": "numeric", "name": "updated_at"}, {"type": "tag", "name": "file_name"}, # custom vector field definition for cohere embeddings { "type": "vector", "name": "vector", "attrs": { "dims": 1024, "algorithm": "hnsw", "distance_metric": "cosine", }, }, ], } ) ```

``` custom_schema.index ```
``` IndexInfo(name='paul_graham', prefix='essay', key_separator=':', storage_type=<StorageType.HASH: 'hash'>) ```
``` custom_schema.fields ```
``` {'id': TagField(name='id', type='tag', path=None, attrs=TagFieldAttributes(sortable=False, separator=',', case_sensitive=False, withsuffixtrie=False)), 'doc_id': TagField(name='doc_id', type='tag', path=None, attrs=TagFieldAttributes(sortable=False, separator=',', case_sensitive=False, withsuffixtrie=False)), 'text': TextField(name='text', type='text', path=None, attrs=TextFieldAttributes(sortable=False, weight=1, no_stem=False, withsuffixtrie=False, phonetic_matcher=None)), 'updated_at': NumericField(name='updated_at', type='numeric', path=None, attrs=NumericFieldAttributes(sortable=False)), 'file_name': TagField(name='file_name', type='tag', path=None, attrs=TagFieldAttributes(sortable=False, separator=',', case_sensitive=False, withsuffixtrie=False)), 'vector': HNSWVectorField(name='vector', type='vector', path=None, attrs=HNSWVectorFieldAttributes(dims=1024, algorithm=<VectorIndexAlgorithm.HNSW: 'HNSW'>, datatype=<VectorDataType.FLOAT32: 'FLOAT32'>, distance_metric= <VectorDistanceMetric.COSINE: 'COSINE'>, initial_cap=None, m=16, ef_construction=200, ef_runtime=10, epsilon=0.01))} ```

Learn more about schema and index design [3] with redis.
``` from datetime import datetime

def date_to_timestamp(date_string: str) -> int: date_format: str = "%Y-%m-%d" return int(datetime.strptime(date_string, date_format).timestamp())

# iterate through documents and add new field for document in documents: document.metadata["updated_at"] = date_to_timestamp( document.metadata["last_modified_date"] ) ```

``` vector_store = RedisVectorStore( schema=custom_schema, # provide customized schema redis_client=redis_client, overwrite=True, )

storage_context = StorageContext.from_defaults(vector_store=vector_store)
# build and load index from documents and storage context index = VectorStoreIndex.from_documents( documents, storage_context=storage_context ) ```

``` 19:40:05 httpx INFO HTTP Request: POST https://api.cohere.ai/v1/embed "HTTP/1.1 200 OK" 19:40:06 httpx INFO HTTP Request: POST https://api.cohere.ai/v1/embed "HTTP/1.1 200 OK" 19:40:06 httpx INFO HTTP Request: POST https://api.cohere.ai/v1/embed "HTTP/1.1 200 OK" 19:40:06 llama_index.vector_stores.redis.base INFO Added 22 documents to index paul_graham ```

### Query the vector store and filter on metadata
Now that we have additional metadata indexed in Redis, let’s try some queries with filters.
``` from llama_index.core.vector_stores import ( MetadataFilters, MetadataFilter, ExactMatchFilter, )

retriever = index.as_retriever( similarity_top_k=3, filters=MetadataFilters( filters=[ ExactMatchFilter(key="file_name", value="paul_graham_essay.txt"), MetadataFilter( key="updated_at", value=date_to_timestamp("2023-01-01"), operator=">=", ), MetadataFilter( key="text", value="learn", operator="text_match", ), ], condition="and", ), ) ```

``` result_nodes = retriever.retrieve("What did the author learn?")
for node in result_nodes: print(node) ```
``` 19:40:22 httpx INFO HTTP Request: POST https://api.cohere.ai/v1/embed "HTTP/1.1 200 OK"

19:40:22 llama_index.vector_stores.redis.base INFO Querying index paul_graham with filters ((@file_name:{paul_graham_essay\.txt} @updated_at:[1672549200 +inf]) @text:(learn)) 19:40:22 llama_index.vector_stores.redis.base INFO Found 3 results for query with id ['essay:0df3b734-ecdb-438e-8c90-f21a8c80f552', 'essay:01108c0d-140b-4dcc-b581-c38b7df9251e', 'essay:ced36463-ac36-46b0-b2d7- 935c1b38b781'] Node ID: 0df3b734-ecdb-438e-8c90-f21a8c80f552 Text: All that seemed left for philosophy were edge cases that people in other fields felt could safely be ignored. I couldn't have put this into words when I was 18. All I knew at the time was that I kept taking philosophy courses and they kept being boring. So I decided to switch to AI. AI was in the air in the mid 1980s, but there were two things... Score: 0.410

Node ID: 01108c0d-140b-4dcc-b581-c38b7df9251e Text: It was not, in fact, simply a matter of teaching SHRDLU more words. That whole way of doing AI, with explicit data structures representing concepts, was not going to work. Its brokenness did, as so often happens, generate a lot of opportunities to write papers about various band-aids that could be applied to it, but it was never going to get us ... Score: 0.390

Node ID: ced36463-ac36-46b0-b2d7-935c1b38b781 Text: Grad students could take classes in any department, and my advisor, Tom Cheatham, was very easy going. If he even knew about the strange classes I was taking, he never said anything. So now I was in a PhD program in computer science, yet planning to be an artist, yet also genuinely in love with Lisp hacking and working away at On Lisp. In other... Score: 0.389 ```

### Restoring from an existing index in Redis
Restoring from an index requires a Redis connection client (or URL), `overwrite=False`, and passing in the same schema object used before. (This can be offloaded to a YAML file for convenience using `.to_yaml()`)
``` custom_schema.to_yaml("paul_graham.yaml") ```
``` vector_store = RedisVectorStore( schema=IndexSchema.from_yaml("paul_graham.yaml"), redis_client=redis_client, ) index = VectorStoreIndex.from_vector_store(vector_store=vector_store) ```

``` 19:40:28 redisvl.index.index INFO Index already exists, not overwriting. ```
**In the near future** — we will implement a convenience method to load just using an index name:
``` RedisVectorStore.from_existing_index(index_name="paul_graham", redis_client=redis_client) ```
### Deleting documents or index completely
Sometimes it may be useful to delete documents or the entire index. This can be done using the `delete` and `delete_index` methods.
``` document_id = documents[0].doc_id document_id ```

``` '7056f7ba-3513-4ef4-9792-2bd28040aaed' ```
``` print("Number of documents before deleting", redis_client.dbsize()) vector_store.delete(document_id) print("Number of documents after deleting", redis_client.dbsize()) ```

``` Number of documents before deleting 22 19:40:32 llama_index.vector_stores.redis.base INFO Deleted 22 documents from index paul_graham Number of documents after deleting 0 ```

However, the Redis index still exists (with no associated documents) for continuous upsert.
``` vector_store.index_exists() ```
``` True ```
``` # now lets delete the index entirely # this will delete all the documents and the index vector_store.delete_index() ```

``` 19:40:37 llama_index.vector_stores.redis.base INFO Deleting index paul_graham ```
``` print("Number of documents after deleting", redis_client.dbsize()) ```
``` Number of documents after deleting 0 ```
### Troubleshooting
If you get an empty query result, there a couple of issues to check:
#### Schema
Unlike other vector stores, Redis expects users to explicitly define the schema for the index. This is for a few reasons:
1. Redis is used for many use cases, including real-time vector search, but also for standard document storage/retrieval, caching, messaging, pub/sub, session mangement, and more. Not all attributes on records need to be indexed for search. This is partially an efficiency thing, and partially an attempt to minimize user foot guns. 2. All index schemas, when using Redis & LlamaIndex, must include the following fields `id`, `doc_id`, `text`, and `vector`, at a minimum.
Instantiate your `RedisVectorStore` with the default schema (assumes OpenAI embeddings), or with a custom schema (see above).
#### Prefix issues
Redis expects all records to have a key prefix that segments the keyspace into “partitions” for potentially different applications, use cases, and clients.
Make sure that the chosen `prefix`, as part of the index schema, is consistent across your code (tied to a specific index).
To see what prefix your index was created with, you can run `FT.INFO <name of your index>` in the Redis CLI and look under `index_definition` => `prefixes`.
#### Data vs Index
Redis treats the records in the dataset and the index as different entities. This allows you more flexibility in performing updates, upserts, and index schema migrations.
If you have an existing index and want to make sure it’s dropped, you can run `FT.DROPINDEX <name of your index>` in the Redis CLI. Note that this will *not* drop your actual data unless you pass `DD`
#### Empty queries when using metadata
If you add metadata to the index *after* it has already been created and then try to query over that metadata, your queries will come back empty.
Redis indexes fields upon index creation only (similar to how it indexes the prefixes, above).

[1] https://hub.docker.com/r/redis/redis-stack
[2] https://redis.com/try-free
[3] https://redisvl.com
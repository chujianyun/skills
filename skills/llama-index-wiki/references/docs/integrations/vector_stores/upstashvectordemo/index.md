# developers.llamaindex.ai/python/framework/integrations/vector_stores/upstashvectordemo/index.md
> https://developers.llamaindex.ai/python/framework/integrations/vector_stores/upstashvectordemo/index.md

--- title: Upstash Vector Store | Developer Documentation ---
We’re going to look at how to use LlamaIndex to interface with Upstash Vector!
``` ! pip install -q llama-index upstash-vector ```
``` from llama_index.core import VectorStoreIndex, SimpleDirectoryReader from llama_index.core.vector_stores import UpstashVectorStore from llama_index.core import StorageContext import textwrap import openai ```
``` # Setup the OpenAI API openai.api_key = "sk-..." ```

``` # Download data ! mkdir -p 'data/paul_graham/' ! wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt' ```

``` --2024-02-03 20:04:25-- https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt Resolving raw.githubusercontent.com (raw.githubusercontent.com)... 185.199.108.133, 185.199.109.133, 185.199.110.133, ... Connecting to raw.githubusercontent.com (raw.githubusercontent.com)|185.199.108.133|:443... connected. HTTP request sent, awaiting response... 200 OK Length: 75042 (73K) [text/plain] Saving to: ‘data/paul_graham/paul_graham_essay.txt’

data/paul_graham/pa 100%[===================>] 73.28K --.-KB/s in 0.01s
2024-02-03 20:04:25 (5.96 MB/s) - ‘data/paul_graham/paul_graham_essay.txt’ saved [75042/75042] ```
Now, we can load the documents using the LlamaIndex SimpleDirectoryReader
``` documents = SimpleDirectoryReader("./data/paul_graham/").load_data()
print("# Documents:", len(documents)) ```
``` # Documents: 1 ```

To create an index on Upstash, visit <https://console.upstash.com/vector>, create an index with 1536 dimensions and `Cosine` distance metric. Copy the URL and token below

``` vector_store = UpstashVectorStore(url="https://...", token="...")
storage_context = StorageContext.from_defaults(vector_store=vector_store) index = VectorStoreIndex.from_documents( documents, storage_context=storage_context ) ```

Now we’ve successfully created an index and populated it with vectors from the essay! The data will take a second to index and then it’ll be ready for querying.

``` query_engine = index.as_query_engine() res1 = query_engine.query("What did the author learn?") print(textwrap.fill(str(res1), 100))
print("\n")
res2 = query_engine.query("What is the author's opinion on startups?") print(textwrap.fill(str(res2), 100)) ```
``` The author learned that the study of philosophy in college did not live up to their expectations. They found that other fields took up most of the space of ideas, leaving little room for what they perceived as the ultimate truths that philosophy was supposed to explore. As a result, they decided to switch to studying AI.

The author's opinion on startups is that they are in need of help and support, especially in the beginning stages. The author believes that founders of startups are often helpless and face various challenges, such as getting incorporated and understanding the intricacies of running a company. The author's investment firm, Y Combinator, aims to provide seed funding and comprehensive support to startups, offering them the guidance and resources they need to succeed. ```

### Metadata Filtering
You can pass `MetadataFilters` with your `VectorStoreQuery` to filter the nodes returned from Upstash vector store.
``` import os
from llama_index.vector_stores.upstash import UpstashVectorStore from llama_index.core.vector_stores.types import ( MetadataFilter, MetadataFilters, FilterOperator, )

vector_store = UpstashVectorStore( url=os.environ.get("UPSTASH_VECTOR_URL") or "", token=os.environ.get("UPSTASH_VECTOR_TOKEN") or "", )
index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
filters = MetadataFilters( filters=[ MetadataFilter( key="author", value="Marie Curie", operator=FilterOperator.EQ ) ], )

retriever = index.as_retriever(filters=filters)
retriever.retrieve("What is inception about?") ```
We can also combine multiple `MetadataFilters` with `AND` or `OR` condition
``` from llama_index.core.vector_stores import FilterOperator, FilterCondition
filters = MetadataFilters( filters=[ MetadataFilter( key="theme", value=["Fiction", "Horror"], operator=FilterOperator.IN, ), MetadataFilter(key="year", value=1997, operator=FilterOperator.GT), ], condition=FilterCondition.AND, )

retriever = index.as_retriever(filters=filters) retriever.retrieve("Harry Potter?") ```
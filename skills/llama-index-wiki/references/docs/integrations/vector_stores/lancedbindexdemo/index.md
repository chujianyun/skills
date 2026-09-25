# developers.llamaindex.ai/python/framework/integrations/vector_stores/lancedbindexdemo/index.md
> https://developers.llamaindex.ai/python/framework/integrations/vector_stores/lancedbindexdemo/index.md

--- title: LanceDB Vector Store | Developer Documentation ---

In this notebook we are going to show how to use LanceDB [1] to perform vector searches in LlamaIndex
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.
``` %pip install llama-index llama-index-vector-stores-lancedb ```
``` %pip install lancedb==0.6.13 #Only required if the above cell installs an older version of lancedb (pypi package may not be released yet) ```
``` # Refresh vector store URI if restarting or re-using the same notebook ! rm -rf ./lancedb ```

``` import logging import sys

# Uncomment to see debug logs # logging.basicConfig(stream=sys.stdout, level=logging.DEBUG) # logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

from llama_index.core import SimpleDirectoryReader, Document, StorageContext from llama_index.core import VectorStoreIndex from llama_index.vector_stores.lancedb import LanceDBVectorStore import textwrap ```

### Setup OpenAI
The first step is to configure the openai key. It will be used to created embeddings for the documents loaded into the index
``` import openai
openai.api_key = "sk-" ```
Download Data
``` !mkdir -p 'data/paul_graham/' !wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt' ```

``` --2024-06-11 16:42:37-- https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt Resolving raw.githubusercontent.com (raw.githubusercontent.com)... 185.199.109.133, 185.199.110.133, 185.199.108.133, ... Connecting to raw.githubusercontent.com (raw.githubusercontent.com)|185.199.109.133|:443... connected. HTTP request sent, awaiting response... 200 OK Length: 75042 (73K) [text/plain] Saving to: ‘data/paul_graham/paul_graham_essay.txt’

data/paul_graham/pa 100%[===================>] 73.28K --.-KB/s in 0.02s
2024-06-11 16:42:37 (3.97 MB/s) - ‘data/paul_graham/paul_graham_essay.txt’ saved [75042/75042] ```
### Loading documents
Load the documents stored in the `data/paul_graham/` using the SimpleDirectoryReader
``` documents = SimpleDirectoryReader("./data/paul_graham/").load_data() print("Document ID:", documents[0].doc_id, "Document Hash:", documents[0].hash) ```

``` Document ID: cac1ba78-5007-4cf8-89ba-280264790115 Document Hash: fe2d4d3ef3a860780f6c2599808caa587c8be6516fe0ba4ca53cf117044ba953 ```
### Create the index
Here we create an index backed by LanceDB using the documents loaded previously. LanceDBVectorStore takes a few arguments.
- uri (str, required): Location where LanceDB will store its files.
- table\_name (str, optional): The table name where the embeddings will be stored. Defaults to “vectors”.
- nprobes (int, optional): The number of probes used. A higher number makes search more accurate but also slower. Defaults to 20.
- refine\_factor: (int, optional): Refine the results by reading extra elements and re-ranking them in memory. Defaults to None
- More details can be found at LanceDB docs [2]
##### For LanceDB cloud :
```` vector_store = LanceDBVectorStore( uri="db://db_name", # your remote DB URI api_key="sk_..", # lancedb cloud api key region="your-region" # the region you configured ... )

```python vector_store = LanceDBVectorStore( uri="./lancedb", mode="overwrite", query_type="hybrid" ) storage_context = StorageContext.from_defaults(vector_store=vector_store)

index = VectorStoreIndex.from_documents( documents, storage_context=storage_context ) ````

### Query the index
We can now ask questions using our index. We can use filtering via `MetadataFilters` or use native lance `where` clause.
``` from llama_index.core.vector_stores import ( MetadataFilters, FilterOperator, FilterCondition, MetadataFilter, )

from datetime import datetime

query_filters = MetadataFilters( filters=[ MetadataFilter( key="creation_date", operator=FilterOperator.EQ, value=datetime.now().strftime("%Y-%m-%d"), ), MetadataFilter( key="file_size", value=75040, operator=FilterOperator.GT ), ], condition=FilterCondition.AND, ) ```

### Hybrid Search
LanceDB offers hybrid search with reranking capabilities. For complete documentation, refer here [3].
This example uses the `colbert` reranker. The following cell installs the necessary dependencies for `colbert`. If you choose a different reranker, make sure to adjust the dependencies accordingly.
``` ! pip install -U torch transformers tantivy@git+https://github.com/quickwit-oss/tantivy-py#164adc87e1a033117001cf70e38c82a53014d985 ```
if you want to add a reranker at vector store initialization, you can pass it in the arguments like below :
``` from lancedb.rerankers import ColbertReranker reranker = ColbertReranker() vector_store = LanceDBVectorStore(uri="./lancedb", reranker=reranker, mode="overwrite") ```
``` import lancedb ```
``` from lancedb.rerankers import ColbertReranker
reranker = ColbertReranker() vector_store._add_reranker(reranker)
query_engine = index.as_query_engine( filters=query_filters, # vector_store_kwargs={ # "query_type": "fts", # }, )

response = query_engine.query("How much did Viaweb charge per month?") ```
``` print(response) print("metadata -", response.metadata) ```
``` Viaweb charged $100 a month for a small store and $300 a month for a big one. metadata - {'65ed5f07-5b8a-4143-a939-e8764884828e': {'file_path': '/Users/raghavdixit/Desktop/open_source/llama_index_lance/docs/examples/vector_stores/data/paul_graham/paul_graham_essay.txt', 'file_name': 'paul_graham_essay.txt', 'file_type': 'text/plain', 'file_size': 75042, 'creation_date': '2024-06-11', 'last_modified_date': '2024-06-11'}, 'be231827-20b8-4988-ac75-94fa79b3c22e': {'file_path': '/Users/raghavdixit/Desktop/open_source/llama_index_lance/docs/examples/vector_stores/data/paul_graham/paul_graham_essay.txt', 'file_name': 'paul_graham_essay.txt', 'file_type': 'text/plain', 'file_size': 75042, 'creation_date': '2024-06-11', 'last_modified_date': '2024-06-11'}}
```
##### lance filters(SQL like) directly via the `where` clause :
``` lance_filter = "metadata.file_name = 'paul_graham_essay.txt' " retriever = index.as_retriever(vector_store_kwargs={"where": lance_filter}) response = retriever.retrieve("What did the author do growing up?") ```
``` print(response[0].get_content()) print("metadata -", response[0].metadata) ```
``` What I Worked On
February 2021
Before college the two main things I worked on, outside of school, were writing and programming. I didn't write essays. I wrote what beginning writers were supposed to write then, and probably still are: short stories. My stories were awful. They had hardly any plot, just characters with strong feelings, which I imagined made them deep.
The first programs I tried writing were on the IBM 1401 that our school district used for what was then called "data processing." This was in 9th grade, so I was 13 or 14. The school district's 1401 happened to be in the basement of our junior high school, and my friend Rich Draves and I got permission to use it. It was like a mini Bond villain's lair down there, with all these alien-looking machines — CPU, disk drives, printer, card reader — sitting up on a raised floor under bright fluorescent lights.
The language we used was an early version of Fortran. You had to type programs on punch cards, then stack them in the card reader and press a button to load the program into memory and run it. The result would ordinarily be to print something on the spectacularly loud printer.
I was puzzled by the 1401. I couldn't figure out what to do with it. And in retrospect there's not much I could have done with it. The only form of input to programs was data stored on punched cards, and I didn't have any data stored on punched cards. The only other option was to do things that didn't rely on any input, like calculate approximations of pi, but I didn't know enough math to do anything interesting of that type. So I'm not surprised I can't remember any programs I wrote, because they can't have done much. My clearest memory is of the moment I learned it was possible for programs not to terminate, when one of mine didn't. On a machine without time-sharing, this was a social as well as a technical error, as the data center manager's expression made clear.
With microcomputers, everything changed. Now you could have a computer sitting right in front of you, on a desk, that could respond to your keystrokes as it was running instead of just churning through a stack of punch cards and then stopping. [1]
The first of my friends to get a microcomputer built it himself. It was sold as a kit by Heathkit. I remember vividly how impressed and envious I felt watching him sitting in front of it, typing programs right into the computer.
Computers were expensive in those days and it took me years of nagging before I convinced my father to buy one, a TRS-80, in about 1980. The gold standard then was the Apple II, but a TRS-80 was good enough. This was when I really started programming. I wrote simple games, a program to predict how high my model rockets would fly, and a word processor that my father used to write at least one book. There was only room in memory for about 2 pages of text, so he'd write 2 pages at a time and then print them out, but it was a lot better than a typewriter.
Though I liked programming, I didn't plan to study it in college. In college I was going to study philosophy, which sounded much more powerful. It seemed, to my naive high school self, to be the study of the ultimate truths, compared to which the things studied in other fields would be mere domain knowledge. What I discovered when I got to college was that the other fields took up so much of the space of ideas that there wasn't much left for these supposed ultimate truths. All that seemed left for philosophy were edge cases that people in other fields felt could safely be ignored.
I couldn't have put this into words when I was 18. All I knew at the time was that I kept taking philosophy courses and they kept being boring. So I decided to switch to AI.
AI was in the air in the mid 1980s, but there were two things especially that made me want to work on it: a novel by Heinlein called The Moon is a Harsh Mistress, which featured an intelligent computer called Mike, and a PBS documentary that showed Terry Winograd using SHRDLU. I haven't tried rereading The Moon is a Harsh Mistress, so I don't know how well it has aged, but when I read it I was drawn entirely into its world. metadata - {'file_path': '/Users/raghavdixit/Desktop/open_source/llama_index_lance/docs/examples/vector_stores/data/paul_graham/paul_graham_essay.txt', 'file_name': 'paul_graham_essay.txt', 'file_type': 'text/plain', 'file_size': 75042, 'creation_date': '2024-06-11', 'last_modified_date': '2024-06-11'} ```
### Appending data
You can also add data to an existing index
``` nodes = [node.node for node in response] ```

index = VectorStoreIndex.from_documents( [Document(text="The sky is purple in Portland, Maine")], uri="/tmp/new_dataset", ) ```
``` index.insert_nodes(nodes) ```
``` query_engine = index.as_query_engine() response = query_engine.query("Where is the sky purple?") print(textwrap.fill(str(response), 100)) ```
``` Portland, Maine ```
You can also create an index from an existing table
``` del index
vec_store = LanceDBVectorStore.from_table(vector_store._table) index = VectorStoreIndex.from_vector_store(vec_store) ```
``` query_engine = index.as_query_engine() response = query_engine.query("What companies did the author start?") print(textwrap.fill(str(response), 100)) ```
``` The author started Viaweb and Aspra. ```

[1] https://www.lancedb.com
[2] https://lancedb.github.io/lancedb/ann_indexes
[3] https://lancedb.github.io/lancedb/hybrid_search/hybrid_search/
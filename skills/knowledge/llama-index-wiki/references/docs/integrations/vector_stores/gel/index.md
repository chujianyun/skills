# developers.llamaindex.ai/python/framework/integrations/vector_stores/gel/index.md
> https://developers.llamaindex.ai/python/framework/integrations/vector_stores/gel/index.md

--- title: Gel Vector Store | Developer Documentation ---

Gel [1] is an open-source PostgreSQL data layer optimized for fast development to production cycle. It comes with a high-level strictly typed graph-like data model, composable hierarchical query language, full SQL support, migrations, Auth and AI modules.

If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.
``` ! pip install gel llama-index-vector-stores-gel ```
``` ! pip install llama-index ```
``` # import logging # import sys

# Uncomment to see debug logs # logging.basicConfig(stream=sys.stdout, level=logging.DEBUG) # logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

from llama_index.core import SimpleDirectoryReader, StorageContext from llama_index.core import VectorStoreIndex from llama_index.vector_stores.gel import GelVectorStore import textwrap import openai ```

### Setup OpenAI
The first step is to configure the openai key. It will be used to created embeddings for the documents loaded into the index
``` import os
os.environ["OPENAI_API_KEY"] = "<your key>" openai.api_key = os.environ["OPENAI_API_KEY"] ```
Download Data

``` !mkdir -p 'data/paul_graham/' !wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt' ```

### Loading documents
Load the documents stored in the `data/paul_graham/` using the SimpleDirectoryReader
``` documents = SimpleDirectoryReader("./data/paul_graham").load_data() print("Document ID:", documents[0].doc_id) ```

### Create the Database

In order to use Gel as a backend for your vectorstore, you’re going to need a working Gel instance. Fortunately, it doesn’t have to involve Docker containers or anything complicated, unless you want to!

To set up a local instance, run:
``` ! gel project init --non-interactive ```
If you are using Gel Cloud (and you should!), add one more argument to that command:
Terminal window
``` gel project init --server-instance <org-name>/<instance-name> ```
For a comprehensive list of ways to run Gel, take a look at Running Gel [2] section of the reference docs.
### Set up the schema

Gel schema [3] is an explicit high-level description of your application’s data model. Aside from enabling you to define exactly how your data is going to be laid out, it drives Gel’s many powerful features such as links, access policies, functions, triggers, constraints, indexes, and more.

The LlamaIndex’s `GelVectorStore` expects the following layout for the schema:
``` schema_content = """ using extension pgvector;
module default { scalar type EmbeddingVector extending ext::pgvector::vector<1536>;
type Record { required collection: str; text: str; embedding: EmbeddingVector; external_id: str { constraint exclusive; }; metadata: json;

index ext::pgvector::hnsw_cosine(m := 16, ef_construction := 128) on (.embedding) } } """.strip()
with open("dbschema/default.gel", "w") as f: f.write(schema_content) ```

In order to apply schema changes to the database, run the migration using the Gel’s migration tool [4]:

``` ! gel migration create --non-interactive ! gel migrate ```

From this point onward, `GelVectorStore` can be used as a drop-in replacement for any other vectorstore available in LlamaIndex.
### Create the index

storage_context = StorageContext.from_defaults(vector_store=vector_store) index = VectorStoreIndex.from_documents( documents, storage_context=storage_context, show_progress=True ) query_engine = index.as_query_engine() ```

### Query the index
We can now ask questions using our index.
``` response = query_engine.query("What did the author do?") ```

``` response = query_engine.query("What happened in the mid 1980s?") ```
``` print(textwrap.fill(str(response), 100)) ```
### Metadata filters
GelVectorStore supports storing metadata in nodes, and filtering based on that metadata during the retrieval step.
#### Download git commits dataset
``` !mkdir -p 'data/git_commits/' !wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/csv/commit_history.csv' -O 'data/git_commits/commit_history.csv' ```

``` import csv
with open("data/git_commits/commit_history.csv", "r") as f: commits = list(csv.DictReader(f))
print(commits[0]) print(len(commits)) ```
#### Add nodes with custom metadata
``` # Create TextNode for each of the first 100 commits from llama_index.core.schema import TextNode from datetime import datetime import re

nodes = [] dates = set() authors = set() for commit in commits[:100]: author_email = commit["author"].split("<")[1][:-1] commit_date = datetime.strptime( commit["date"], "%a %b %d %H:%M:%S %Y %z" ).strftime("%Y-%m-%d") commit_text = commit["change summary"] if commit["change details"]: commit_text += "\n\n" + commit["change details"] fixes = re.findall(r"#(\d+)", commit_text, re.IGNORECASE) nodes.append( TextNode( text=commit_text, metadata={ "commit_date": commit_date, "author": author_email, "fixes": fixes, }, ) ) dates.add(commit_date) authors.add(author_email)

print(nodes[0]) print(min(dates), "to", max(dates)) print(authors) ```

``` vector_store = GelVectorStore()
index = VectorStoreIndex.from_vector_store(vector_store=vector_store) index.insert_nodes(nodes) ```
``` print(index.as_query_engine().query("How did Lakshmi fix the segfault?")) ```
#### Apply metadata filters
Now we can filter by commit author or by date when retrieving nodes.
``` from llama_index.core.vector_stores.types import ( MetadataFilter, MetadataFilters, )

filters = MetadataFilters( filters=[ MetadataFilter(key="author", value="mats@timescale.com"), MetadataFilter(key="author", value="sven@timescale.com"), ], condition="or", )

``` filters = MetadataFilters( filters=[ MetadataFilter(key="commit_date", value="2023-08-15", operator=">="), MetadataFilter(key="commit_date", value="2023-08-25", operator="<="), ], condition="and", )

#### Apply nested filters
In the above examples, we combined multiple filters using AND or OR. We can also combine multiple sets of filters.
``` filters = MetadataFilters( filters=[ MetadataFilters( filters=[ MetadataFilter( key="commit_date", value="2023-08-01", operator=">=" ), MetadataFilter( key="commit_date", value="2023-08-15", operator="<=" ), ], condition="and", ), MetadataFilters( filters=[ MetadataFilter(key="author", value="mats@timescale.com"), MetadataFilter(key="author", value="sven@timescale.com"), ], condition="or", ), ], condition="and", )

The above can be simplified by using the IN operator. `GelVectorStore` supports `in`, `nin`, and `contains` for comparing an element with a list.
``` filters = MetadataFilters( filters=[ MetadataFilter(key="commit_date", value="2023-08-01", operator=">="), MetadataFilter(key="commit_date", value="2023-08-15", operator="<="), MetadataFilter( key="author", value=["mats@timescale.com", "sven@timescale.com"], operator="in", ), ], condition="and", )

``` # Same thing, with NOT IN filters = MetadataFilters( filters=[ MetadataFilter(key="commit_date", value="2023-08-01", operator=">="), MetadataFilter(key="commit_date", value="2023-08-15", operator="<="), MetadataFilter( key="author", value=["mats@timescale.com", "sven@timescale.com"], operator="nin", ), ], condition="and", )

retrieved_nodes = retriever.retrieve("What is this software project about?")
for node in retrieved_nodes: print(node.node.metadata) ```
``` # CONTAINS filters = MetadataFilters( filters=[ MetadataFilter(key="fixes", value="5680", operator="contains"), ] )

retriever = index.as_retriever( similarity_top_k=10, filters=filters, )
retrieved_nodes = retriever.retrieve("How did these commits fix the issue?") for node in retrieved_nodes: print(node.node.metadata) ```

[1] https://www.geldata.com/
[2] https://docs.geldata.com/reference/running
[3] https://docs.geldata.com/reference/datamodel
[4] https://docs.geldata.com/reference/datamodel/migrations
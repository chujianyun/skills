# developers.llamaindex.ai/python/framework/integrations/vector_stores/postgres/index.md
> https://developers.llamaindex.ai/python/framework/integrations/vector_stores/postgres/index.md

--- title: Postgres Vector Store | Developer Documentation ---

In this notebook we are going to show how to use Postgresql [1] and pgvector [2] to perform vector searches in LlamaIndex

If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.
``` %pip install llama-index-vector-stores-postgres ```
``` !pip install llama-index ```
Running the following cell will install Postgres with PGVector in Colab.
``` !sudo apt update !echo | sudo apt install -y postgresql-common !echo | sudo /usr/share/postgresql-common/pgdg/apt.postgresql.org.sh !echo | sudo apt install postgresql-15-pgvector !sudo service postgresql start !sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'password';" !sudo -u postgres psql -c "CREATE DATABASE vector_db;" ```

``` # import logging # import sys

# Uncomment to see debug logs # logging.basicConfig(stream=sys.stdout, level=logging.DEBUG) # logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

from llama_index.core import SimpleDirectoryReader, StorageContext from llama_index.core import VectorStoreIndex from llama_index.vector_stores.postgres import PGVectorStore import textwrap ```

### Setup OpenAI
The first step is to configure the openai key. It will be used to created embeddings for the documents loaded into the index
``` import os
os.environ["OPENAI_API_KEY"] = "sk-..." ```
Download Data

``` !mkdir -p 'data/paul_graham/' !wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt' ```

### Loading documents
Load the documents stored in the `data/paul_graham/` using the SimpleDirectoryReader
``` documents = SimpleDirectoryReader("./data/paul_graham").load_data() print("Document ID:", documents[0].doc_id) ```

``` Document ID: 56e70c8c-0fb7-4250-99be-b953d0185a01 ```
### Create the Database
Using an existing postgres running at localhost, create the database we’ll be using.
``` import psycopg2
connection_string = "postgresql://postgres:password@localhost:5432" db_name = "vector_db" conn = psycopg2.connect(connection_string) conn.autocommit = True

with conn.cursor() as c: c.execute(f"DROP DATABASE IF EXISTS {db_name}") c.execute(f"CREATE DATABASE {db_name}") ```

### Create the index

Here we create an index backed by Postgres using the documents loaded previously. PGVectorStore takes a few arguments. The example below constructs a PGVectorStore with a HNSW index with m = 16, ef\_construction = 64, and ef\_search = 40, with the `vector_cosine_ops` method.

url = make_url(connection_string) vector_store = PGVectorStore.from_params( database=db_name, host=url.host, password=url.password, port=url.port, user=url.username, table_name="paul_graham_essay", embed_dim=1536, # openai embedding dimension hnsw_kwargs={ "hnsw_m": 16, "hnsw_ef_construction": 64, "hnsw_ef_search": 40, "hnsw_dist_method": "vector_cosine_ops", }, )

storage_context = StorageContext.from_defaults(vector_store=vector_store) index = VectorStoreIndex.from_documents( documents, storage_context=storage_context, show_progress=True ) query_engine = index.as_query_engine() ```
``` Parsing nodes: 0%| | 0/1 [00:00<?, ?it/s]

Generating embeddings: 0%| | 0/22 [00:00<?, ?it/s]

2025-09-11 16:47:21,725 - INFO - HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK" ```
### Query the index
We can now ask questions using our index.

``` 2025-09-11 16:47:30,412 - INFO - HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK" 2025-09-11 16:47:31,665 - INFO - HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK" ```

``` The author worked on writing essays, programming, building microcomputers, predicting rocket heights, developing a word processor, and giving talks on starting a startup. ```
``` response = query_engine.query("What happened in the mid 1980s?") ```
``` 2025-09-11 16:47:37,531 - INFO - HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK" 2025-09-11 16:47:38,352 - INFO - HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK" ```

``` AI was in the air in the mid 1980s, and two things that influenced the desire to work on it were a novel by Heinlein called The Moon is a Harsh Mistress, which featured an intelligent computer called Mike, and a PBS documentary that showed Terry Winograd using SHRDLU. ```
### Querying existing index
``` vector_store = PGVectorStore.from_params( database="vector_db", host="localhost", password="password", port=5432, user="postgres", table_name="paul_graham_essay", embed_dim=1536, # openai embedding dimension hnsw_kwargs={ "hnsw_m": 16, "hnsw_ef_construction": 64, "hnsw_ef_search": 40, "hnsw_dist_method": "vector_cosine_ops", }, )

index = VectorStoreIndex.from_vector_store(vector_store=vector_store) query_engine = index.as_query_engine() ```
``` response = query_engine.query("What did the author do?") ```
``` print(textwrap.fill(str(response), 100)) ```
``` The author worked on writing essays, programming, creating microcomputers, developing software, giving talks, and starting a startup. ```
### Hybrid Search
To enable hybrid search, you need to:

1. pass in `hybrid_search=True` when constructing the `PGVectorStore` (and optionally configure `text_search_config` with the desired language) 2. pass in `vector_store_query_mode="hybrid"` when constructing the query engine (this config is passed to the retriever under the hood). You can also optionally set the `sparse_top_k` to configure how many results we should obtain from sparse text search (default is using the same value as `similarity_top_k`).

``` from sqlalchemy import make_url
url = make_url(connection_string) hybrid_vector_store = PGVectorStore.from_params( database=db_name, host=url.host, password=url.password, port=url.port, user=url.username, table_name="paul_graham_essay_hybrid_search", embed_dim=1536, # openai embedding dimension hybrid_search=True, text_search_config="english", hnsw_kwargs={ "hnsw_m": 16, "hnsw_ef_construction": 64, "hnsw_ef_search": 40, "hnsw_dist_method": "vector_cosine_ops", }, )

storage_context = StorageContext.from_defaults( vector_store=hybrid_vector_store ) hybrid_index = VectorStoreIndex.from_documents( documents, storage_context=storage_context ) ```
``` hybrid_query_engine = hybrid_index.as_query_engine( vector_store_query_mode="hybrid", sparse_top_k=2 ) hybrid_response = hybrid_query_engine.query( "Who does Paul Graham think of with the word schtick" ) ```

``` print(hybrid_response) ```
``` Roy Lichtenstein ```
#### Improving hybrid search with QueryFusionRetriever
Since the scores for text search and vector search are calculated differently, the nodes that were found only by text search will have a much lower score.
You can often improve hybrid search performance by using `QueryFusionRetriever`, which makes better use of the mutual information to rank the nodes.
``` from llama_index.core.response_synthesizers import CompactAndRefine from llama_index.core.retrievers import QueryFusionRetriever from llama_index.core.query_engine import RetrieverQueryEngine
vector_retriever = hybrid_index.as_retriever( vector_store_query_mode="default", similarity_top_k=5, ) text_retriever = hybrid_index.as_retriever( vector_store_query_mode="sparse", similarity_top_k=5, # interchangeable with sparse_top_k in this context ) retriever = QueryFusionRetriever( [vector_retriever, text_retriever], similarity_top_k=5, num_queries=1, # set this to 1 to disable query generation mode="relative_score", use_async=False, )

response_synthesizer = CompactAndRefine() query_engine = RetrieverQueryEngine( retriever=retriever, response_synthesizer=response_synthesizer, ) ```
``` response = query_engine.query( "Who does Paul Graham think of with the word schtick, and why?" ) print(response) ```

``` Paul Graham thinks of Roy Lichtenstein when using the word "schtick" because Lichtenstein's distinctive signature style in his paintings immediately identifies his work as his own. ```

### Metadata filters
PGVectorStore supports storing metadata in nodes, and filtering based on that metadata during the retrieval step.
#### Download git commits dataset
``` !mkdir -p 'data/git_commits/' !wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/csv/commit_history.csv' -O 'data/git_commits/commit_history.csv' ```

``` import csv
with open("data/git_commits/commit_history.csv", "r") as f: commits = list(csv.DictReader(f))
print(commits[0]) print(len(commits)) ```

``` {'commit': '44e41c12ab25e36c202f58e068ced262eadc8d16', 'author': 'Lakshmi Narayanan Sreethar<lakshmi@timescale.com>', 'date': 'Tue Sep 5 21:03:21 2023 +0530', 'change summary': 'Fix segfault in set_integer_now_func', 'change details': 'When an invalid function oid is passed to set_integer_now_func, it finds out that the function oid is invalid but before throwing the error, it calls ReleaseSysCache on an invalid tuple causing a segfault. Fixed that by removing the invalid call to ReleaseSysCache. Fixes #6037 '}

4167 ```
#### Add nodes with custom metadata
``` # Create TextNode for each of the first 100 commits from llama_index.core.schema import TextNode from datetime import datetime import re

nodes = [] dates = set() authors = set() for commit in commits[:100]: author_email = commit["author"].split("<")[1][:-1] commit_date = datetime.strptime( commit["date"], "%a %b %d %H:%M:%S %Y %z" ).strftime("%Y-%m-%d") commit_text = commit["change summary"] if commit["change details"]: commit_text += "\n\n" + commit["change details"] fixes = re.findall(r"#(\d+)", commit_text, re.IGNORECASE) nodes.append( TextNode( text=commit_text, metadata={ "commit_date": commit_date, "author": author_email, "fixes": fixes, }, ) ) dates.add(commit_date) authors.add(author_email)

print(nodes[0]) print(min(dates), "to", max(dates)) print(authors) ```

``` Node ID: 9c2c2f17-d763-4ce8-bb02-83cb176008e4 Text: Fix segfault in set_integer_now_func When an invalid function oid is passed to set_integer_now_func, it finds out that the function oid is invalid but before throwing the error, it calls ReleaseSysCache on an invalid tuple causing a segfault. Fixed that by removing the invalid call to ReleaseSysCache. Fixes #6037 2023-03-22 to 2023-09-05 {'konstantina@timescale.com', 'nikhil@timescale.com', 'satish.8483@gmail.com', 'mats@timescale.com', 'fabriziomello@gmail.com', 'erik@timescale.com', 'sven@timescale.com', 'lakshmi@timescale.com', 'dmitry@timescale.com', 'engel@sero-systems.de', 'rafia.sabih@gmail.com', '36882414+akuzm@users.noreply.github.com', 'jguthrie@timescale.com', 'jan@timescale.com', 'me@noctarius.com'} ```

``` vector_store = PGVectorStore.from_params( database=db_name, host=url.host, password=url.password, port=url.port, user=url.username, table_name="metadata_filter_demo3", embed_dim=1536, # openai embedding dimension hnsw_kwargs={ "hnsw_m": 16, "hnsw_ef_construction": 64, "hnsw_ef_search": 40, "hnsw_dist_method": "vector_cosine_ops", }, )

index = VectorStoreIndex.from_vector_store(vector_store=vector_store) index.insert_nodes(nodes) ```
``` 2025-09-11 16:48:11,383 - INFO - HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK" ```
``` print(index.as_query_engine().query("How did Lakshmi fix the segfault?")) ```
``` 2025-09-11 16:48:15,149 - INFO - HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK" 2025-09-11 16:48:15,687 - INFO - HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"

Lakshmi fixed the segfault by removing the invalid call to ReleaseSysCache that was causing the issue. ```
#### Apply metadata filters
Now we can filter by commit author or by date when retrieving nodes.
``` from llama_index.core.vector_stores.types import ( MetadataFilter, MetadataFilters, )

filters = MetadataFilters( filters=[ MetadataFilter(key="author", value="mats@timescale.com"), MetadataFilter(key="author", value="sven@timescale.com"), ], condition="or", )

``` 2025-09-11 16:48:31,673 - INFO - HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
{'commit_date': '2023-08-07', 'author': 'mats@timescale.com', 'fixes': []} {'commit_date': '2023-08-27', 'author': 'sven@timescale.com', 'fixes': []} {'commit_date': '2023-07-13', 'author': 'mats@timescale.com', 'fixes': []} {'commit_date': '2023-08-07', 'author': 'sven@timescale.com', 'fixes': []} {'commit_date': '2023-08-30', 'author': 'sven@timescale.com', 'fixes': []} {'commit_date': '2023-08-15', 'author': 'sven@timescale.com', 'fixes': []} {'commit_date': '2023-08-23', 'author': 'sven@timescale.com', 'fixes': []} {'commit_date': '2023-08-10', 'author': 'mats@timescale.com', 'fixes': []} {'commit_date': '2023-07-25', 'author': 'mats@timescale.com', 'fixes': ['5892']} {'commit_date': '2023-08-21', 'author': 'sven@timescale.com', 'fixes': []} ```
``` filters = MetadataFilters( filters=[ MetadataFilter(key="commit_date", value="2023-08-15", operator=">="), MetadataFilter(key="commit_date", value="2023-08-25", operator="<="), ], condition="and", )

``` 2025-09-11 16:48:40,347 - INFO - HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"

{'commit_date': '2023-08-23', 'author': 'erik@timescale.com', 'fixes': []} {'commit_date': '2023-08-17', 'author': 'konstantina@timescale.com', 'fixes': []} {'commit_date': '2023-08-15', 'author': '36882414+akuzm@users.noreply.github.com', 'fixes': []} {'commit_date': '2023-08-15', 'author': '36882414+akuzm@users.noreply.github.com', 'fixes': []} {'commit_date': '2023-08-24', 'author': 'lakshmi@timescale.com', 'fixes': []} {'commit_date': '2023-08-15', 'author': 'sven@timescale.com', 'fixes': []} {'commit_date': '2023-08-23', 'author': 'sven@timescale.com', 'fixes': []} {'commit_date': '2023-08-21', 'author': 'sven@timescale.com', 'fixes': []} {'commit_date': '2023-08-20', 'author': 'sven@timescale.com', 'fixes': []} {'commit_date': '2023-08-21', 'author': 'sven@timescale.com', 'fixes': []} ```

#### Apply nested filters
In the above examples, we combined multiple filters using AND or OR. We can also combine multiple sets of filters.
e.g. in SQL:
``` WHERE (commit_date >= '2023-08-01' AND commit_date <= '2023-08-15') AND (author = 'mats@timescale.com' OR author = 'sven@timescale.com') ```
``` filters = MetadataFilters( filters=[ MetadataFilters( filters=[ MetadataFilter( key="commit_date", value="2023-08-01", operator=">=" ), MetadataFilter( key="commit_date", value="2023-08-15", operator="<=" ), ], condition="and", ), MetadataFilters( filters=[ MetadataFilter(key="author", value="mats@timescale.com"), MetadataFilter(key="author", value="sven@timescale.com"), ], condition="or", ), ], condition="and", )

``` 2025-09-11 16:48:45,021 - INFO - HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"

The above can be simplified by using the IN operator. `PGVectorStore` supports `in`, `nin`, and `contains` for comparing an element with a list.
``` filters = MetadataFilters( filters=[ MetadataFilter(key="commit_date", value="2023-08-01", operator=">="), MetadataFilter(key="commit_date", value="2023-08-15", operator="<="), MetadataFilter( key="author", value=["mats@timescale.com", "sven@timescale.com"], operator="in", ), ], condition="and", )

``` 2025-09-11 16:48:49,129 - INFO - HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
{'commit_date': '2023-08-07', 'author': 'mats@timescale.com', 'fixes': []} {'commit_date': '2023-08-07', 'author': 'sven@timescale.com', 'fixes': []} {'commit_date': '2023-08-15', 'author': 'sven@timescale.com', 'fixes': []} {'commit_date': '2023-08-10', 'author': 'mats@timescale.com', 'fixes': []} ```
``` # Same thing, with NOT IN filters = MetadataFilters( filters=[ MetadataFilter(key="commit_date", value="2023-08-01", operator=">="), MetadataFilter(key="commit_date", value="2023-08-15", operator="<="), MetadataFilter( key="author", value=["mats@timescale.com", "sven@timescale.com"], operator="nin", ), ], condition="and", )

retrieved_nodes = retriever.retrieve("What is this software project about?")
for node in retrieved_nodes: print(node.node.metadata) ```
``` 2025-09-11 16:48:51,587 - INFO - HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
{'commit_date': '2023-08-09', 'author': 'me@noctarius.com', 'fixes': ['5805']} {'commit_date': '2023-08-15', 'author': '36882414+akuzm@users.noreply.github.com', 'fixes': []} {'commit_date': '2023-08-15', 'author': '36882414+akuzm@users.noreply.github.com', 'fixes': []} {'commit_date': '2023-08-11', 'author': '36882414+akuzm@users.noreply.github.com', 'fixes': []} {'commit_date': '2023-08-09', 'author': 'konstantina@timescale.com', 'fixes': ['5923', '5680', '5774', '5786', '5906', '5912']} {'commit_date': '2023-08-03', 'author': 'dmitry@timescale.com', 'fixes': []} {'commit_date': '2023-08-03', 'author': 'dmitry@timescale.com', 'fixes': ['5908']} {'commit_date': '2023-08-01', 'author': 'nikhil@timescale.com', 'fixes': []} {'commit_date': '2023-08-10', 'author': 'konstantina@timescale.com', 'fixes': []} {'commit_date': '2023-08-10', 'author': '36882414+akuzm@users.noreply.github.com', 'fixes': []} ```

``` # CONTAINS filters = MetadataFilters( filters=[ MetadataFilter(key="fixes", value="5680", operator="contains"), ] )

``` 2025-09-11 16:48:56,822 - INFO - HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
{'commit_date': '2023-08-09', 'author': 'konstantina@timescale.com', 'fixes': ['5923', '5680', '5774', '5786', '5906', '5912']} ```
### Customize queries

It is possible to build more complex queries such as joining other tables. This is done by setting the `customize_query_fn` argument with your function. First, lets create a user table and populate it.

``` from sqlalchemy import ( Table, MetaData, Column, String, Integer, create_engine, insert, )

engine = create_engine(url=connection_string + "/" + db_name)
metadata = MetaData()
user_table = Table( "user", metadata, Column("id", Integer, primary_key=True, autoincrement=True), Column("name", String, nullable=False), Column("email", String, nullable=False), )

user_table.drop(engine, checkfirst=True) user_table.create(engine)
with engine.begin() as conn: stmt = insert(user_table) conn.execute( stmt, [{"name": "Konstantina", "email": "konstantina@timescale.com"}] ) ```

Then, we can create a query customization function and instantiate `PGVectorStore` with `customize_query_fn`.
``` from typing import Any from sqlalchemy import Select

def customize_query(query: Select, table_class: Any, **kwargs: Any) -> Select: # Join the user table on the email addresses and add the name column to the select statement return query.add_columns(user_table.c.name).join( user_table, user_table.c.email == table_class.metadata_["author"].astext, )

vector_store = PGVectorStore.from_params( database=db_name, host=url.host, password=url.password, port=url.port, user=url.username, table_name="metadata_filter_demo3", embed_dim=1536, # openai embedding dimension hnsw_kwargs={ "hnsw_m": 16, "hnsw_ef_construction": 64, "hnsw_ef_search": 40, "hnsw_dist_method": "vector_cosine_ops", }, customize_query_fn=customize_query, ) index = VectorStoreIndex.from_vector_store(vector_store=vector_store) ```

We can then query the vector store and retrieve any additional field added to the select statement in a dictionary named `custom_fields` in the node metadata.

``` filters = MetadataFilters( filters=[ MetadataFilter(key="fixes", value="5680", operator="contains"), ] )
retriever = index.as_retriever( similarity_top_k=10, filters=filters, )
retrieved_nodes = retriever.retrieve("How did these commits fix the issue?") for node in retrieved_nodes: print(node.node.metadata) ```
``` 2025-09-11 17:06:43,812 - INFO - HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"

{'commit_date': '2023-08-09', 'author': 'konstantina@timescale.com', 'fixes': ['5923', '5680', '5774', '5786', '5906', '5912'], 'custom_fields': {'name': 'Konstantina'}} ```

### PgVector Query Options
#### IVFFlat Probes
Specify the number of IVFFlat probes [3] (1 by default)
When retrieving from the index, you can specify an appropriate number of IVFFlat probes (higher is better for recall, lower is better for speed)
``` retriever = index.as_retriever( vector_store_query_mode="hybrid", similarity_top_k=5, vector_store_kwargs={"ivfflat_probes": 10}, ) ```

#### HNSW EF Search
Specify the size of the dynamic candidate list [4] for search (40 by default)
``` retriever = index.as_retriever( vector_store_query_mode="hybrid", similarity_top_k=5, vector_store_kwargs={"hnsw_ef_search": 300}, ) ```

[1] https://www.postgresql.org
[2] https://github.com/pgvector/pgvector
[3] https://github.com/pgvector/pgvector?tab=readme-ov-file#query-options
[4] https://github.com/pgvector/pgvector?tab=readme-ov-file#query-options-1
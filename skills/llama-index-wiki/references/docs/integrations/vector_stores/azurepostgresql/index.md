# developers.llamaindex.ai/python/framework/integrations/vector_stores/azurepostgresql/index.md
> https://developers.llamaindex.ai/python/framework/integrations/vector_stores/azurepostgresql/index.md

--- title: Azure Postgres Vector Store | Developer Documentation ---

In this notebook we are going to show how to use Azure Postgresql [1] and pg\_diskann [2] to perform vector searches in LlamaIndex. Please note that this document is mostly based on the document for PostgreSQL integration [3] to simplify the transition.

``` !pip install llama-index ```
``` %load_ext sql ```
``` import subprocess import os from urllib.parse import quote_plus
cmd = [ "az", "account", "get-access-token", "--resource", "https://ossrdbms-aad.database.windows.net", "--query", "accessToken", "--output", "tsv", ]

try: token = subprocess.check_output(cmd, text=True).strip() except subprocess.CalledProcessError as exc: raise RuntimeError(f"Failed to run command: {exc}") from exc os.environ["PGPASSWORD"] = token ```
``` %sql postgresql:// ```
Connecting to ‘postgresql://’
``` %%sql drop table if exists llamaindex_vectors; ```

``` import logging import sys import os
# Uncomment to see debug logs # logging.basicConfig(stream=sys.stdout, level=logging.DEBUG) # logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))
from llama_index.core import ( SimpleDirectoryReader, StorageContext, VectorStoreIndex, ) from llama_index.core.settings import Settings from llama_index.llms.azure_openai import AzureOpenAI from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding import textwrap

# Import from the local file from llama_index.vector_stores.azure_postgres import AzurePGVectorStore from llama_index.vector_stores.azure_postgres.common import ( AzurePGConnectionPool, DiskANN, VectorOpClass, ) ```

### Setup OpenAI
The first step is to configure the Azure openai key. It will be used to created embeddings for the documents loaded into the index
``` import os
# Method 1: Using os.environ.get() with fallback values aoai_api_key = os.environ.get("AOAI_API_KEY", "key") aoai_endpoint = os.environ.get("AOAI_ENDPOINT", "endpoint") aoai_api_version = os.environ.get("AOAI_API_VERSION", "2024-12-01-preview")
llm = AzureOpenAI( model="o4-mini", deployment_name="o4-mini", api_key=aoai_api_key, azure_endpoint=aoai_endpoint, api_version=aoai_api_version, )

# You need to deploy your own embedding model as well as your own chat completion model embed_model = AzureOpenAIEmbedding( model="text-embedding-3-small", deployment_name="text-embedding-3-small", api_key=aoai_api_key, azure_endpoint=aoai_endpoint, api_version=aoai_api_version, ) ```

Download Data

``` !mkdir -p 'data/paul_graham/' !wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt' ```

``` --2025-09-03 15:56:56-- https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt Resolving raw.githubusercontent.com (raw.githubusercontent.com)... 185.199.108.133, 185.199.109.133, 185.199.111.133, ... Connecting to raw.githubusercontent.com (raw.githubusercontent.com)|185.199.108.133|:443... connected. HTTP request sent, awaiting response... 200 OK Length: 75042 (73K) [text/plain] Saving to: ‘data/paul_graham/paul_graham_essay.txt’

data/paul_graham/pa 100%[===================>] 73.28K --.-KB/s in 0.1s
2025-09-03 15:56:56 (765 KB/s) - ‘data/paul_graham/paul_graham_essay.txt’ saved [75042/75042] ```
### Loading documents
Load the documents stored in the `data/paul_graham/` using the SimpleDirectoryReader
``` documents = SimpleDirectoryReader("./data/paul_graham").load_data() print("Document ID:", documents[0].doc_id) ```

``` Document ID: 4a7a27c2-6013-408b-aa3d-65fd89b824d8 ```
### Create the Database

Using an existing postgres instance running on Azure, we will use Microsoft Entra authentication to connect to the database. Please make sure you are logged in to your Azure account.

``` host = os.environ.get("PGHOST", "<your_host>") port = int(os.environ.get("PGPORT", 5432)) database = os.environ.get("PGDATABASE", "postgres") from psycopg import Connection from psycopg.rows import dict_row from llama_index.vector_stores.azure_postgres.common import ( ConnectionInfo, create_extensions, Extension, )
def configure_connection(conn: Connection) -> None: conn.autocommit = True create_extensions(conn, [Extension(ext_name="vector")]) create_extensions(conn, [Extension(ext_name="pg_diskann")]) conn.row_factory = dict_row
azure_conn_info: ConnectionInfo = ConnectionInfo( host=host, port=port, dbname=database, configure=configure_connection ) conn = AzurePGConnectionPool( azure_conn_info=azure_conn_info, ) ```
### Create the vector store

Here we create an index backed by Postgres using the documents loaded previously. AzurePGVectorStore takes a few arguments. The example below constructs a PGVectorStore with no index.

``` vector_store = AzurePGVectorStore.from_params( connection_pool=conn, table_name="llamaindex_vectors", embed_dim=1536, # openai embedding dimension )
Settings.llm = llm Settings.embed_model = embed_model storage_context = StorageContext.from_defaults(vector_store=vector_store) index = VectorStoreIndex.from_documents( documents, storage_context=storage_context, show_progress=True ) query_engine = index.as_query_engine() ```

``` Embedding type is not specified, defaulting to 'vector'. Embedding dimension is not specified, defaulting to 1536. Embedding index is not specified, defaulting to 'DiskANN' with 'vector_cosine_ops' opclass. /home/kislalorhan/workspace/myenv/lib/python3.12/site-packages/tqdm/auto.py:21: TqdmWarning: IProgress not found. Please update jupyter and ipywidgets. See https://ipywidgets.readthedocs.io/en/stable/user_install.html from .autonotebook import tqdm as notebook_tqdm Parsing nodes: 100%|██████████| 1/1 [00:00<00:00, 11.88it/s] Generating embeddings: 100%|██████████| 22/22 [00:02<00:00, 9.54it/s] ```

### Query the dataset
We can now ask questions.

``` He pursued two parallel creative tracks—writing and programming. • As a teenager he wrote (admittedly “awful”) short stories and taught himself to program on his school’s IBM 1401, later moving on to a TRS-80 where he wrote simple games, a model-rocket flight predictor, and even a small word processor. • In college he initially majored in philosophy but switched to AI, became fascinated by Lisp, and decided to write a book on Lisp hacking. Much of what became On Lisp was drafted during his grad-school years. • At the same time, seeking a more permanent art form, he began taking painting classes at Harvard, planning to make and earn a living from paintings that, unlike software, wouldn’t become obsolete. ```

``` response = query_engine.query("What happened in the mid 1980s?") print(textwrap.fill(str(response), 100)) ```
``` Artificial intelligence became a hot topic. Two specific influences drove that surge of interest: - Heinlein’s science-fiction novel The Moon Is a Harsh Mistress, featuring the self-aware computer “Mike” - A PBS documentary demonstrating Terry Winograd’s SHRDLU natural-language program ```
### Querying existing index

Now, we create a pg\_diskann index with max\_neighbors = 32, l\_value\_ib = 100, and l\_value\_is = 100, with the `vector_cosine_ops` method on our embeddings and use it with a new vector store.

``` %%sql create index on llamaindex_vectors using diskann (embedding vector_cosine_ops) with ( max_neighbors = 32, l_value_ib = 100 ); set diskann.l_value_is to 100; ```

Running query in ‘postgresql://‘
| | | - |
``` diskann = DiskANN( op_class=VectorOpClass.vector_cosine_ops, max_neighbors=32, l_value_ib=100, l_value_is=100, ) ```

``` vector_store = AzurePGVectorStore.from_params( connection_pool=conn, schema_name="public", table_name="llamaindex_vectors", embed_dim=1536, # openai embedding dimension embedding_index=diskann, )

index = VectorStoreIndex.from_vector_store(vector_store=vector_store) query_engine = index.as_query_engine() ```

``` [{'schema_name': 'public', 'table_name': 'llamaindex_vectors', 'index_name': 'llamaindex_vectors_embedding_idx', 'index_type': 'diskann', 'index_column': 'embedding', 'index_opclass': 'vector_cosine_ops', 'index_opts': ['max_neighbors=32', 'l_value_ib=100']}] ```

``` response = query_engine.query("What did the author do?") print(textwrap.fill(str(response), 100)) ```

``` He spent his spare time writing (mostly really bad short stories) and learning to program. As a teenager he punched out Fortran jobs on an IBM 1401, then moved on to a TRS-80 microcomputer, where he wrote simple games, a model-rocket flight predictor, and even a tiny word-processor. ```

### Access individual nodes
Read a specific node by its id.
``` nodes = vector_store.get_nodes() print(len(nodes)) node_id = nodes[0].node_id print(node_id) nodes = vector_store.get_nodes([node_id]) print(nodes[0]) ```

``` 22 3dd2f695-1def-431b-ae2c-2561472a0272 Node ID: 3dd2f695-1def-431b-ae2c-2561472a0272 Text: What I Worked On February 2021 Before college the two main things I worked on, outside of school, were writing and programming. I didn't write essays. I wrote what beginning writers were supposed to write then, and probably still are: short stories. My stories were awful. They had hardly any plot, just characters with strong feelings, which I ... ```

Delete a single node and then the whole table.
``` vector_store.delete_nodes(node_ids=[node_id]) nodes = vector_store.get_nodes() print(len(nodes)) vector_store.clear() # delete all nodes = vector_store.get_nodes() print(len(nodes)) ```

``` 21 ```
### Metadata filters
AzurePGVectorStore supports storing metadata in nodes, and filtering based on that metadata during the retrieval step.
#### Download git commits dataset
``` # !mkdir -p 'data/csv/' # !wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/csv/commit_history_2.csv' -O 'data/csv/commit_history_2.csv' import builtins import csv

# TODO: Once the PR is merged: Change this to with open("data/csv/commit_history_2.csv", "r") as f: with builtins.open("../data/csv/commit_history_2.csv", "r") as f: commits = list(csv.DictReader(f))

print(commits[0]) print(len(commits)) ```

``` {'commit': '03baef1008086ed4960042fa463e570072173bb5', 'author': 'Benjamin Christopher Simmonds <44439583+benibenj@users.noreply.github.com>', 'date': 'Mon Aug 25 13:01:24 2025 +0200', 'change summary': 'Support registering views to the secondary side bar (#261619)', 'change details': "* Support registering views to the secondary side bar\\n\\n* rename to secondarySideBar\\n\\n* Rename 'auxiliarybar' to 'secondarySidebar'"} 169 ```

#### Add nodes with custom metadata
``` # Create TextNode for each of the first 100 commits from llama_index.core.schema import TextNode from datetime import datetime import re

nodes = [] dates = set() authors = set() for commit in commits[:100]: author_email = commit["author"].split("<")[1][:-1] commit_date = datetime.strptime( commit["date"], "%a %b %d %H:%M:%S %Y %z" ).strftime("%Y-%m-%d") commit_text = commit["change summary"] if commit["change details"]: commit_text += "\n\n" + commit["change details"] fixes = re.findall(r"#(\d+)", commit_text, re.IGNORECASE) nodes.append( TextNode( text=commit_text, metadata={ "commit_date": commit_date, "author": author_email, "fixes": fixes, }, ) ) dates.add(commit_date) authors.add(author_email)

print(nodes[0]) print(min(dates), "to", max(dates)) print(authors) ```

``` Node ID: 9a06a469-32bc-4dd3-90a7-d6b933e7ad3f Text: Support registering views to the secondary side bar (#261619) * Support registering views to the secondary side bar\n\n* rename to secondarySideBar\n\n* Rename 'auxiliarybar' to 'secondarySidebar' 2025-08-18 to 2025-08-25 {'benjamin.pasero@microsoft.com', 'lramos15@gmail.com', 'matb@microsoft.com', 'mpg@mpg.is', '23246594+joshspicer@users.noreply.github.com', '2644648+TylerLeonhardt@users.noreply.github.com', '62267334+anthonykim1@users.noreply.github.com', '2193314+Tyriar@users.noreply.github.com', '3372902+lszomoru@users.noreply.github.com', 'martinae@microsoft.com', '38270282+alexr00@users.noreply.github.com', 'copeet@microsoft.com', 'rwoll@users.noreply.github.com', 'merogge@microsoft.com', '44439583+benibenj@users.noreply.github.com', '4821+timheuer@users.noreply.github.com', '49699333+dependabot[bot]@users.noreply.github.com', '54879025+justschen@users.noreply.github.com', 'bhavyau@microsoft.com', 'roblourens@gmail.com', 'ethanbovard@hotmail.com', 'hkirschner@microsoft.com', 'hop2deep@gmail.com', '198982749+Copilot@users.noreply.github.com', 'amarlenkyzy@microsoft.com'}

```
``` vector_store = AzurePGVectorStore.from_params( connection_pool=conn, schema_name="public", table_name="metadata_filter_demo3", embed_dim=1536, # openai embedding dimension )

index = VectorStoreIndex.from_vector_store(vector_store=vector_store) index.insert_nodes(nodes) ```
``` Embedding type is not specified, defaulting to 'vector'. Embedding dimension is not specified, defaulting to 1536. Embedding index is not specified, defaulting to 'DiskANN' with 'vector_cosine_ops' opclass. ```
``` print(index.as_query_engine().query("How did Leonhardt allow modal?")) ```

``` He added an opt-in “automation” mode that swaps in custom dialog windows (and a simple file picker) so that modal dialogs can be surfaced and driven under automation. ```

#### Apply metadata filters
Now we can filter by commit author or by date when retrieving nodes.
``` from llama_index.core.vector_stores.types import ( MetadataFilter, MetadataFilters, )

filters = MetadataFilters( filters=[ MetadataFilter(key="author", value="matb@microsoft.com"), MetadataFilter(key="author", value="benjamin.pasero@microsoft.com"), ], condition="or", )

``` filters = MetadataFilters( filters=[ MetadataFilter(key="commit_date", value="2025-08-20", operator=">="), MetadataFilter(key="commit_date", value="2025-08-25", operator="<="), ], condition="and", )

``` {'commit_date': '2025-08-22', 'author': '2644648+TylerLeonhardt@users.noreply.github.com', 'fixes': ['262984']} {'commit_date': '2025-08-22', 'author': '198982749+Copilot@users.noreply.github.com', 'fixes': ['261705']} {'commit_date': '2025-08-20', 'author': 'bhavyau@microsoft.com', 'fixes': ['262619']} {'commit_date': '2025-08-21', 'author': 'merogge@microsoft.com', 'fixes': ['262732', '252515']} {'commit_date': '2025-08-22', 'author': '54879025+justschen@users.noreply.github.com', 'fixes': ['262975']} {'commit_date': '2025-08-20', 'author': 'matb@microsoft.com', 'fixes': []} {'commit_date': '2025-08-21', 'author': '198982749+Copilot@users.noreply.github.com', 'fixes': ['262214']} {'commit_date': '2025-08-21', 'author': '2644648+TylerLeonhardt@users.noreply.github.com', 'fixes': ['262510']} {'commit_date': '2025-08-21', 'author': '54879025+justschen@users.noreply.github.com', 'fixes': ['262802']} {'commit_date': '2025-08-22', 'author': '54879025+justschen@users.noreply.github.com', 'fixes': ['262951']} ```

#### Apply nested filters
In the above examples, we combined multiple filters using AND or OR. We can also combine multiple sets of filters.
e.g. in SQL:
``` WHERE (commit_date >= '2025-08-20' AND commit_date <= '2023-08-25') AND (author = 'matb@microsoft.com' OR author = 'benjamin.pasero@microsoft.com') ```
``` filters = MetadataFilters( filters=[ MetadataFilters( filters=[ MetadataFilter( key="commit_date", value="2025-08-20", operator=">=" ), MetadataFilter( key="commit_date", value="2025-08-25", operator="<=" ), ], condition="and", ), MetadataFilters( filters=[ MetadataFilter(key="author", value="matb@microsoft.com"), MetadataFilter( key="author", value="benjamin.pasero@microsoft.com" ), ], condition="or", ), ], condition="and", )

``` {'commit_date': '2025-08-20', 'author': 'matb@microsoft.com', 'fixes': []} {'commit_date': '2025-08-20', 'author': 'matb@microsoft.com', 'fixes': []} {'commit_date': '2025-08-20', 'author': 'matb@microsoft.com', 'fixes': []} {'commit_date': '2025-08-22', 'author': 'benjamin.pasero@microsoft.com', 'fixes': ['262878']} {'commit_date': '2025-08-21', 'author': 'matb@microsoft.com', 'fixes': ['262772', '262772']} {'commit_date': '2025-08-21', 'author': 'matb@microsoft.com', 'fixes': []} {'commit_date': '2025-08-20', 'author': 'benjamin.pasero@microsoft.com', 'fixes': ['262444', '262417']} {'commit_date': '2025-08-25', 'author': 'benjamin.pasero@microsoft.com', 'fixes': ['263211']} {'commit_date': '2025-08-20', 'author': 'matb@microsoft.com', 'fixes': ['262472']} {'commit_date': '2025-08-22', 'author': 'benjamin.pasero@microsoft.com', 'fixes': ['5761', '262439']} ```

The above can be simplified by using the IN operator. `AzurePGVectorStore` supports `in`, `nin`, and `contains` for comparing an element with a list.
``` filters = MetadataFilters( filters=[ MetadataFilter(key="commit_date", value="2025-08-15", operator=">="), MetadataFilter(key="commit_date", value="2025-08-20", operator="<="), MetadataFilter( key="author", value=["matb@microsoft.com", "benjamin.pasero@microsoft.com"], operator="in", ), ], condition="and", )

``` {'commit_date': '2025-08-20', 'author': 'matb@microsoft.com', 'fixes': []} {'commit_date': '2025-08-20', 'author': 'matb@microsoft.com', 'fixes': []} {'commit_date': '2025-08-20', 'author': 'matb@microsoft.com', 'fixes': []} {'commit_date': '2025-08-20', 'author': 'benjamin.pasero@microsoft.com', 'fixes': ['262444', '262417']} {'commit_date': '2025-08-20', 'author': 'matb@microsoft.com', 'fixes': ['262472']} {'commit_date': '2025-08-18', 'author': 'matb@microsoft.com', 'fixes': []} {'commit_date': '2025-08-19', 'author': 'matb@microsoft.com', 'fixes': []} {'commit_date': '2025-08-20', 'author': 'matb@microsoft.com', 'fixes': ['262508']} {'commit_date': '2025-08-20', 'author': 'matb@microsoft.com', 'fixes': []} {'commit_date': '2025-08-18', 'author': 'matb@microsoft.com', 'fixes': ['262219']} ```
``` # Same thing, with NOT IN filters = MetadataFilters( filters=[ MetadataFilter(key="commit_date", value="2025-08-15", operator=">="), MetadataFilter(key="commit_date", value="2025-08-20", operator="<="), MetadataFilter( key="author", value=["matb@microsoft.com", "benjamin.pasero@microsoft.com"], operator="nin", ), ], condition="and", )

retrieved_nodes = retriever.retrieve("What is this software project about?")
for node in retrieved_nodes: print(node.node.metadata) ```
``` {'commit_date': '2025-08-20', 'author': 'bhavyau@microsoft.com', 'fixes': ['262619']} {'commit_date': '2025-08-19', 'author': '3372902+lszomoru@users.noreply.github.com', 'fixes': ['262276']} {'commit_date': '2025-08-19', 'author': '54879025+justschen@users.noreply.github.com', 'fixes': ['262239']} {'commit_date': '2025-08-18', 'author': 'roblourens@gmail.com', 'fixes': ['262222', '260539']} {'commit_date': '2025-08-19', 'author': '2644648+TylerLeonhardt@users.noreply.github.com', 'fixes': ['262417']} {'commit_date': '2025-08-19', 'author': '54879025+justschen@users.noreply.github.com', 'fixes': ['262362']} {'commit_date': '2025-08-18', 'author': '2644648+TylerLeonhardt@users.noreply.github.com', 'fixes': ['262260']} {'commit_date': '2025-08-20', 'author': '2644648+TylerLeonhardt@users.noreply.github.com', 'fixes': ['262564']} {'commit_date': '2025-08-19', 'author': '198982749+Copilot@users.noreply.github.com', 'fixes': []} {'commit_date': '2025-08-19', 'author': '198982749+Copilot@users.noreply.github.com', 'fixes': []} ```

``` # CONTAINS filters = MetadataFilters( filters=[ MetadataFilter(key="fixes", value="5680", operator="contains"), ] )

retriever = index.as_retriever( similarity_top_k=10, filters=filters, )
retrieved_nodes = retriever.retrieve("How did these commits fix the issue?") for node in retrieved_nodes: print(node.node.metadata) ```

[1] https://azure.microsoft.com/en-au/products/postgresql
[2] https://github.com/microsoft/DiskANN
[3] https://docs.llamaindex.ai/en/stable/examples/vector_stores/postgres/
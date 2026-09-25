# developers.llamaindex.ai/python/framework/integrations/vector_stores/cassandraindexdemo/index.md
> https://developers.llamaindex.ai/python/framework/integrations/vector_stores/cassandraindexdemo/index.md

--- title: Cassandra Vector Store | Developer Documentation ---

Apache Cassandra® [1] is a NoSQL, row-oriented, highly scalable and highly available database. Starting with version 5.0, the database ships with [vector search] [2] capabilities.
DataStax Astra DB through CQL [3] is a managed serverless database built on Cassandra, offering the same interface and strengths.
**This notebook shows the basic usage of the Cassandra Vector Store in LlamaIndex.**
To run the full code you need either a running Cassandra cluster equipped with Vector Search capabilities or a DataStax Astra DB instance.
## Setup
``` %pip install llama-index-vector-stores-cassandra ```
``` !pip install --quiet "astrapy>=0.5.8" ```
``` import os from getpass import getpass

from llama_index.core import ( VectorStoreIndex, SimpleDirectoryReader, Document, StorageContext, ) from llama_index.vector_stores.cassandra import CassandraVectorStore ```

The next step is to initialize CassIO with a global DB connection: this is the only step that is done slightly differently for a Cassandra cluster and Astra DB:
### Initialization (Cassandra cluster)
In this case, you first need to create a `cassandra.cluster.Session` object, as described in the Cassandra driver documentation [4]. The details vary (e.g. with network settings and authentication), but this might be something like:
``` from cassandra.cluster import Cluster
cluster = Cluster(["127.0.0.1"]) session = cluster.connect() ```

CASSANDRA_KEYSPACE = input("CASSANDRA_KEYSPACE = ")
cassio.init(session=session, keyspace=CASSANDRA_KEYSPACE) ```
### Initialization (Astra DB through CQL)
In this case you initialize CassIO with the following connection parameters:
- the Database ID, e.g. 01234567-89ab-cdef-0123-456789abcdef - the Token, e.g. AstraCS:6gBhNmsk135… (it must be a “Database Administrator” token) - Optionally a Keyspace name (if omitted, the default one for the database will be used)
``` ASTRA_DB_ID = input("ASTRA_DB_ID = ") ASTRA_DB_TOKEN = getpass("ASTRA_DB_TOKEN = ")

desired_keyspace = input("ASTRA_DB_KEYSPACE (optional, can be left empty) = ") if desired_keyspace: ASTRA_DB_KEYSPACE = desired_keyspace else: ASTRA_DB_KEYSPACE = None ```

``` ASTRA_DB_ID = 01234567-89ab-cdef-0123-456789abcdef ASTRA_DB_TOKEN = ········ ASTRA_DB_KEYSPACE (optional, can be left empty) = ```

``` import cassio
cassio.init( database_id=ASTRA_DB_ID, token=ASTRA_DB_TOKEN, keyspace=ASTRA_DB_KEYSPACE, ) ```

### OpenAI key
In order to use embeddings by OpenAI you need to supply an OpenAI API Key:
``` os.environ["OPENAI_API_KEY"] = getpass("OpenAI API Key:") ```
``` OpenAI API Key: ········ ```
### Download data
``` !mkdir -p 'data/paul_graham/' !wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt' ```

``` --2023-11-10 01:44:05-- https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt Resolving raw.githubusercontent.com (raw.githubusercontent.com)... 185.199.109.133, 185.199.110.133, 185.199.111.133, ... Connecting to raw.githubusercontent.com (raw.githubusercontent.com)|185.199.109.133|:443... connected. HTTP request sent, awaiting response... 200 OK Length: 75042 (73K) [text/plain] Saving to: ‘data/paul_graham/paul_graham_essay.txt’

data/paul_graham/pa 100%[===================>] 73.28K --.-KB/s in 0.01s
2023-11-10 01:44:06 (4.80 MB/s) - ‘data/paul_graham/paul_graham_essay.txt’ saved [75042/75042] ```
## Creating and populating the Vector Store
You will now load some essays by Paul Graham from a local file and store them into the Cassandra Vector Store.
``` # load documents documents = SimpleDirectoryReader("./data/paul_graham/").load_data() print(f"Total documents: {len(documents)}") print(f"First document, id: {documents[0].doc_id}") print(f"First document, hash: {documents[0].hash}") print( "First document, text" f" ({len(documents[0].text)} characters):\n{'='*20}\n{documents[0].text[:360]} ..." ) ```

``` Total documents: 1 First document, id: 12bc6987-366a-49eb-8de0-7b52340e4958 First document, hash: abe31930a1775c78df5a5b1ece7108f78fedbf5fe4a9cf58d7a21808fccaef34 First document, text (75014 characters): ====================

What I Worked On

Before college the two main things I worked on, outside of school, were writing and programming. I didn't write essays. I wrote what beginning writers were supposed to write then, and probably still are: short stories. My stories were awful. They had hardly any plot, just characters with strong feelings, which I imagined ma ... ```
### Initialize the Cassandra Vector Store
Creation of the vector store entails creation of the underlying database table if it does not exist yet:
``` cassandra_store = CassandraVectorStore( table="cass_v_table", embedding_dimension=1536 ) ```

Now wrap this store into an `index` LlamaIndex abstraction for later querying:
``` storage_context = StorageContext.from_defaults(vector_store=cassandra_store)
index = VectorStoreIndex.from_documents( documents, storage_context=storage_context ) ```

Note that the above `from_documents` call does several things at once: it splits the input documents into chunks of manageable size (“nodes”), computes embedding vectors for each node, and stores them all in the Cassandra Vector Store.
## Querying the store
### Basic querying
``` query_engine = index.as_query_engine() response = query_engine.query("Why did the author choose to work on AI?") print(response.response) ```

``` The author chose to work on AI because they were inspired by a novel called The Moon is a Harsh Mistress, which featured an intelligent computer, and a PBS documentary that showed Terry Winograd using SHRDLU. These experiences sparked the author's interest in AI and motivated them to pursue it as a field of study and work. ```

### MMR-based queries
The MMR (maximal marginal relevance) method is designed to fetch text chunks from the store that are at the same time relevant to the query but as different as possible from each other, with the goal of providing a broader context to the building of the final answer:
``` query_engine = index.as_query_engine(vector_store_query_mode="mmr") response = query_engine.query("Why did the author choose to work on AI?") print(response.response) ```

``` The author chose to work on AI because they believed that teaching SHRDLU more words would eventually lead to the development of intelligent programs. They were fascinated by the potential of AI and saw it as an opportunity to expand their understanding of programming and push the limits of what could be achieved. ```

## Connecting to an existing store
Since this store is backed by Cassandra, it is persistent by definition. So, if you want to connect to a store that was created and populated previously, here is how:
``` new_store_instance = CassandraVectorStore( table="cass_v_table", embedding_dimension=1536 )

# Create index (from preexisting stored vectors) new_index_instance = VectorStoreIndex.from_vector_store( vector_store=new_store_instance )

# now you can do querying, etc: query_engine = new_index_instance.as_query_engine(similarity_top_k=5) response = query_engine.query( "What did the author study prior to working on AI?" ) ```

``` print(response.response) ```
``` The author studied philosophy prior to working on AI. ```
## Removing documents from the index
First get an explicit list of pieces of a document, or “nodes”, from a `Retriever` spawned from the index:
``` retriever = new_index_instance.as_retriever( vector_store_query_mode="mmr", similarity_top_k=3, vector_store_kwargs={"mmr_prefetch_factor": 4}, ) nodes_with_scores = retriever.retrieve( "What did the author study prior to working on AI?" ) ```

``` print(f"Found {len(nodes_with_scores)} nodes.") for idx, node_with_score in enumerate(nodes_with_scores): print(f" [{idx}] score = {node_with_score.score}") print(f" id = {node_with_score.node.node_id}") print(f" text = {node_with_score.node.text[:90]} ...") ```

``` Found 3 nodes. [0] score = 0.4251742327832831 id = 7e628668-58fa-4548-9c92-8c31d315dce0 text = What I Worked On

February 2021
Before college the two main things I worked on, outside o ... [1] score = -0.020323897262800816 id = aa279d09-717f-4d68-9151-594c5bfef7ce text = This was now only weeks away. My nice landlady let me leave my stuff in her attic. I had s ... [2] score = 0.011198131320563909 id = 50b9170d-6618-4e8b-aaf8-36632e2801a6 text = It seemed only a matter of time before we'd have Mike, and when I saw Winograd using SHRDL ... ```

But wait! When using the vector store, you should consider the **document** as the sensible unit to delete, and not any individual node belonging to it. Well, in this case, you just inserted a single text file, so all nodes will have the same `ref_doc_id`:
``` print("Nodes' ref_doc_id:") print("\n".join([nws.node.ref_doc_id for nws in nodes_with_scores])) ```

``` Nodes' ref_doc_id: 12bc6987-366a-49eb-8de0-7b52340e4958 12bc6987-366a-49eb-8de0-7b52340e4958 12bc6987-366a-49eb-8de0-7b52340e4958 ```

Now let’s say you need to remove the text file you uploaded:
``` new_store_instance.delete(nodes_with_scores[0].node.ref_doc_id) ```
Repeat the very same query and check the results now. You should see *no results* being found:
``` nodes_with_scores = retriever.retrieve( "What did the author study prior to working on AI?" )

print(f"Found {len(nodes_with_scores)} nodes.") ```
``` Found 0 nodes. ```
## Metadata filtering
The Cassandra vector store support metadata filtering in the form of exact-match `key=value` pairs at query time. The following cells, which work on a brand new Cassandra table, demonstrate this feature.
In this demo, for the sake of brevity, a single source document is loaded (the `../data/paul_graham/paul_graham_essay.txt` text file). Nevertheless, you will attach some custom metadata to the document to illustrate how you can can restrict queries with conditions on the metadata attached to the documents.
``` md_storage_context = StorageContext.from_defaults( vector_store=CassandraVectorStore( table="cass_v_table_md", embedding_dimension=1536 ) )

def my_file_metadata(file_name: str): """Depending on the input file name, associate a different metadata.""" if "essay" in file_name: source_type = "essay" elif "dinosaur" in file_name: # this (unfortunately) will not happen in this demo source_type = "dinos" else: source_type = "other" return {"source_type": source_type}

[Column 1]
# Load documents and build index md_documents = SimpleDirectoryReader( "./data/paul_graham", file_metadata=my_file_metadata ).load_data() md_index = VectorStoreIndex.from_documents( md_documents, storage_context=md_storage_context ) ```

That’s it: you can now add filtering to your query engine:
``` from llama_index.core.vector_stores import ExactMatchFilter, MetadataFilters ```
``` md_query_engine = md_index.as_query_engine( filters=MetadataFilters( filters=[ExactMatchFilter(key="source_type", value="essay")] ) ) md_response = md_query_engine.query( "did the author appreciate Lisp and painting?" ) print(md_response.response) ```

To test that the filtering is at play, try to change it to use only `"dinos"` documents… there will be no answer this time :)

[Column 2]
``` Yes, the author appreciated Lisp and painting. They mentioned spending a significant amount of time working on Lisp and even building a new dialect of Lisp called Arc. Additionally, the author mentioned spending most of 2014 painting and experimenting with different techniques. ```


[1] https://cassandra.apache.org
[2] https://cassandra.apache.org/doc/trunk/cassandra/vector-search/overview.html
[3] https://docs.datastax.com/en/astra-serverless/docs/vector-search/quickstart.html
[4] https://docs.datastax.com/en/developer/python-driver/latest/api/cassandra/cluster/#module- cassandra.cluster
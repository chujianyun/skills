# developers.llamaindex.ai/python/framework/integrations/vector_stores/orallamavs/index.md
> https://developers.llamaindex.ai/python/framework/integrations/vector_stores/orallamavs/index.md

--- title: Oracle AI Vector Search: Vector Store | Developer Documentation ---
Oracle AI Vector Search is designed for Artificial Intelligence (AI) workloads that allows you to query data based on semantics, rather than keywords. One of the biggest benefits of Oracle AI Vector Search is that semantic search on unstructured data can be combined with relational search on business data in one single system. This is not only powerful but also significantly more effective because you don’t need to add a specialized vector database, eliminating the pain of data fragmentation between multiple systems.
In addition, your vectors can benefit from all of Oracle Database’s most powerful features, like the following:
- Partitioning Support [1] - Real Application Clusters scalability [2] - Exadata smart scans [3] - Shard processing across geographically distributed databases [4] - Transactions [5] - Parallel SQL [6] - Disaster recovery [7] - Security [8] - Oracle Machine Learning [9] - Oracle Graph Database [10] - Oracle Spatial and Graph [11] - Oracle Blockchain [12] - JSON [13]

The guide demonstrates how to use Vector Capabilities within Oracle AI Vector Search.
If you are just starting with Oracle Database, consider exploring the free Oracle 23 AI [14] which provides a great introduction to setting up your database environment. While working with the database, it is often advisable to avoid using the system user by default; instead, you can create your own user for enhanced security and customization. For detailed steps on user creation, refer to our end-to-end guide [15] which also shows how to set up a user in Oracle. Additionally, understanding user privileges is crucial for managing database security effectively. You can learn more about this topic in the official Oracle guide [16] on administering user accounts and security.
### Prerequisites
Please install Oracle Python Client driver to use Llama Index with Oracle AI Vector Search.
``` %pip install llama-index-vector-stores-oracledb ```
### Connect to Oracle AI Vector Search
The following sample code will show how to connect to Oracle Database. By default, python-oracledb runs in a ‘Thin’ mode which connects directly to Oracle Database. This mode does not need Oracle Client libraries. However, some additional functionality is available when python-oracledb uses them. Python-oracledb is said to be in ‘Thick’ mode when Oracle Client libraries are used. Both modes have comprehensive functionality supporting the Python Database API v2.0 Specification. See the following guide [17] that talks about features supported in each mode. You might want to switch to thick-mode if you are unable to use thin-mode.
``` import oracledb
# please update with your username, password, hostname and service_name username = "<username>" password = "<password>" dsn = "<hostname>/<service_name>"
try: connection = oracledb.connect(user=username, password=password, dsn=dsn) print("Connection successful!") except Exception as ex: print("Exception occurred while index creation", ex) ```

### Import the required dependencies to play with Oracle AI Vector Search
``` import sys import os

from llama_index.core.schema import NodeRelationship, RelatedNodeInfo, TextNode from llama_index.core.vector_stores.types import ( ExactMatchFilter, MetadataFilters, VectorStoreQuery, )

from llama_index.vector_stores.oracledb import base as orallamavs from llama_index.vector_stores.oracledb import OraLlamaVS, DistanceStrategy ```
### Load Documents
``` # Define a list of documents (These dummy examples are 4 random documents )
text_json_list = [ { "text": "If the answer to any preceding questions is yes, then the database stops the search and allocates space from the specified tablespace; otherwise, space is allocated from the database default shared temporary tablespace.", "id_": "cncpt_15.5.3.2.2_P4", "embedding": [1.0, 0.0], "relationships": "test-0", "metadata": { "weight": 1.0, "rank": "a", "url": "https://docs.oracle.com/en/database/oracle/oracle-database/23/cncpt/logical-storage-structures.html#GUID-5387D7B2-C0CA-4C1E-811B-C7EB9B636442", }, }, { "text": "A tablespace can be online (accessible) or offline (not accessible) whenever the database is open.\nA tablespace is usually online so that its data is available to users. The SYSTEM tablespace and temporary tablespaces cannot be taken offline.", "id_": "cncpt_15.5.5_P1", "embedding": [0.0, 1.0], "relationships": "test-1", "metadata": { "weight": 2.0, "rank": "c", "url": "https://docs.oracle.com/en/database/oracle/oracle-database/23/cncpt/logical-storage-structures.html#GUID-D02B2220-E6F5-40D9-AFB5-BC69BCEF6CD4", }, }, { "text": "The database stores LOBs differently from other data types. Creating a LOB column implicitly creates a LOB segment and a LOB index. The tablespace containing the LOB segment and LOB index, which are always stored together, may be different from the tablespace containing the table.\nSometimes the database can store small amounts of LOB data in the table itself rather than in a separate LOB segment.",

"id_": "cncpt_22.3.4.3.1_P2", "embedding": [1.0, 1.0], "relationships": "test-2", "metadata": { "weight": 3.0, "rank": "d", "url": "https://docs.oracle.com/en/database/oracle/oracle-database/23/cncpt/concepts-for-database-developers.html#GUID-3C50EAB8-FC39-4BB3-B680-4EACCE49E866", }, }, { "text": "The LOB segment stores data in pieces called chunks. A chunk is a logically contiguous set of data blocks and is the smallest unit of allocation for a LOB. A row in the table stores a pointer called a LOB locator, which points to the LOB index. When the table is queried, the database uses the LOB index to quickly locate the LOB chunks.", "id_": "cncpt_22.3.4.3.1_P3", "embedding": [2.0, 1.0], "relationships": "test-3", "metadata": { "weight": 4.0, "rank": "e", "url": "https://docs.oracle.com/en/database/oracle/oracle-database/23/cncpt/concepts-for-database-developers.html#GUID-3C50EAB8-FC39-4BB3-B680-4EACCE49E866", }, }, ] ```

``` # Create Llama Text Nodes text_nodes = [] for text_json in text_json_list: # Construct the relationships using RelatedNodeInfo relationships = { NodeRelationship.SOURCE: RelatedNodeInfo( node_id=text_json["relationships"] ) }

# Prepare the metadata dictionary; you might want to exclude certain metadata fields if necessary metadata = { "weight": text_json["metadata"]["weight"], "rank": text_json["metadata"]["rank"], }

# Create a TextNode instance text_node = TextNode( text=text_json["text"], id_=text_json["id_"], embedding=text_json["embedding"], relationships=relationships, metadata=metadata, )

text_nodes.append(text_node) print(text_nodes) ```
### Using AI Vector Search Create a bunch of Vector Stores with different distance strategies
First we will create three vector stores each with different distance functions. Since we have not created indices in them yet, they will just create tables for now. Later we will use these vector stores to create HNSW indicies.
You can manually connect to the Oracle Database and will see three tables Documents\_DOT, Documents\_COSINE and Documents\_EUCLIDEAN.
We will then create three additional tables Documents\_DOT\_IVF, Documents\_COSINE\_IVF and Documents\_EUCLIDEAN\_IVF which will be used to create IVF indicies on the tables instead of HNSW indices.
To understand more about the different types of indices Oracle AI Vector Search supports, refer to the following guide [18]
``` # Ingest documents into Oracle Vector Store using different distance strategies
vector_store_dot = OraLlamaVS.from_documents( text_nodes, table_name="Documents_DOT", client=connection, distance_strategy=DistanceStrategy.DOT_PRODUCT, ) vector_store_max = OraLlamaVS.from_documents( text_nodes, table_name="Documents_COSINE", client=connection, distance_strategy=DistanceStrategy.COSINE, ) vector_store_euclidean = OraLlamaVS.from_documents( text_nodes, table_name="Documents_EUCLIDEAN", client=connection, distance_strategy=DistanceStrategy.EUCLIDEAN_DISTANCE, )

# Ingest documents into Oracle Vector Store using different distance strategies vector_store_dot_ivf = OraLlamaVS.from_documents( text_nodes, table_name="Documents_DOT_IVF", client=connection, distance_strategy=DistanceStrategy.DOT_PRODUCT, ) vector_store_max_ivf = OraLlamaVS.from_documents( text_nodes, table_name="Documents_COSINE_IVF", client=connection, distance_strategy=DistanceStrategy.COSINE, ) vector_store_euclidean_ivf = OraLlamaVS.from_documents( text_nodes, table_name="Documents_EUCLIDEAN_IVF", client=connection, distance_strategy=DistanceStrategy.EUCLIDEAN_DISTANCE, ) ```

### Demonstrating add, delete operations for texts, and basic similarity search
``` def manage_texts(vector_stores): """ Adds texts to each vector store, demonstrates error handling for duplicate additions, and performs deletion of texts. Showcases similarity searches and index creation for each vector store.

Args: - vector_stores (list): A list of OracleVS instances. """ for i, vs in enumerate(vector_stores, start=1): # Deleting texts using the value of 'id' vs.delete("test-1") print(f"\n\n\nDelete texts complete for vector store {i}\n\n\n")

# Similarity search query = VectorStoreQuery( query_embedding=[1.0, 1.0], similarity_top_k=3 ) results = vs.query(query=query) print( f"\n\n\nSimilarity search results for vector store {i}: {results}\n\n\n" )

vector_store_list = [ vector_store_dot, vector_store_max, vector_store_euclidean, vector_store_dot_ivf, vector_store_max_ivf, vector_store_euclidean_ivf, ] manage_texts(vector_store_list) ```

### Demonstrating index creation with specific parameters for each distance strategy
``` def create_search_indices(connection): """ Creates search indices for the vector stores, each with specific parameters tailored to their distance strategy. """ # Index for DOT_PRODUCT strategy # Notice we are creating a HNSW index with default parameters # This will default to creating a HNSW index with 8 Parallel Workers and use the Default Accuracy used by Oracle AI Vector Search orallamavs.create_index( connection, vector_store_dot, params={"idx_name": "hnsw_idx1", "idx_type": "HNSW"}, )

# Index for COSINE strategy with specific parameters # Notice we are creating a HNSW index with parallel 16 and Target Accuracy Specification as 97 percent orallamavs.create_index( connection, vector_store_max, params={ "idx_name": "hnsw_idx2", "idx_type": "HNSW", "accuracy": 97, "parallel": 16, }, )

# Index for EUCLIDEAN_DISTANCE strategy with specific parameters # Notice we are creating a HNSW index by specifying Power User Parameters which are neighbors = 64 and efConstruction = 100 orallamavs.create_index( connection, vector_store_euclidean, params={ "idx_name": "hnsw_idx3", "idx_type": "HNSW", "neighbors": 64, "efConstruction": 100, }, )

# Index for DOT_PRODUCT strategy with specific parameters # Notice we are creating an IVF index with default parameters # This will default to creating an IVF index with 8 Parallel Workers and use the Default Accuracy used by Oracle AI Vector Search orallamavs.create_index( connection, vector_store_dot_ivf, params={ "idx_name": "ivf_idx1", "idx_type": "IVF", }, )

# Index for COSINE strategy with specific parameters # Notice we are creating an IVF index with parallel 32 and Target Accuracy Specification as 90 percent orallamavs.create_index( connection, vector_store_max_ivf, params={ "idx_name": "ivf_idx2", "idx_type": "IVF", "accuracy": 90, "parallel": 32, }, )

# Index for EUCLIDEAN_DISTANCE strategy with specific parameters # Notice we are creating an IVF index by specifying Power User Parameters which is neighbor_part = 64 orallamavs.create_index( connection, vector_store_euclidean_ivf, params={ "idx_name": "ivf_idx3", "idx_type": "IVF", "neighbor_part": 64, }, )

print("Index creation complete.")
create_search_indices(connection) ```
### Now we will conduct a bunch of advanced searches on all six vector stores. Each of these three searches have a with and without filter version. The filter only selects the document with id 101 out and filters out everything else
``` # Conduct advanced searches after creating the indices def conduct_advanced_searches(vector_stores): # Constructing a filter for direct comparison against document metadata # This filter aims to include documents whose metadata 'id' is exactly '2'

for i, vs in enumerate(vector_stores, start=1):
def query_without_filters_returns_all_rows_sorted_by_similarity(): print(f"\n--- Vector Store {i} Advanced Searches ---") # Similarity search without a filter print("\nSimilarity search results without filter:") query = VectorStoreQuery( query_embedding=[1.0, 1.0], similarity_top_k=3 ) print(vs.query(query=query))

query_without_filters_returns_all_rows_sorted_by_similarity()
def query_with_filters_returns_multiple_matches(): print(f"\n--- Vector Store {i} Advanced Searches ---") # Similarity search with filter print("\nSimilarity search results without filter:") filters = MetadataFilters( filters=[ExactMatchFilter(key="rank", value="c")] ) query = VectorStoreQuery( query_embedding=[1.0, 1.0], filters=filters, similarity_top_k=1 ) result = vs.query(query) print(result.ids)

query_with_filters_returns_multiple_matches()
def query_with_filter_applies_top_k(): print(f"\n--- Vector Store {i} Advanced Searches ---") # Similarity search with a filter print("\nSimilarity search results with filter:") filters = MetadataFilters( filters=[ExactMatchFilter(key="rank", value="c")] ) query = VectorStoreQuery( query_embedding=[1.0, 1.0], filters=filters, similarity_top_k=1 ) result = vs.query(query) print(result.ids)

query_with_filter_applies_top_k()
def query_with_filter_applies_node_id_filter(): print(f"\n--- Vector Store {i} Advanced Searches ---") # Similarity search with a filter print("\nSimilarity search results with filter:") filters = MetadataFilters( filters=[ExactMatchFilter(key="rank", value="c")] ) query = VectorStoreQuery( query_embedding=[1.0, 1.0], filters=filters, similarity_top_k=3, node_ids=["452D24AB-F185-414C-A352-590B4B9EE51B"], ) result = vs.query(query) print(result.ids)

query_with_filter_applies_node_id_filter()
def query_with_exact_filters_returns_single_match(): print(f"\n--- Vector Store {i} Advanced Searches ---") # Similarity search with a filter print("\nSimilarity search results with filter:") filters = MetadataFilters( filters=[ ExactMatchFilter(key="rank", value="c"), ExactMatchFilter(key="weight", value=2), ] ) query = VectorStoreQuery( query_embedding=[1.0, 1.0], filters=filters ) result = vs.query(query) print(result.ids)

query_with_exact_filters_returns_single_match()
def query_with_contradictive_filter_returns_no_matches(): filters = MetadataFilters( filters=[ ExactMatchFilter(key="weight", value=2), ExactMatchFilter(key="weight", value=3), ] ) query = VectorStoreQuery( query_embedding=[1.0, 1.0], filters=filters ) result = vs.query(query) print(result.ids)

query_with_contradictive_filter_returns_no_matches()
def query_with_filter_on_unknown_field_returns_no_matches(): print(f"\n--- Vector Store {i} Advanced Searches ---") # Similarity search with a filter print("\nSimilarity search results with filter:") filters = MetadataFilters( filters=[ExactMatchFilter(key="unknown_field", value="c")] ) query = VectorStoreQuery( query_embedding=[1.0, 1.0], filters=filters ) result = vs.query(query) print(result.ids)

query_with_filter_on_unknown_field_returns_no_matches()
def delete_removes_document_from_query_results(): vs.delete("test-1") query = VectorStoreQuery( query_embedding=[1.0, 1.0], similarity_top_k=2 ) result = vs.query(query) print(result.ids)

delete_removes_document_from_query_results()
conduct_advanced_searches(vector_store_list) ```
### End to End Demo
Please refer to our complete demo guide Oracle AI Vector Search End-to-End Demo Guide [15] to build an end to end RAG pipeline with the help of Oracle AI Vector Search.

[1] https://www.oracle.com/database/technologies/partitioning.html
[2] https://www.oracle.com/database/real-application-clusters/
[3] https://www.oracle.com/database/technologies/exadata/software/smartscan/
[4] https://www.oracle.com/database/distributed-database/
[5] https://docs.oracle.com/en/database/oracle/oracle-database/23/cncpt/transactions.html
[6] https://docs.oracle.com/en/database/oracle/oracle-database/21/vldbg/parallel-exec-intro.html#GUID-D28717E4-0F77-44F5-BB4E-234C31D4E4BA
[7] https://www.oracle.com/database/data-guard/
[8] https://www.oracle.com/security/database-security/
[9] https://www.oracle.com/artificial-intelligence/database-machine-learning/
[10] https://www.oracle.com/database/integrated-graph-database/
[11] https://www.oracle.com/database/spatial/
[12] https://docs.oracle.com/en/database/oracle/oracle-database/23/arpls/dbms_blockchain_table.html#GUID-B469E277-978E-4378-A8C1-26D3FF96C9A6
[13] https://docs.oracle.com/en/database/oracle/oracle-database/23/adjsn/json-in-oracle-database.html
[14] https://www.oracle.com/database/free/#resources
[15] https://github.com/run-llama/llama_index/blob/main/docs/examples/cookbooks/oracleai_demo.ipynb
[16] https://docs.oracle.com/en/database/oracle/oracle-database/19/admqs/administering-user-accounts-and- security.html#GUID-36B21D72-1BBB-46C9-A0C9-F0D2A8591B8D
[17] https://python-oracledb.readthedocs.io/en/latest/user_guide/appendix_a.html#featuresummary
[18] https://docs.oracle.com/en/database/oracle/oracle-database/23/vecse/manage-different-categories- vector-indexes.html
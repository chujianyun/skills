# developers.llamaindex.ai/python/framework/integrations/vector_stores/db2llamavs/index.md
> https://developers.llamaindex.ai/python/framework/integrations/vector_stores/db2llamavs/index.md

--- title: IBM Db2 Vector Store and Vector Search | Developer Documentation ---

LlamaIndex’s Db2 integration (llama-index-vector-stores-db2) provides vector store and vector search capabilities for working with IBM relational database Db2 version v12.1.2 and above, distributed under the MIT license. Users can use the provided implementations as-is or customize them for specific needs. Key features include:

- Vector storage with metadata - Vector similarity search and filtering options - Support for EUCLIDEAN\_DISTANCE, DOT\_PRODUCT, COSINE, MANHATTAN\_DISTANCE, HAMMING\_DISTANCE, and EUCLIDEAN\_SQUARED distance metrics - Performance optimization by index creation and Approximate nearest neighbors search. (Will be added soon)

### Prerequisites for using LlamaIndex with Db2 Vector Store and Search
Install package `llama-index-vector-stores-db2` which is the integration package for the db2 LlamaIndex Vector Store and Search.
``` # pip install llama-index-vector-stores-db2 ```
### Connect to Db2 Vector Store

The following sample code will show how to connect to Db2 Database. Besides the dependencies above, you will need a Db2 database instance (with version v12.1.2+, which has the vector datatype support) running.

``` import ibm_db import ibm_db_dbi
database = "" username = "" password = ""
try: connection = ibm_db_dbi.connect(database, username, password) print("Connection successful!") except Exception as e: print("Connection failed!", e) ```
### Import the required dependencies
``` from llama_index.core.schema import NodeRelationship, RelatedNodeInfo, TextNode from llama_index.core.vector_stores.types import ( ExactMatchFilter, MetadataFilters, VectorStoreQuery, )

from llama_index.vector_stores.db2 import base as db2llamavs from llama_index.vector_stores.db2 import DB2LlamaVS, DistanceStrategy ```
### Load Documents

``` # Define a list of documents (These dummy examples are 4 random documents ) text_json_list = [ { "text": "Db2 handles LOB data differently than other kinds of data. As a result, you sometimes need to take additional actions when you define LOB columns and insert the LOB data.", "id_": "doc_1_2_P4", "embedding": [1.0, 0.0], "relationships": "test-0", "metadata": { "weight": 1.0, "rank": "a", "url": "https://www.ibm.com/docs/en/db2-for-zos/12?topic=programs-storing-lob-data-in-tables", }, }, { "text": "Introduced in Db2 13, SQL Data Insights brought artificial intelligence (AI) functionality to the Db2 for z/OS engine. It provided the capability to run SQL AI query to find valuable insights hidden in your Db2 data and help you make better business decisions.", "id_": "doc_15.5.1_P1", "embedding": [0.0, 1.0], "relationships": "test-1", "metadata": { "weight": 2.0, "rank": "c", "url": "https://community.ibm.com/community/user/datamanagement/blogs/neena-cherian/2023/03/07/accelerating-db2-ai-queries-with-the-new-vector-pr", }, }, { "text": "Data structures are elements that are required to use DB2®. You can access and use these elements to organize your data. Examples of data structures include tables, table spaces, indexes, index spaces, keys, views, and databases.",

"id_": "id_22.3.4.3.1_P2", "embedding": [1.0, 1.0], "relationships": "test-2", "metadata": { "weight": 3.0, "rank": "d", "url": "https://www.ibm.com/docs/en/zos-basic-skills?topic=concepts-db2-data-structures", }, }, { "text": "DB2® maintains a set of tables that contain information about the data that DB2 controls. These tables are collectively known as the catalog. The catalog tables contain information about DB2 objects such as tables, views, and indexes. When you create, alter, or drop an object, DB2 inserts, updates, or deletes rows of the catalog that describe the object.", "id_": "id_3.4.3.1_P3", "embedding": [2.0, 1.0], "relationships": "test-3", "metadata": { "weight": 4.0, "rank": "e", "url": "https://www.ibm.com/docs/en/zos-basic-skills?topic=objects-db2-catalog", }, }, ] ```

``` # Create Llama Text Nodes text_nodes = [] for text_json in text_json_list: # Construct the relationships using RelatedNodeInfo relationships = { NodeRelationship.SOURCE: RelatedNodeInfo( node_id=text_json["relationships"] ) }

# Prepare the metadata dictionary; you might want to exclude certain metadata fields if necessary metadata = { "weight": text_json["metadata"]["weight"], "rank": text_json["metadata"]["rank"], }

# Create a TextNode instance text_node = TextNode( text=text_json["text"], id_=text_json["id_"], embedding=text_json["embedding"], relationships=relationships, metadata=metadata, )

text_nodes.append(text_node) print(text_nodes) ```
### Using AI Vector Search Create a bunch of Vector Stores with different distance strategies
First we will create three vector stores each with different distance functions.
You can manually connect to the Db2 Database and will see three tables Documents\_DOT, Documents\_COSINE and Documents\_EUCLIDEAN.
``` # Ingest documents into Db2 Vector Store using different distance strategies vector_store_dot = DB2LlamaVS.from_documents( text_nodes, table_name="Documents_DOT", client=connection, distance_strategy=DistanceStrategy.DOT_PRODUCT, embed_dim=2, ) vector_store_max = DB2LlamaVS.from_documents( text_nodes, table_name="Documents_COSINE", client=connection, distance_strategy=DistanceStrategy.COSINE, embed_dim=2, ) vector_store_euclidean = DB2LlamaVS.from_documents( text_nodes, table_name="Documents_EUCLIDEAN", client=connection, distance_strategy=DistanceStrategy.EUCLIDEAN_DISTANCE, embed_dim=2, ) ```

### Demonstrating add, delete operations for texts, and basic similarity search
``` def manage_texts(vector_stores): for i, vs in enumerate(vector_stores, start=1): # Adding texts try: vs.add_texts(text_nodes, metadata) print(f"\n\n\nAdd texts complete for vector store {i}\n\n\n") except Exception as ex: print( f"\n\n\nExpected error on duplicate add for vector store {i}\n\n\n" )

# Deleting texts using the value of 'doc_id' vs.delete("test-1") print(f"\n\n\nDelete texts complete for vector store {i}\n\n\n")
# Similarity search query = VectorStoreQuery( query_embedding=[1.0, 1.0], similarity_top_k=3 ) results = vs.query(query=query) print( f"\n\n\nSimilarity search results for vector store {i}: {results}\n\n\n" )

vector_store_list = [ vector_store_dot, vector_store_max, vector_store_euclidean, ] manage_texts(vector_store_list) ```

### Now we will conduct a bunch of advanced searches on all 3 vector stores.
``` def conduct_advanced_searches(vector_stores): for i, vs in enumerate(vector_stores, start=1):
def query_without_filters_returns_all_rows_sorted_by_similarity(): print(f"\n--- Vector Store {i} Advanced Searches ---") # Similarity search without a filter print("\nSimilarity search results without filter:") query = VectorStoreQuery( query_embedding=[1.0, 1.0], similarity_top_k=3 ) print(vs.query(query=query))

query_without_filters_returns_all_rows_sorted_by_similarity()
def query_with_filters_returns_multiple_matches(): print(f"\n--- Vector Store {i} Advanced Searches ---") # Similarity search with filter print("\nSimilarity search results with filter:") filters = MetadataFilters( filters=[ExactMatchFilter(key="rank", value="c")] ) query = VectorStoreQuery( query_embedding=[1.0, 1.0], filters=filters, similarity_top_k=3 ) result = vs.query(query) print(result.ids)

query_with_filters_returns_multiple_matches()
def query_with_filter_applies_top_k(): print(f"\n--- Vector Store {i} Advanced Searches ---") # Similarity search with a filter print("\nSimilarity search results with top k filter:") filters = MetadataFilters( filters=[ExactMatchFilter(key="rank", value="c")] ) query = VectorStoreQuery( query_embedding=[1.0, 1.0], filters=filters, similarity_top_k=1 ) result = vs.query(query) print(result.ids)

query_with_filter_applies_top_k()
def query_with_filter_applies_node_id_filter(): print(f"\n--- Vector Store {i} Advanced Searches ---") # Similarity search with a filter print("\nSimilarity search results with node_id filter:") filters = MetadataFilters( filters=[ExactMatchFilter(key="rank", value="c")] ) query = VectorStoreQuery( query_embedding=[1.0, 1.0], filters=filters, similarity_top_k=3, node_ids=["452D24AB-F185-414C-A352-590B4B9EE51B"], ) result = vs.query(query) print(result.ids)

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
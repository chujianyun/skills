# developers.llamaindex.ai/python/framework/integrations/vector_stores/tablestoredemo/index.md
> https://developers.llamaindex.ai/python/framework/integrations/vector_stores/tablestoredemo/index.md

--- title: TablestoreVectorStore | Developer Documentation ---

> Tablestore [1] is a fully managed NoSQL cloud database service that enables storage of a massive amount of structured and semi-structured data.
This notebook shows how to use functionality related to the `Tablestore` vector database.
To use Tablestore, you must create an instance. Here are the creating instance instructions [2].
## Install
``` %pip install llama-index-vector-stores-tablestore ```
``` import getpass import os

os.environ["end_point"] = getpass.getpass("Tablestore end_point:") os.environ["instance_name"] = getpass.getpass("Tablestore instance_name:") os.environ["access_key_id"] = getpass.getpass("Tablestore access_key_id:") os.environ["access_key_secret"] = getpass.getpass( "Tablestore access_key_secret:"<SECRET>"end_point"), instance_name=os.getenv("instance_name"), access_key_id=os.getenv("access_key_id"), access_key_secret=os.getenv("access_key_secret"), vector_dimension=vector_dimension, vector_metric_type=VectorMetricType.VM_COSINE, # optional: custom metadata mapping is used to filter non-vector fields. metadata_mappings=[ FieldSchema( "type", FieldType.KEYWORD, index=True, enable_sort_and_agg=True ), FieldSchema( "time", FieldType.LONG, index=True, enable_sort_and_agg=True ), ], ) ```

Create table and index.
``` store.create_table_if_not_exist() store.create_search_index_if_not_exist() ```

New a mock embedding for test.
``` embedder = MockEmbedding(vector_dimension) ```
Prepare some docs.
``` texts = [ TextNode( id_="1", text="The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption.", metadata={"type": "a", "time": 1995}, ), TextNode( id_="2", text="When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.", metadata={"type": "a", "time": 1990}, ), TextNode( id_="3", text="An insomniac office worker and a devil-may-care soapmaker form an underground fight club that evolves into something much, much more.", metadata={"type": "a", "time": 2009}, ), TextNode( id_="4", text="A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into thed of a C.E.O.",

metadata={"type": "a", "time": 2023}, ), TextNode( id_="5", text="A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.", metadata={"type": "b", "time": 2018}, ), TextNode( id_="6", text="Two detectives, a rookie and a veteran, hunt a serial killer who uses the seven deadly sins as his motives.", metadata={"type": "c", "time": 2010}, ), TextNode( id_="7", text="An organized crime dynasty's aging patriarch transfers control of his clandestine empire to his reluctant son.", metadata={"type": "a", "time": 2023}, ), ] for t in texts: t.embedding = embedder.get_text_embedding(t.text) ```

Write some docs.
``` store.add(texts) ```
``` ['1', '2', '3', '4', '5', '6', '7'] ```
Delete docs.
``` store.delete("1") ```
Query with filters.
``` store.query( query=VectorStoreQuery( query_embedding=embedder.get_text_embedding("nature fight physical"), similarity_top_k=5, filters=MetadataFilters( filters=[ MetadataFilter( key="type", value="a", operator=FilterOperator.EQ ), MetadataFilter( key="time", value=2020, operator=FilterOperator.LTE ), ], condition=FilterCondition.AND, ), ), ) ```

``` VectorStoreQueryResult(nodes=[TextNode(id_='1', embedding=[0.5, 0.5, 0.5, 0.5], metadata={'time': 1995, 'type': 'a'}, excluded_embed_metadata_keys=[], excluded_llm_metadata_keys=[], relationships={}, metadata_template='{key}: {value}', metadata_separator='\n', text='The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption.', mimetype='text/plain', start_char_idx=None, end_char_idx=None, metadata_seperator='\n', text_template='{metadata_str}\n\n{content}'), TextNode(id_='2', embedding=[0.5, 0.5, 0.5, 0.5], metadata={'time': 1990, 'type': 'a'}, excluded_embed_metadata_keys=[], excluded_llm_metadata_keys=[], relationships={}, metadata_template='{key}: {value}', metadata_separator='\n', text='When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.', mimetype='text/plain', start_char_idx=None, end_char_idx=None, metadata_seperator='\n', text_template='{metadata_str}\n\n{content}'), TextNode(id_='3', embedding=[0.5, 0.5, 0.5, 0.5], metadata={'time': 2009, 'type': 'a'}, excluded_embed_metadata_keys=[], excluded_llm_metadata_keys=[], relationships={}, metadata_template='{key}: {value}', metadata_separator='\n', text='An insomniac office worker and a devil-may-care soapmaker form an underground fight club that evolves into something much, much more.', mimetype='text/plain', start_char_idx=None, end_char_idx=None, metadata_seperator='\n', text_template='{metadata_str}\n\n{content}')], similarities=[1.0, 1.0, 1.0], ids=['1', '2', '3'])

Full text search: query mode = TEXT.
``` query_result = store.query( query=VectorStoreQuery( mode=VectorStoreQueryMode.TEXT_SEARCH, query_str="computer", similarity_top_k=5, ), ) print(query_result) ```

``` VectorStoreQueryResult(nodes=[TextNode(id_='5', embedding=[0.5, 0.5, 0.5, 0.5], metadata={'time': 2018, 'type': 'b'}, excluded_embed_metadata_keys=[], excluded_llm_metadata_keys=[], relationships={}, metadata_template='{key}: {value}', metadata_separator='\n', text='A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.', mimetype='text/plain', start_char_idx=None, end_char_idx=None, metadata_seperator='\n', text_template='{metadata_str}\n\n{content}')], similarities=[2.673976421356201], ids=['5'])

HYBRID query.
``` query_result = store.query( query=VectorStoreQuery( mode=VectorStoreQueryMode.HYBRID, query_embedding=embedder.get_text_embedding("nature fight physical"), query_str="python", similarity_top_k=5, ), ) print(query_result) ```

``` VectorStoreQueryResult(nodes=[TextNode(id_='1', embedding=[0.5, 0.5, 0.5, 0.5], metadata={'time': 1995, 'type': 'a'}, excluded_embed_metadata_keys=[], excluded_llm_metadata_keys=[], relationships={}, metadata_template='{key}: {value}', metadata_separator='\n', text='The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption.', mimetype='text/plain', start_char_idx=None, end_char_idx=None, metadata_seperator='\n', text_template='{metadata_str}\n\n{content}'), TextNode(id_='2', embedding=[0.5, 0.5, 0.5, 0.5], metadata={'time': 1990, 'type': 'a'}, excluded_embed_metadata_keys=[], excluded_llm_metadata_keys=[], relationships={}, metadata_template='{key}: {value}', metadata_separator='\n', text='When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.', mimetype='text/plain', start_char_idx=None, end_char_idx=None, metadata_seperator='\n', text_template='{metadata_str}\n\n{content}'), TextNode(id_='3', embedding=[0.5, 0.5, 0.5, 0.5], metadata={'time': 2009, 'type': 'a'}, excluded_embed_metadata_keys=[], excluded_llm_metadata_keys=[], relationships={}, metadata_template='{key}: {value}', metadata_separator='\n', text='An insomniac office worker and a devil-may-care soapmaker form an underground fight club that evolves into something much, much more.', mimetype='text/plain', start_char_idx=None, end_char_idx=None, metadata_seperator='\n', text_template='{metadata_str}\n\n{content}'), TextNode(id_='4', embedding=[0.5, 0.5, 0.5, 0.5], metadata={'time': 2023, 'type': 'a'}, excluded_embed_metadata_keys=[], excluded_llm_metadata_keys=[], relationships={}, metadata_template='{key}: {value}', metadata_separator='\n', text='A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into thed of a C.E.O.', mimetype='text/plain', start_char_idx=None, end_char_idx=None, metadata_seperator='\n', text_template='{metadata_str}\n\n{content}'), TextNode(id_='5', embedding=[0.5, 0.5, 0.5, 0.5], metadata={'time': 2018, 'type': 'b'}, excluded_embed_metadata_keys=[], excluded_llm_metadata_keys=[], relationships={}, metadata_template='{key}: {value}', metadata_separator='\n', text='A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.', mimetype='text/plain', start_char_idx=None, end_char_idx=None, metadata_seperator='\n', text_template='{metadata_str}\n\n{content}')], similarities=[1.0, 1.0, 1.0, 1.0, 1.0], ids=['1', '2', '3', '4', '5'])

```

[1] https://www.aliyun.com/product/ots
[2] https://help.aliyun.com/zh/tablestore/getting-started/manage-the-wide-column-model-in-the-tablestore-console
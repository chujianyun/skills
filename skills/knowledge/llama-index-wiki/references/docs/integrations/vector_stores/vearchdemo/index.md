# developers.llamaindex.ai/python/framework/integrations/vector_stores/vearchdemo/index.md
> https://developers.llamaindex.ai/python/framework/integrations/vector_stores/vearchdemo/index.md

--- title: load documents | Developer Documentation ---

documents = SimpleDirectoryReader(”./data/paul\_graham/“).load\_data() print(“Document ID:”, len(documents), documents\[0].doc\_id)
```` Document ID: 1 8d84aefd-ca73-4c1e-b83d-141c1b1b3ba6

```python from llama_index import ServiceContext from llama_index.embeddings import HuggingFaceEmbedding from llama_index.vector_stores import VearchVectorStore
""" vearch cluster """ vector_store = VearchVectorStore( path_or_url="http://liama-index-router.vectorbase.svc.sq01.n.jd.local", table_name="liama_index_test2", db_name="liama_index", flag=1, )

""" vearch standalone """ # vector_store = VearchVectorStore( # path_or_url = '/data/zhx/zhx/liama_index/knowledge_base/liama_index_teststandalone', # # path_or_url = 'http://liama-index-router.vectorbase.svc.sq01.n.jd.local', # table_name = 'liama_index_teststandalone', # db_name = 'liama_index', # flag = 0)

embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5") service_context = ServiceContext.from_defaults(embed_model=embed_model) storage_context = StorageContext.from_defaults(vector_store=vector_store) index = VectorStoreIndex.from_documents( documents, storage_context=storage_context, service_context=service_context ) ````
``` Loading checkpoint shards: 0%| | 0/7 [00:00<?, ?it/s] ```
``` query_engine = index.as_query_engine() response = query_engine.query("What did the author do growing up?") display(Markdown(f"<b>{response}</b>")) ```
**The author did not provide any information about their growing up.**
``` query_engine = index.as_query_engine() response = query_engine.query( "What did the author do after his time at Y Combinator?" ) display(Markdown(f"<b>{response}</b>")) ```

**The author wrote all of Y Combinator’s internal software in Arc while continuing to work on Y Combinator, but later stopped working on Arc and focused on writing essays and working on Y Combinator. In 2012, the author’s mother had a stroke, and the author realized that Y Combinator was taking up too much of their time and decided to hand it over to someone else. The author suggested this to Robert Morris, who offered unsolicited advice to the author to make sure Y Combinator wasn’t the last cool thing the author did. The author ultimately decided to hand over the leadership of Y Combinator to Sam Altman in 2013.**
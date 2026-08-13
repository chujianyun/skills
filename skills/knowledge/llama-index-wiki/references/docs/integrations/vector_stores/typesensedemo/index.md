# developers.llamaindex.ai/python/framework/integrations/vector_stores/typesensedemo/index.md
> https://developers.llamaindex.ai/python/framework/integrations/vector_stores/typesensedemo/index.md

--- title: Typesense Vector Store | Developer Documentation ---
#### Download Data
``` %pip install llama-index-embeddings-openai %pip install llama-index-vector-stores-typesense ```
``` !mkdir -p 'data/paul_graham/' !wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt' ```
#### Load documents, build the VectorStoreIndex
``` # import logging # import sys
# logging.basicConfig(stream=sys.stdout, level=logging.INFO) # logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))
from llama_index.core import ( VectorStoreIndex, SimpleDirectoryReader, StorageContext, ) from IPython.display import Markdown, display ```
``` # load documents documents = SimpleDirectoryReader("./data/paul_graham/").load_data() ```
``` from llama_index.vector_stores.typesense import TypesenseVectorStore from typesense import Client
typesense_client = Client( { "api_key": "xyz", "nodes": [{"host": "localhost", "port": "8108", "protocol": "http"}], "connection_timeout_seconds": 2, } ) typesense_vector_store = TypesenseVectorStore(typesense_client) storage_context = StorageContext.from_defaults( vector_store=typesense_vector_store )

index = VectorStoreIndex.from_documents( documents, storage_context=storage_context ) ```
#### Query Index
``` from llama_index.core import QueryBundle from llama_index.embeddings.openai import OpenAIEmbedding
# By default, typesense vector store uses vector search. You need to provide the embedding yourself. query_str = "What did the author do growing up?" embed_model = OpenAIEmbedding() # You can also get the settings from the Settings object from llama_index.core import Settings
# embed_model = Settings.embed_model query_embedding = embed_model.get_agg_embedding_from_queries(query_str) query_bundle = QueryBundle(query_str, embedding=query_embedding) response = index.as_query_engine().query(query_bundle)
display(Markdown(f"<b>{response}</b>")) ```
**The author grew up skipping a step in the evolution of computers, learning Italian, walking through Florence, painting people, working with technology companies, seeking signature styles at RISD, living in a rent- stabilized apartment, launching software, editing code (including Lisp expressions), writing essays, publishing them online, and receiving feedback from angry readers. He also experienced the exponential growth of commodity processors in the 1990s, which rolled up high-end, special-purpose hardware and software companies. He also learned how to make a little Italian go a long way by stringing together abstract concepts with a few simple verbs. He also experienced the tight coupling of money and coolness in the art world, and the fact that anything expensive comes to be seen as cool, and anything seen as cool will soon become equally expensive. He also experienced the challenge of launching software, as he had to recruit an initial set of users and make sure they had decent-looking stores before launching publicly. He also experienced the first instance of what is now a familiar experience, when he read the comments and found they were full of angry people. He also experienced the difference between putting something online and publishing it online. Finally, he wrote essays about topics he had stacked up, and wrote a more detailed version for others to read.**
``` from llama_index.core.vector_stores.types import VectorStoreQueryMode
# You can also use text search
query_bundle = QueryBundle(query_str=query_str) response = index.as_query_engine( vector_store_query_mode=VectorStoreQueryMode.TEXT_SEARCH ).query(query_bundle) display(Markdown(f"<b>{response}</b>")) ```
****
**The author grew up during the Internet Bubble and was running a startup. They had to hire more people than they wanted to in order to seem more professional and were at the mercy of their investors until Yahoo bought them. They learned a lot about retail and startups, and had to do a lot of things that they weren’t necessarily good at in order to make their business successful.**
# developers.llamaindex.ai/python/framework/integrations/vector_stores/neo4jvectordemo/index.md
> https://developers.llamaindex.ai/python/framework/integrations/vector_stores/neo4jvectordemo/index.md

--- title: Neo4j vector store | Developer Documentation ---
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.
``` %pip install llama-index-vector-stores-neo4jvector ```
``` !pip install llama-index ```
``` import os import openai
os.environ["OPENAI_API_KEY"] = "OPENAI_API_KEY" openai.api_key = os.environ["OPENAI_API_KEY"] ```
## Initiate Neo4j vector wrapper
``` from llama_index.vector_stores.neo4jvector import Neo4jVectorStore
username = "neo4j" password = "pleaseletmein" url = "bolt://localhost:7687" embed_dim = 1536
neo4j_vector = Neo4jVectorStore(username, password, url, embed_dim) ```
## Load documents, build the VectorStoreIndex
``` from llama_index.core import VectorStoreIndex, SimpleDirectoryReader from IPython.display import Markdown, display ```
Download Data

``` !mkdir -p 'data/paul_graham/' !wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt' ```

``` --2023-12-14 18:44:00-- https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt Resolving raw.githubusercontent.com (raw.githubusercontent.com)... 185.199.111.133, 185.199.109.133, 185.199.110.133, ... Connecting to raw.githubusercontent.com (raw.githubusercontent.com)|185.199.111.133|:443... connected. HTTP request sent, awaiting response... 200 OK Length: 75042 (73K) [text/plain] Saving to: ‘data/paul_graham/paul_graham_essay.txt’

data/paul_graham/pa 100%[===================>] 73,28K --.-KB/s in 0,03s
2023-12-14 18:44:00 (2,16 MB/s) - ‘data/paul_graham/paul_graham_essay.txt’ saved [75042/75042] ```
``` # load documents documents = SimpleDirectoryReader("./data/paul_graham").load_data() ```
``` from llama_index.core import StorageContext
storage_context = StorageContext.from_defaults(vector_store=neo4j_vector) index = VectorStoreIndex.from_documents( documents, storage_context=storage_context ) ```
``` query_engine = index.as_query_engine() response = query_engine.query("What happened at interleaf?") display(Markdown(f"<b>{response}</b>")) ```

**At Interleaf, they added a scripting language inspired by Emacs and made it a dialect of Lisp. They were looking for a Lisp hacker to write things in this scripting language. The author of the text worked at Interleaf and mentioned that their Lisp was the thinnest icing on a giant C cake. The author also mentioned that they didn’t know C and didn’t want to learn it, so they never understood most of the software at Interleaf. Additionally, the author admitted to being a bad employee and spending much of their time working on a separate project called On Lisp.**

## Hybrid search
Hybrid search uses a combination of keyword and vector search In order to use hybrid search, you need to set the `hybrid_search` to `True`
``` neo4j_vector_hybrid = Neo4jVectorStore( username, password, url, embed_dim, hybrid_search=True ) ```

``` storage_context = StorageContext.from_defaults( vector_store=neo4j_vector_hybrid ) index = VectorStoreIndex.from_documents( documents, storage_context=storage_context ) query_engine = index.as_query_engine() response = query_engine.query("What happened at interleaf?") display(Markdown(f"<b>{response}</b>")) ```

**At Interleaf, they added a scripting language inspired by Emacs and made it a dialect of Lisp. They were looking for a Lisp hacker to write things in this scripting language. The author of the essay worked at Interleaf but didn’t understand most of the software because he didn’t know C and didn’t want to learn it. He also mentioned that their Lisp was the thinnest icing on a giant C cake. The author admits to being a bad employee and spending much of his time working on a contract to publish On Lisp.**

## Load existing vector index
In order to connect to an existing vector index, you need to define the `index_name` and `text_node_property` parameters:
- index\_name: name of the existing vector index (default is `vector`) - text\_node\_property: name of the property that containt the text value (default is `text`)
``` index_name = "existing_index" text_node_property = "text" existing_vector = Neo4jVectorStore( username, password, url, embed_dim, index_name=index_name, text_node_property=text_node_property, )

loaded_index = VectorStoreIndex.from_vector_store(existing_vector) ```
## Customizing responses
You can customize the retrieved information from the knowledge graph using the `retrieval_query` parameter.
The retrieval query must return the following four columns:
- text:str - The text of the returned document - score:str - similarity score - id:str - node id - metadata: Dict - dictionary with additional metadata (must contain `_node_type` and `_node_content` keys)

``` retrieval_query = ( "RETURN 'Interleaf hired Tomaz' AS text, score, node.id AS id, " "{author: 'Tomaz', _node_type:node._node_type, _node_content:node._node_content} AS metadata" ) neo4j_vector_retrieval = Neo4jVectorStore( username, password, url, embed_dim, retrieval_query=retrieval_query ) ```

``` loaded_index = VectorStoreIndex.from_vector_store( neo 4j_vector_retrieval ).as_query_engine() response = loaded_index.query("What happened at interleaf?") display(Markdown(f"<b>{response}</b>")) ```

**Interleaf hired Tomaz.**
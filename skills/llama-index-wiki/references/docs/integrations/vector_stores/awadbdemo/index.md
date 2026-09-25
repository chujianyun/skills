# developers.llamaindex.ai/python/framework/integrations/vector_stores/awadbdemo/index.md
> https://developers.llamaindex.ai/python/framework/integrations/vector_stores/awadbdemo/index.md

--- title: Awadb Vector Store | Developer Documentation ---

If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.
``` %pip install llama-index-embeddings-huggingface %pip install llama-index-vector-stores-awadb ```

``` !pip install llama-index ```
## Creating an Awadb index
``` import logging import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO) logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout)) ```
#### Load documents, build the VectorStoreIndex
``` from llama_index.core import ( SimpleDirectoryReader, VectorStoreIndex, StorageContext, ) from IPython.display import Markdown, display import openai

openai.api_key = "" ```
``` INFO:numexpr.utils:Note: NumExpr detected 12 cores but "NUMEXPR_MAX_THREADS" not set, so enforcing safe limit of 8. Note: NumExpr detected 12 cores but "NUMEXPR_MAX_THREADS" not set, so enforcing safe limit of 8. INFO:numexpr.utils:NumExpr defaulting to 8 threads. NumExpr defaulting to 8 threads. ```

#### Download Data
``` !mkdir -p 'data/paul_graham/' !wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt' ```

#### Load Data
``` # load documents documents = SimpleDirectoryReader("./data/paul_graham/").load_data() ```

``` from llama_index.embeddings.huggingface import HuggingFaceEmbedding from llama_index.vector_stores.awadb import AwaDBVectorStore

embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
vector_store = AwaDBVectorStore() storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents( documents, storage_context=storage_context, embed_model=embed_model ) ```

#### Query Index
``` # set Logging to DEBUG for more detailed outputs query_engine = index.as_query_engine() response = query_engine.query("What did the author do growing up?") ```

**Growing up, the author wrote short stories, experimented with programming on an IBM 1401, nagged his father to buy a TRS-80 computer, wrote simple games, a program to predict how high his model rockets would fly, and a word processor. He also studied philosophy in college, switched to AI, and worked on building the infrastructure of the web. He wrote essays and published them online, had dinners for a group of friends every Thursday night, painted, and bought a building in Cambridge.**
``` # set Logging to DEBUG for more detailed outputs query_engine = index.as_query_engine() response = query_engine.query( "What did the author do after his time at Y Combinator?" ) ```
``` display(Markdown(f"<b>{response}</b>")) ```
**After his time at Y Combinator, the author wrote essays, worked on Lisp, and painted. He also visited his mother in Oregon and helped her get out of a nursing home.**
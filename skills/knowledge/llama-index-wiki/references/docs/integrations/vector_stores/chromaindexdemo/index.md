# developers.llamaindex.ai/python/framework/integrations/vector_stores/chromaindexdemo/index.md
> https://developers.llamaindex.ai/python/framework/integrations/vector_stores/chromaindexdemo/index.md

--- title: Chroma | Developer Documentation ---

> Chroma [1] is a AI-native open-source vector database focused on developer productivity and happiness. Chroma is licensed under Apache 2.0.
![Discord][5]  [2] ![License](<https://img.shields.io/static/v1?label=license\&message=Apache 2.0\&color=white>)  [3] [4]
- Website [6] - Documentation [7] - Twitter [8] - Discord [2]

Chroma is fully-typed, fully-tested and fully-documented.
Install Chroma with:
Terminal window
``` pip install chromadb ```
Chroma runs in various modes. See below for examples of each integrated with LlamaIndex.
- `in-memory` - in a python script or jupyter notebook - `in-memory with persistence` - in a script or notebook and save/load to disk - `in a docker container` - as a server running your local machine or in the cloud
Like any other database, you can:
- `.add` - `.get` - `.update` - `.upsert` - `.delete` - `.peek` - and `.query` runs the similarity search.

View full docs at docs [9].
## Basic Example
In this basic example, we take the Paul Graham essay, split it into chunks, embed it using an open-source embedding model, load it into Chroma, and then query it.
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.
``` %pip install llama-index-vector-stores-chroma %pip install llama-index-embeddings-huggingface ```

``` !pip install llama-index ```
#### Creating a Chroma Index
``` # !pip install llama-index chromadb --quiet # !pip install chromadb # !pip install sentence-transformers # !pip install pydantic==1.10.11 ```

``` # import from llama_index.core import VectorStoreIndex, SimpleDirectoryReader from llama_index.vector_stores.chroma import ChromaVectorStore from llama_index.core import StorageContext from llama_index.embeddings.huggingface import HuggingFaceEmbedding from IPython.display import Markdown, display import chromadb ```

``` # set up OpenAI import os import getpass

os.environ["OPENAI_API_KEY"] = getpass.getpass("OpenAI API Key:") import openai
openai.api_key = os.environ["OPENAI_API_KEY"] ```
Download Data
``` !mkdir -p 'data/paul_graham/' !wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt' ```

``` # create client and a new collection chroma_client = chromadb.EphemeralClient() chroma_collection = chroma_client.create_collection("quickstart")

# define embedding function embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")
# load documents documents = SimpleDirectoryReader("./data/paul_graham/").load_data()
# set up ChromaVectorStore and load in data vector_store = ChromaVectorStore(chroma_collection=chroma_collection) storage_context = StorageContext.from_defaults(vector_store=vector_store) index = VectorStoreIndex.from_documents( documents, storage_context=storage_context, embed_model=embed_model )

# Query Data query_engine = index.as_query_engine() response = query_engine.query("What did the author do growing up?") display(Markdown(f"<b>{response}</b>")) ```

``` /Users/loganmarkewich/llama_index/llama-index/lib/python3.9/site-packages/tqdm/auto.py:21: TqdmWarning: IProgress not found. Please update jupyter and ipywidgets. See https://ipywidgets.readthedocs.io/en/stable/user_install.html from .autonotebook import tqdm as notebook_tqdm /Users/loganmarkewich/llama_index/llama-index/lib/python3.9/site-packages/bitsandbytes/cextension.py:34: UserWarning: The installed version of bitsandbytes was compiled without GPU support. 8-bit optimizers, 8-bit multiplication, and GPU quantization are unavailable. warn("The installed version of bitsandbytes was compiled without GPU support. "

'NoneType' object has no attribute 'cadam32bit_grad_fp32' ```
**The author worked on writing and programming growing up. They wrote short stories and tried writing programs on an IBM 1401 computer. Later, they got a microcomputer and started programming more extensively.**
## Basic Example (including saving to disk)
Extending the previous example, if you want to save to disk, simply initialize the Chroma client and pass the directory where you want the data to be saved to.
`Caution`: Chroma makes a best-effort to automatically save data to disk, however multiple in-memory clients can stomp each other’s work. As a best practice, only have one client per path running at any given time.
``` # save to disk
db = chromadb.PersistentClient(path="./chroma_db") chroma_collection = db.get_or_create_collection("quickstart") vector_store = ChromaVectorStore(chroma_collection=chroma_collection) storage_context = StorageContext.from_defaults(vector_store=vector_store)

index = VectorStoreIndex.from_documents( documents, storage_context=storage_context, embed_model=embed_model )

# load from disk db2 = chromadb.PersistentClient(path="./chroma_db") chroma_collection = db2.get_or_create_collection("quickstart") vector_store = ChromaVectorStore(chroma_collection=chroma_collection) index = VectorStoreIndex.from_vector_store( vector_store, embed_model=embed_model, )

# Query Data from the persisted index query_engine = index.as_query_engine() response = query_engine.query("What did the author do growing up?") display(Markdown(f"<b>{response}</b>")) ```

**The author worked on writing and programming growing up. They wrote short stories and tried writing programs on an IBM 1401 computer. Later, they got a microcomputer and started programming games and a word processor.**
## Basic Example (using the Docker Container)
You can also run the Chroma Server in a Docker container separately, create a Client to connect to it, and then pass that to LlamaIndex.
Here is how to clone, build, and run the Docker Image:
``` git clone git@github.com:chroma-core/chroma.git docker-compose up -d --build ```

``` # create the chroma client and add our data import chromadb

remote_db = chromadb.HttpClient() chroma_collection = remote_db.get_or_create_collection("quickstart") vector_store = ChromaVectorStore(chroma_collection=chroma_collection) storage_context = StorageContext.from_defaults(vector_store=vector_store)

index = VectorStoreIndex.from_documents( documents, storage_context=storage_context, embed_model=embed_model ) ```

``` # Query Data from the Chroma Docker index query_engine = index.as_query_engine() response = query_engine.query("What did the author do growing up?") display(Markdown(f"<b>{response}</b>")) ```

**Growing up, the author wrote short stories, programmed on an IBM 1401, and wrote programs on a TRS-80 microcomputer. He also took painting classes at Harvard and worked as a de facto studio assistant for a painter. He also tried to start a company to put art galleries online, and wrote software to build online stores.**
## Update and Delete
While building toward a real application, you want to go beyond adding data, and also update and delete data.
Chroma has users provide `ids` to simplify the bookkeeping here. `ids` can be the name of the file, or a combined has like `filename_paragraphNumber`, etc.
Here is a basic example showing how to do various operations:
``` doc_to_update = chroma_collection.get(limit=1) doc_to_update["metadatas"][0] = { **doc_to_update["metadatas"][0], **{"author": "Paul Graham"}, } chroma_collection.update( ids=[doc_to_update["ids"][0]], metadatas=[doc_to_update["metadatas"][0]] ) updated_doc = chroma_collection.get(limit=1) print(updated_doc["metadatas"][0])

# delete the last document print("count before", chroma_collection.count()) chroma_collection.delete(ids=[doc_to_update["ids"][0]]) print("count after", chroma_collection.count()) ```

``` {'_node_content': '{"id_": "be08c8bc-f43e-4a71-ba64-e525921a8319", "embedding": null, "metadata": {}, "excluded_embed_metadata_keys": [], "excluded_llm_metadata_keys": [], "relationships": {"1": {"node_id": "2cbecdbb-0840- 48b2-8151-00119da0995b", "node_type": null, "metadata": {}, "hash": "4c702b4df575421e1d1af4b1fd50511b226e0c9863dbfffeccb8b689b8448f35"}, "3": {"node_id": "6a75604a-fa76-4193-8f52-c72a7b18b154", "node_type": null, "metadata": {}, "hash": "d6c408ee1fbca650fb669214e6f32ffe363b658201d31c204e85a72edb71772f"}}, "hash": "b4d0b960aa09e693f9dc0d50ef46a3d0bf5a8fb3ac9f3e4bcf438e326d17e0d8", "text": "", "start_char_idx": 0, "end_char_idx": 4050, "text_template": "{metadata_str}\\n\\n{content}", "metadata_template": "{key}: {value}", "metadata_seperator": "\\n"}', 'author': 'Paul Graham', 'doc_id': '2cbecdbb-0840-48b2-8151-00119da0995b', 'document_id': '2cbecdbb-0840-48b2-8151-00119da0995b', 'ref_doc_id': '2cbecdbb-0840-48b2-8151-00119da0995b'}

count before 20 count after 19 ```

[1] https://docs.trychroma.com/getting-started
[2] https://discord.gg/MMeYNTmh3x
[3] https://github.com/chroma- core/chroma/blob/master/LICENSE
[4] https://github.com/chroma-core/chroma/actions/workflows/chroma-integration-test.yml/badge.svg?branch=main
[5] https://img.shields.io/discord/1073293645303795742
[6] https://www.trychroma.com/
[7] https://docs.trychroma.com/
[8] https://twitter.com/trychroma
[9] https://docs.trychroma.com/reference
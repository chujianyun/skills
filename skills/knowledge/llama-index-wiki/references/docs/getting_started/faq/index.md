# developers.llamaindex.ai/python/framework/getting_started/faq/index.md
> https://developers.llamaindex.ai/python/framework/getting_started/faq/index.md

--- title: Frequently Asked Questions (FAQ) | Developer Documentation ---
Tip
If you haven’t already, install LlamaIndex and complete the starter tutorial. If you run into terms you don’t recognize, check out the high-level concepts.
In this section, we start with the code you wrote for the starter example and show you the most common ways you might want to customize it for your use case:

documents = SimpleDirectoryReader("data").load_data() index = VectorStoreIndex.from_documents(documents) query_engine = index.as_query_engine() response = query_engine.query("What did the author do growing up?") print(response) ```

## **“I want to parse my documents into smaller chunks"**
``` # Global settings from llama_index.core import Settings
Settings.chunk_size = 512
# Local settings from llama_index.core.node_parser import SentenceSplitter
index = VectorStoreIndex.from_documents( documents, transformations=[SentenceSplitter(chunk_size=512)] ) ```

## **"I want to use a different vector store”**
First, you can install the vector store you want to use. For example, to use Chroma as the vector store, you can install it using pip:
Terminal window
``` pip install llama-index-vector-stores-chroma ```
To learn more about all integrations available, check out LlamaHub [1].
Then, you can use it in your code:
``` import chromadb from llama_index.vector_stores.chroma import ChromaVectorStore from llama_index.core import StorageContext

chroma_client = chromadb.PersistentClient() chroma_collection = chroma_client.create_collection("quickstart") vector_store = ChromaVectorStore(chroma_collection=chroma_collection) storage_context = StorageContext.from_defaults(vector_store=vector_store) ```

`StorageContext` defines the storage backend for where the documents, embeddings, and indexes are stored. You can learn more about storage and [how to customize it] (/python/framework/module_guides/storing/customization/index.md).

documents = SimpleDirectoryReader("data").load_data() index = VectorStoreIndex.from_documents( documents, storage_context=storage_context ) query_engine = index.as_query_engine() response = query_engine.query("What did the author do growing up?") print(response) ```

## **”I want to retrieve more context when I query”**

documents = SimpleDirectoryReader("data").load_data() index = VectorStoreIndex.from_documents(documents) query_engine = index.as_query_engine(similarity_top_k=5) response = query_engine.query("What did the author do growing up?") print(response) ```
`as_query_engine` builds a default `retriever` and `query engine` on top of the index. You can configure the retriever and query engine by passing in keyword arguments. Here, we configure the retriever to return the top 5 most similar documents (instead of the default of 2). You can learn more about retrievers and [query engines] (/python/framework/module_guides/querying/retriever/index.md).

## **”I want to use a different LLM”**
``` # Global settings from llama_index.core import Settings from llama_index.llms.ollama import Ollama
Settings.llm = Ollama( model="mistral", request_timeout=60.0, # Manually set the context window to limit memory usage context_window=8000, )
# Local settings index.as_query_engine( llm=Ollama( model="mistral", request_timeout=60.0, # Manually set the context window to limit memory usage context_window=8000, ) ) ```
You can learn more about customizing LLMs.

## **”I want to use a different response mode”**

documents = SimpleDirectoryReader("data").load_data() index = VectorStoreIndex.from_documents(documents) query_engine = index.as_query_engine(response_mode="tree_summarize") response = query_engine.query("What did the author do growing up?") print(response) ```
You can learn more about query engines and response modes.

## **”I want to stream the response back”**

documents = SimpleDirectoryReader("data").load_data() index = VectorStoreIndex.from_documents(documents) query_engine = index.as_query_engine(streaming=True) response = query_engine.query("What did the author do growing up?") response.print_response_stream() ```
You can learn more about streaming responses.

## **”I want a chatbot instead of Q\&A”**
``` from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
documents = SimpleDirectoryReader("data").load_data() index = VectorStoreIndex.from_documents(documents) query_engine = index.as_chat_engine() response = query_engine.chat("What did the author do growing up?") print(response)

response = query_engine.chat("Oh interesting, tell me more.") print(response) ```
Learn more about the chat engine.
---
## Next Steps
- Want a thorough walkthrough of (almost) everything you can configure? Get started with Understanding LlamaIndex. - Want more in-depth understanding of specific modules? Check out the component guides.

[1] https://llamahub.ai
# developers.llamaindex.ai/python/framework/integrations/retrievers/composable_retrievers/index.md
> https://developers.llamaindex.ai/python/framework/integrations/retrievers/composable_retrievers/index.md

--- title: Composable Objects | Developer Documentation ---

In this notebook, we show how you can combine multiple objects into a single top-level index.
This approach works by setting up `IndexNode` objects, with an `obj` field that points to a:
- query engine - retriever - query pipeline - another node!

``` object = IndexNode(index_id="my_object", obj=query_engine, text="some text about this object") ```
## Data Setup
``` %pip install llama-index-storage-docstore-mongodb %pip install llama-index-vector-stores-qdrant %pip install llama-index-storage-docstore-firestore %pip install llama-index-retrievers-bm25 %pip install llama-index-storage-docstore-redis %pip install llama-index-storage-docstore-dynamodb %pip install llama-index-readers-file pymupdf ```

``` !wget --user-agent "Mozilla" "https://arxiv.org/pdf/2307.09288.pdf" -O "./llama2.pdf" !wget --user-agent "Mozilla" "https://arxiv.org/pdf/1706.03762.pdf" -O "./attention.pdf" ```

``` from llama_index.core import download_loader
from llama_index.readers.file import PyMuPDFReader
llama2_docs = PyMuPDFReader().load_data( file_path="./llama2.pdf", metadata=True ) attention_docs = PyMuPDFReader().load_data( file_path="./attention.pdf", metadata=True ) ```

## Retriever Setup
``` import os
os.environ["OPENAI_API_KEY"] = "sk-..." ```
``` from llama_index.core.node_parser import TokenTextSplitter
nodes = TokenTextSplitter( chunk_size=1024, chunk_overlap=128 ).get_nodes_from_documents(llama2_docs + attention_docs) ```

``` from llama_index.core.storage.docstore import SimpleDocumentStore from llama_index.storage.docstore.redis import RedisDocumentStore from llama_index.storage.docstore.mongodb import MongoDocumentStore from llama_index.storage.docstore.firestore import FirestoreDocumentStore from llama_index.storage.docstore.dynamodb import DynamoDBDocumentStore

docstore = SimpleDocumentStore() docstore.add_documents(nodes) ```
``` from llama_index.core import VectorStoreIndex, StorageContext from llama_index.retrievers.bm25 import BM25Retriever from llama_index.vector_stores.qdrant import QdrantVectorStore from qdrant_client import QdrantClient

client = QdrantClient(path="./qdrant_data") vector_store = QdrantVectorStore("composable", client=client) storage_context = StorageContext.from_defaults(vector_store=vector_store)

index = VectorStoreIndex(nodes=nodes) vector_retriever = index.as_retriever(similarity_top_k=2) bm25_retriever = BM25Retriever.from_defaults( docstore=docstore, similarity_top_k=2 ) ```

## Composing Objects
Here, we construct the `IndexNodes`. Note that the text is what is used to index the node by the top-level index.
For a vector index, the text is embedded, for a keyword index, the text is used for keywords.
In this example, the `SummaryIndex` is used, which does not technically need the text for retrieval, since it always retrieves all nodes.

``` from llama_index.core import SummaryIndex

## Querying
When we query, all objects will be retrieved and used to generate the nodes to get a final answer.
Using `tree_summarize` with `aquery()` ensures concurrent execution and faster responses.
``` query_engine = summary_index.as_query_engine( response_mode="tree_summarize", verbose=True ) ```

``` response = await query_engine.aquery( "How does attention work in transformers?" ) ```

``` Attention in transformers works by mapping a query and a set of key-value pairs to an output. The output is computed as a weighted sum of the values, where the weights are determined by the similarity between the query and the keys. In the transformer model, attention is used in three different ways:
1. Encoder-decoder attention: The queries come from the previous decoder layer, and the memory keys and values come from the output of the encoder. This allows every position in the decoder to attend over all positions in the input sequence.
2. Self-attention in the encoder: In a self-attention layer, all of the keys, values, and queries come from the same place, which is the output of the previous layer in the encoder. Each position in the encoder can attend to all positions in the previous layer of the encoder.
3. Self-attention in the decoder: Similar to the encoder, self-attention layers in the decoder allow each position in the decoder to attend to all positions in the decoder up to and including that position. However, leftward information flow in the decoder is prevented to preserve the auto-regressive property.
Overall, attention in transformers allows the model to jointly attend to information from different representation subspaces at different positions, improving the model's ability to capture dependencies and relationships between different parts of the input sequence. ```
``` response = await query_engine.aquery( "What is the architecture of Llama2 based on?" ) ```

[Column 1]
``` The architecture of Llama 2 is based on the transformer model. ```
``` response = await query_engine.aquery( "What was used before attention in transformers?" ) ```

``` [1;3;38;2;11;159;203mRetrieval entering vector: VectorIndexRetriever [0m[1;3;38;2;11;159;203mRetrieval entering bm25: BM25Retriever [0m ```

``` print(str(response)) ```

## Note on Saving and Loading
Since objects aren’t technically serializable, when saving and loading, then need to be provided at load time as well.
Here’s an example of how I might save/load this setup.
### Save
``` # qdrant is already saved automatically! # we only need to save the docstore here

# save our docstore nodes for bm25 docstore.persist("./docstore.json") ```
### Load
``` from llama_index.core.storage.docstore import SimpleDocumentStore from llama_index.vector_stores.qdrant import QdrantVectorStore from qdrant_client import QdrantClient

docstore = SimpleDocumentStore.from_persist_path("./docstore.json")
client = QdrantClient(path="./qdrant_data") vector_store = QdrantVectorStore("composable", client=client) ```
``` index = VectorStoreIndex.from_vector_store(vector_store) vector_retriever = index.as_retriever(similarity_top_k=2) bm25_retriever = BM25Retriever.from_defaults( docstore=docstore, similarity_top_k=2 ) ```

``` from llama_index.core.schema import IndexNode
vector_obj = IndexNode( index_id="vector", obj=vector_retriever, text="Vector Retriever" ) bm25_obj = IndexNode( index_id="bm25", obj=bm25_retriever, text="BM25 Retriever" ) ```

``` # if we had added regular nodes to the summary index, we could save/load that as well # summary_index.persist("./summary_index.json") # summary_index = load_index_from_storage(storage_context, objects=objects)

from llama_index.core import SummaryIndex
summary_index = SummaryIndex(objects=[vector_obj, bm25_obj]) ```

[Column 2]
``` Recurrent neural networks, such as long short-term memory (LSTM) and gated recurrent neural networks, were commonly used before attention in transformers. These models were widely used in sequence modeling and transduction problems, including language modeling and machine translation. ```

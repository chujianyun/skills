# developers.llamaindex.ai/python/framework/integrations/retrievers/multi_doc_together_hybrid/index.md
> https://developers.llamaindex.ai/python/framework/integrations/retrievers/multi_doc_together_hybrid/index.md

[Column 1]
--- title: Chunk + Document Hybrid Retrieval with Long-Context Embeddings (Together.ai) | Developer Documentation ---

Visit <https://together.ai> and sign up to get an API key.
## Setup and Download Data
We load in our documentation. For the sake of speed we load in just 10 pages, but of course if you want to stress test your model you should load in all of it.
``` %pip install llama-index-embeddings-together %pip install llama-index-llms-openai %pip install llama-index-embeddings-openai %pip install llama-index-readers-file ```

``` domain = "docs.llamaindex.ai" docs_url = "https://docs.llamaindex.ai/en/latest/" !wget -e robots=off --recursive --no-clobber --page-requisites --html-extension --convert-links --restrict-file-names=windows --domains {domain} --no-parent {docs_url} ```

``` from llama_index.readers.file import UnstructuredReader from pathlib import Path from llama_index.llms.openai import OpenAI from llama_index.core import Document ```

``` reader = UnstructuredReader() # all_files_gen = Path("./docs.llamaindex.ai/").rglob("*") # all_files = [f.resolve() for f in all_files_gen] # all_html_files = [f for f in all_files if f.suffix.lower() == ".html"]

# curate a subset all_html_files = [ "docs.llamaindex.ai/en/latest/index.html", "docs.llamaindex.ai/en/latest/contributing/contributing.html", "docs.llamaindex.ai/en/latest/understanding/understanding.html", "docs.llamaindex.ai/en/latest/understanding/using_llms/using_llms.html", "docs.llamaindex.ai/en/latest/understanding/using_llms/privacy.html", "docs.llamaindex.ai/en/latest/understanding/loading/llamahub.html", "docs.llamaindex.ai/en/latest/optimizing/production_rag.html", "docs.llamaindex.ai/en/latest/module_guides/models/llms.html", ]

[Column 2]
This notebook shows how to use long-context together.ai embedding models for advanced RAG. We index each document by running the embedding model over the entire document text, as well as embedding each chunk. We then define a custom retriever that can compute both node similarity as well as document similarity.


# TODO: set to higher value if you want more docs doc_limit = 10
docs = [] for idx, f in enumerate(all_html_files): if idx > doc_limit: break print(f"Idx {idx}/{len(all_html_files)}") loaded_docs = reader.load_data(file=f, split_documents=True) # Hardcoded Index. Everything before this is ToC for all pages # Adjust this start_idx to suit your needs start_idx = 64 loaded_doc = Document( id_=str(f), text="\n\n".join([d.get_content() for d in loaded_docs[start_idx:]]), metadata={"path": str(f)}, ) print(str(f)) docs.append(loaded_doc) ```

``` [nltk_data] Downloading package punkt to /Users/jerryliu/nltk_data... [nltk_data] Package punkt is already up-to-date! [nltk_data] Downloading package averaged_perceptron_tagger to [nltk_data] /Users/jerryliu/nltk_data... [nltk_data] Package averaged_perceptron_tagger is already up-to- [nltk_data] date!

Idx 0/8 docs.llamaindex.ai/en/latest/index.html Idx 1/8 docs.llamaindex.ai/en/latest/contributing/contributing.html Idx 2/8 docs.llamaindex.ai/en/latest/understanding/understanding.html Idx 3/8 docs.llamaindex.ai/en/latest/understanding/using_llms/using_llms.html Idx 4/8 docs.llamaindex.ai/en/latest/understanding/using_llms/privacy.html Idx 5/8 docs.llamaindex.ai/en/latest/understanding/loading/llamahub.html Idx 6/8 docs.llamaindex.ai/en/latest/optimizing/production_rag.html Idx 7/8 docs.llamaindex.ai/en/latest/module_guides/models/llms.html ```

## Building Hybrid Retrieval with Chunk Embedding + Parent Embedding
Define a custom retriever that does the following:
- First retrieve relevant chunks based on embedding similarity - For each chunk, lookup the source document embedding. - Weight it by an alpha.
This is essentially vector retrieval with a reranking step that reweights the node similarities.
``` # You can set the API key in the embeddings or env # import os # os.environ["TOEGETHER_API_KEY"] = "your-api-key"

from llama_index.embeddings.together import TogetherEmbedding from llama_index.embeddings.openai import OpenAIEmbedding from llama_index.llms.openai import OpenAI

api_key = "<api_key>"
embed_model = TogetherEmbedding( model_name="togethercomputer/m2-bert-80M-32k-retrieval", api_key=api_key )

llm = OpenAI(temperature=0, model="gpt-3.5-turbo") ```
### Create Document Store
Create docstore for original documents. Embed each document, and put in docstore.
We will refer to this later in our hybrid retrieval algorithm!
``` from llama_index.core.storage.docstore import SimpleDocumentStore
for doc in docs: embedding = embed_model.get_text_embedding(doc.get_content()) doc.embedding = embedding

docstore = SimpleDocumentStore() docstore.add_documents(docs) ```
### Build Vector Index
Let’s build the vector index of chunks. Each chunk will also have a reference to its source document through its `index_id` (which can then be used to lookup the source document in the docstore).
``` from llama_index.core.schema import IndexNode from llama_index.core import ( load_index_from_storage, StorageContext, VectorStoreIndex, ) from llama_index.core.node_parser import SentenceSplitter from llama_index.core import SummaryIndex from llama_index.core.retrievers import RecursiveRetriever import os from tqdm.notebook import tqdm import pickle

def build_index(docs, out_path: str = "storage/chunk_index"): nodes = []
splitter = SentenceSplitter(chunk_size=512, chunk_overlap=70) for idx, doc in enumerate(tqdm(docs)): # print('Splitting: ' + str(idx))
cur_nodes = splitter.get_nodes_from_documents([doc]) for cur_node in cur_nodes: # ID will be base + parent file_path = doc.metadata["path"] new_node = IndexNode( text=cur_node.text or "None", index_id=str(file_path), metadata=doc.metadata # obj=doc ) nodes.append(new_node) print("num nodes: " + str(len(nodes)))

# save index to disk if not os.path.exists(out_path): index = VectorStoreIndex(nodes, embed_model=embed_model) index.set_index_id("simple_index") index.storage_context.persist(f"./{out_path}") else: # rebuild storage context storage_context = StorageContext.from_defaults( persist_dir=f"./{out_path}" ) # load index index = load_index_from_storage( storage_context, index_id="simple_index", embed_model=embed_model )

return index ```
``` index = build_index(docs) ```
### Define Hybrid Retriever
We define a hybrid retriever that can first fetch chunks by vector similarity, and then reweight it based on similarity with the parent document (using an alpha parameter).
``` from llama_index.core.retrievers import BaseRetriever from llama_index.core.indices.query.embedding_utils import get_top_k_embeddings from llama_index.core import QueryBundle from llama_index.core.schema import NodeWithScore from typing import List, Any, Optional

class HybridRetriever(BaseRetriever): """Hybrid retriever."""
def __init__( self, vector_index, docstore, similarity_top_k: int = 2, out_top_k: Optional[int] = None, alpha: float = 0.5, **kwargs: Any, ) -> None: """Init params.""" super().__init__(**kwargs) self._vector_index = vector_index self._embed_model = vector_index._embed_model self._retriever = vector_index.as_retriever( similarity_top_k=similarity_top_k ) self._out_top_k = out_top_k or similarity_top_k self._docstore = docstore self._alpha = alpha

def _retrieve(self, query_bundle: QueryBundle) -> List[NodeWithScore]: """Retrieve nodes given query."""
# first retrieve chunks nodes = self._retriever.retrieve(query_bundle.query_str)
# get documents, and embedding similiaryt between query and documents
# # get doc embeddings docs = [self._docstore.get_document(n.node.index_id) for n in nodes] doc_embeddings = [d.embedding for d in docs] query_embedding = self._embed_model.get_query_embedding( query_bundle.query_str )
# # compute doc similarities doc_similarities, doc_idxs = get_top_k_embeddings( query_embedding, doc_embeddings )
# # compute final similarity with doc similarities and original node similarity result_tups = [] for doc_idx, doc_similarity in zip(doc_idxs, doc_similarities): node = nodes[doc_idx] # weight alpha * node similarity + (1-alpha) * doc similarity full_similarity = (self._alpha * node.score) + ( (1 - self._alpha) * doc_similarity ) print( f"Doc {doc_idx} (node score, doc similarity, full similarity): {(node.score, doc_similarity, full_similarity)}" ) result_tups.append((full_similarity, node))

result_tups = sorted(result_tups, key=lambda x: x[0], reverse=True) # update scores for full_score, node in result_tups: node.score = full_score
return [n for _, n in result_tups][:out_top_k] ```
``` top_k = 10 out_top_k = 3 hybrid_retriever = HybridRetriever( index, docstore, similarity_top_k=top_k, out_top_k=3, alpha=0.5 ) base_retriever = index.as_retriever(similarity_top_k=out_top_k) ```

``` def show_nodes(nodes, out_len: int = 200): for idx, n in enumerate(nodes): print(f"\n\n >>>>>>>>>>>> ID {n.id_}: {n.metadata['path']}") print(n.get_content()[:out_len]) ```
``` query_str = "Tell me more about the LLM interface and where they're used" ```
``` nodes = hybrid_retriever.retrieve(query_str) ```
``` Doc 0 (node score, doc similarity, full similarity): (0.8951729860296237, 0.888711859390314, 0.8919424227099688) Doc 3 (node score, doc similarity, full similarity): (0.7606735418349336, 0.888711859390314, 0.8246927006126239) Doc 1 (node score, doc similarity, full similarity): (0.8008658562229534, 0.888711859390314, 0.8447888578066337) Doc 4 (node score, doc similarity, full similarity): (0.7083936595542725, 0.888711859390314, 0.7985527594722932) Doc 2 (node score, doc similarity, full similarity): (0.7627518988051541, 0.7151744680533735, 0.7389631834292638) Doc 5 (node score, doc similarity, full similarity): (0.6576277615091234, 0.6506473659825045, 0.654137563745814) Doc 7 (node score, doc similarity, full similarity): (0.6141130778320664, 0.6159139530209246, 0.6150135154264955) Doc 6 (node score, doc similarity, full similarity): (0.6225339833394525, 0.24827341793941335, 0.43540370063943296) Doc 8 (node score, doc similarity, full similarity): (0.5672766061523489, 0.24827341793941335, 0.4077750120458811) Doc 9 (node score, doc similarity, full similarity): (0.5671131641337652, 0.24827341793941335, 0.4076932910365893) ```

``` show_nodes(nodes) ```

>>>>>>>>>>>> ID 7c2be7c7-44aa-4f11-b670-e402e5ac35a5: docs.llamaindex.ai/en/latest/module_guides/models/llms.html If you change the LLM, you may need to update this tokenizer to ensure accurate token counts, chunking, and prompting.
The single requirement for a tokenizer is that it is a callable function, that t ```
``` base_nodes = base_retriever.retrieve(query_str) ```
``` show_nodes(base_nodes) ```
``` >>>>>>>>>>>> ID 2c7b42d3-520c-4510-ba34-d2f2dfd5d8f5: docs.llamaindex.ai/en/latest/module_guides/models/llms.html Contributing: Anyone is welcome to contribute new LLMs to the documentation. Simply copy an existing notebook, setup and test your LLM, and open a PR with your results.
If you have ways to improve th

>>>>>>>>>>>> ID 72cc9101-5b36-4821-bd50-e707dac8dca1: docs.llamaindex.ai/en/latest/module_guides/models/llms.html Using LLMs
Concept
Picking the proper Large Language Model (LLM) is one of the first steps you need to consider when building any LLM application over your data.
LLMs are a core component of Llam

>>>>>>>>>>>> ID 252fc99b-2817-4913-bcbf-4dd8ef509b8c: docs.llamaindex.ai/en/latest/index.html These could be APIs, PDFs, SQL, and (much) more.
Data indexes structure your data in intermediate representations that are easy and performant for LLMs to consume.
Engines provide natural language a ```
## Run Some Queries
``` from llama_index.core.query_engine import RetrieverQueryEngine
query_engine = RetrieverQueryEngine(hybrid_retriever) base_query_engine = index.as_query_engine(similarity_top_k=out_top_k) ```
``` response = query_engine.query(query_str) print(str(response)) ```
``` Doc 0 (node score, doc similarity, full similarity): (0.8951729860296237, 0.888711859390314, 0.8919424227099688) Doc 3 (node score, doc similarity, full similarity): (0.7606735418349336, 0.888711859390314, 0.8246927006126239) Doc 1 (node score, doc similarity, full similarity): (0.8008658562229534, 0.888711859390314, 0.8447888578066337) Doc 4 (node score, doc similarity, full similarity): (0.7083936595542725, 0.888711859390314, 0.7985527594722932) Doc 2 (node score, doc similarity, full similarity): (0.7627518988051541, 0.7151744680533735, 0.7389631834292638) Doc 5 (node score, doc similarity, full similarity): (0.6576277615091234, 0.6506473659825045, 0.654137563745814) Doc 7 (node score, doc similarity, full similarity): (0.6141130778320664, 0.6159139530209246, 0.6150135154264955) Doc 6 (node score, doc similarity, full similarity): (0.6225339833394525, 0.24827341793941335, 0.43540370063943296) Doc 8 (node score, doc similarity, full similarity): (0.5672766061523489, 0.24827341793941335, 0.4077750120458811) Doc 9 (node score, doc similarity, full similarity): (0.5671131641337652, 0.24827341793941335, 0.4076932910365893) The LLM interface is a unified interface provided by LlamaIndex for defining Large Language Models (LLMs) from different sources such as OpenAI, Hugging Face, or LangChain. This interface eliminates the need to write the boilerplate code for defining the LLM interface yourself. The LLM interface supports text completion and chat endpoints, as well as streaming and non-streaming endpoints. It also supports both synchronous and asynchronous endpoints.

To use LLMs, you can import the necessary modules and instantiate the LLM object. You can then use the LLM object to generate responses or complete text prompts. LlamaIndex provides examples and code snippets to help you get started with using LLMs.
It's important to note that tokenization plays a crucial role in LLMs. LlamaIndex uses a global tokenizer by default, but if you change the LLM, you may need to update the tokenizer to ensure accurate token counts, chunking, and prompting. LlamaIndex provides instructions on how to set a global tokenizer using libraries like tiktoken or Hugging Face's AutoTokenizer.
Overall, LLMs are powerful tools for building LlamaIndex applications and can be customized within the LlamaIndex abstractions. While LLMs from paid APIs like OpenAI and Anthropic are generally considered more reliable, local open-source models are gaining popularity due to their customizability and transparency. LlamaIndex offers integrations with various LLMs and provides documentation on their compatibility and performance. Contributions to improve the setup and performance of existing LLMs or to add new LLMs are welcome.
```
``` base_response = base_query_engine.query(query_str) print(str(base_response)) ```
``` The LLM interface is a unified interface provided by LlamaIndex for defining Large Language Model (LLM) modules. It allows users to easily integrate LLMs from different providers such as OpenAI, Hugging Face, or LangChain into their applications without having to write the boilerplate code for defining the LLM interface themselves.
LLMs are a core component of LlamaIndex and can be used as standalone modules or plugged into other core LlamaIndex modules such as indices, retrievers, and query engines. They are primarily used during the response synthesis step, which occurs after retrieval. Depending on the type of index being used, LLMs may also be used during index construction, insertion, and query traversal.
The LLM interface supports various functionalities, including text completion and chat endpoints. It also provides support for streaming and non-streaming endpoints, as well as synchronous and asynchronous endpoints.
To use LLMs, you can import the necessary modules and make use of the provided functions. For example, you can use the OpenAI module to interact with the gpt-3.5-turbo LLM by calling the `OpenAI()` function. You can then use the `complete()` function to generate completions based on a given prompt.
It's important to note that LlamaIndex uses a global tokenizer called cl100k from tiktoken by default for all token counting. If you change the LLM being used, you may need to update the tokenizer to ensure accurate token counts, chunking, and prompting.
Overall, LLMs and the LLM interface provided by LlamaIndex are essential for building LLM applications and integrating them into the LlamaIndex ecosystem. ```
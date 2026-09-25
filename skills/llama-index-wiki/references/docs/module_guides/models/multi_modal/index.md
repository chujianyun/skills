# developers.llamaindex.ai/python/framework/module_guides/models/multi_modal/index.md
> https://developers.llamaindex.ai/python/framework/module_guides/models/multi_modal/index.md

--- title: Multi-modal models | Developer Documentation ---
## Concept
Large language models (LLMs) are text-in, text-out. Large Multi-modal Models (LMMs) generalize this beyond the text modalities. For instance, models such as GPT-4V allow you to jointly input both images and text, and output text.
We’ve included a base `MultiModalLLM` abstraction to allow for text+image models. **NOTE**: This naming is subject to change!
## Usage Pattern
1. The following code snippet shows how you can get started using LMMs e.g. with GPT-4V.
``` from llama_index.multi_modal_llms.openai import OpenAIMultiModal from llama_index.core.multi_modal_llms.generic_utils import load_image_urls from llama_index.core import SimpleDirectoryReader

# load image documents from urls image_documents = load_image_urls(image_urls)
# load image documents from local directory image_documents = SimpleDirectoryReader(local_directory).load_data()
# non-streaming openai_mm_llm = OpenAIMultiModal( model="gpt-4-vision-preview", api_key=OPENAI_API_KEY, max_new_tokens=300 ) response = openai_mm_llm.complete( prompt="what is in the image?", image_documents=image_documents ) ```

2. The following code snippet shows how you can build MultiModal Vector Stores/Index.
``` from llama_index.core.indices import MultiModalVectorStoreIndex from llama_index.vector_stores.qdrant import QdrantVectorStore from llama_index.core import SimpleDirectoryReader, StorageContext

import qdrant_client from llama_index.core import SimpleDirectoryReader
# Create a local Qdrant vector store client = qdrant_client.QdrantClient(path="qdrant_mm_db")
# if you only need image_store for image retrieval, # you can remove text_store text_store = QdrantVectorStore( client=client, collection_name="text_collection" ) image_store = QdrantVectorStore( client=client, collection_name="image_collection" )

storage_context = StorageContext.from_defaults( vector_store=text_store, image_store=image_store )

# Load text and image documents from local folder documents = SimpleDirectoryReader("./data_folder/").load_data() # Create the MultiModal index index = MultiModalVectorStoreIndex.from_documents( documents, storage_context=storage_context, ) ```

3. The following code snippet shows how you can use MultiModal Retriever and Query Engine.
``` from llama_index.multi_modal_llms.openai import OpenAIMultiModal from llama_index.core import PromptTemplate from llama_index.core.query_engine import SimpleMultiModalQueryEngine

retriever_engine = index.as_retriever( similarity_top_k=3, image_similarity_top_k=3 )

# retrieve more information from the GPT4V response retrieval_results = retriever_engine.retrieve(response)
# if you only need image retrieval without text retrieval # you can use `text_to_image_retrieve` # retrieval_results = retriever_engine.text_to_image_retrieve(response)

qa_tmpl_str = ( "Context information is below.\n" "---------------------\n" "{context_str}\n" "---------------------\n" "Given the context information and not prior knowledge, " "answer the query.\n" "Query: {query_str}\n" "Answer: " ) qa_tmpl = PromptTemplate(qa_tmpl_str)

query_engine = index.as_query_engine( multi_modal_llm=openai_mm_llm, text_qa_template=qa_tmpl )

query_str = "Tell me more about the Porsche" response = query_engine.query(query_str) ```
**Legend**
- ✅ = should work fine - ⚠️ = sometimes unreliable, may need more tuning to improve - 🛑 = not available at the moment.

### End to End Multi-Modal Work Flow
The tables below attempt to show the **initial** steps with various LlamaIndex features for building your own Multi-Modal RAGs (Retrieval Augmented Generation). You can combine different modules/steps together for composing your own Multi-Modal RAG orchestration.
| Query Type | Data Sources for MultiModal Vector Store/Index | MultiModal Embedding | Retriever | Query Engine | Output Data Type | | ---------- | ---------------------------------------------- | --------------------------------- | ------------------------------------------- | --------------------- | ------------------------------------ | | Text ✅ | Text ✅ | Text ✅ | Top-k retrieval ✅ Simple Fusion retrieval ✅ | Simple Query Engine ✅ | Retrieved Text ✅ Generated Text ✅ | Image ✅ | Image ✅ | Image ✅ Image to Text Embedding ✅ | Top-k retrieval ✅ Simple Fusion retrieval ✅ | Simple Query Engine ✅ | Retrieved Image ✅ Generated Image 🛑 | Audio 🛑 | Audio 🛑 | Audio 🛑 | 🛑 | 🛑 | Audio 🛑 | Video 🛑 | Video 🛑 | Video 🛑 | 🛑 | 🛑 | Video 🛑

### Multi-Modal LLM Models
These notebooks serve as examples how to leverage and integrate Multi-Modal LLM model, Multi-Modal embeddings, Multi-Modal vector stores, Retriever, Query engine for composing Multi-Modal Retrieval Augmented Generation (RAG) orchestration.
| Multi-Modal Vision Models | Single Image Reasoning | Multiple Images Reasoning | Image Embeddings | Simple Query Engine | Pydantic Structured Output | | ----------------------------------------------------------------------------------------- | ---------------------- | ------------------------- | ---------------- | ------------------- | -------------------------- | | GPT4V (OpenAI API) | ✅ | ✅ | 🛑 | ✅ | ✅ | GPT4V-Azure (Azure API) | ✅ | ✅ | 🛑 | ✅ | ✅ | Gemini (Google) | ✅ | ✅ | 🛑 | ✅ | ✅ | CLIP (Local host) | 🛑 | 🛑 | ✅ | 🛑 | 🛑 | LLaVa (replicate) | ✅ | 🛑 | 🛑 | ✅ | ⚠️ | | Fuyu-8B (replicate) | ✅ | 🛑 | 🛑 | ✅ | ⚠️ | | ImageBind  [1]\[To integrate] | 🛑 | 🛑 | ✅ | 🛑 | 🛑 | MiniGPT-4  | ✅ | 🛑 | 🛑 | ✅ | ⚠️ | | CogVLM  [2] | ✅ | 🛑 | 🛑 | ✅ | ⚠️ | | Qwen-VL  [3]\[To integrate] | ✅ | 🛑 | 🛑 | ✅ | ⚠️ |

### Multi Modal Vector Stores
Below table lists some vector stores supporting Multi-Modal use cases. Our LlamaIndex built-in `MultiModalVectorStoreIndex` supports building separate vector stores for image and text embedding vector stores. `MultiModalRetriever`, and `SimpleMultiModalQueryEngine` support text to text/image and image to image retrieval and simple ranking fusion functions for combining text and image retrieval results.
| Multi-Modal Vector Stores | Single Vector Store | Multiple Vector Stores | Text Embedding | Image Embedding | | ----------------------------------------------------------------------------------------------------------------------- | ------------------- | ---------------------- | --------------------------------------------------- | -------------------------------------------------- | | LLamaIndex self-built MultiModal Index | 🛑 | ✅ | Can be arbitrary text embedding (Default is GPT3.5) | Can be arbitrary Image embedding (Default is CLIP) | | Chroma | ✅ | 🛑 | CLIP ✅ | CLIP ✅ | | Weaviate [4] \[To integrate] | ✅ | 🛑 | CLIP ✅ ImageBind ✅ | CLIP ✅ ImageBind ✅ |

## Multi-Modal LLM Modules
We support integrations with GPT4-V, Anthropic (Opus, Sonnet), Gemini (Google), CLIP (OpenAI), BLIP (Salesforce), and Replicate (LLaVA, Fuyu-8B, MiniGPT-4, CogVLM), and more.
- OpenAI - Gemini - Anthropic - Replicate - Pydantic Multi-Modal - GPT-4v COT Experiments - Llava Tesla 10q

## Multi-Modal Retrieval Augmented Generation
We support Multi-Modal Retrieval Augmented Generation with different Multi-Modal LLMs with Multi-Modal vector stores.
- GPT-4v Retrieval - Multi-Modal Retrieval - Image-to-Image Retrieval - Chroma Multi-Modal

## Evaluation
We support basic evaluation for Multi-Modal LLM and Retrieval Augmented Generation.
- Multi-Modal RAG Eval

[1] https://imagebind.metademolab.com/
[2] https://github.com/THUDM/CogVLM
[3] https://arxiv.org/abs/2308.12966
[4] https://weaviate.io/developers/weaviate/modules/retriever-vectorizer-modules/multi2vec-bind
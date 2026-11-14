# Build a semantic search engine with LangChain

## Overview

Build a semantic search engine over a PDF with LangChain [embeddings](https://docs.langchain.com/oss/python/integrations/embeddings.md) and [vector stores](https://docs.langchain.com/oss/python/integrations/vectorstores.md). Use it to retrieve passages similar to a query, then plug the retriever into [retrieval-augmented generation (RAG)](../../../Advanced%20usage/Retrieval.md) or other LLM workflows.

This tutorial covers:

1. Create `Document` objects from a PDF.
2. Generate embeddings.
3. Load and split a PDF.
4. Index chunks in a vector store and query by similarity.
5. Wrap the store as a retriever.

The guide also includes a minimal RAG implementation on top of the search engine.

### Concepts

This tutorial focuses on text retrieval and covers the following concepts:

* [`Document`](https://reference.langchain.com/python/langchain-core/documents/base/Document)
* [Text splitters](https://docs.langchain.com/oss/python/integrations/splitters.md)
* [Embeddings](https://docs.langchain.com/oss/python/integrations/embeddings.md)
* [Vector stores](https://docs.langchain.com/oss/python/integrations/vectorstores.md) and [retrievers](https://docs.langchain.com/oss/python/integrations/retrievers.md)

## Setup

### Install dependencies

This tutorial reads a PDF using the `pypdf` package:

```bash pip
pip install pypdf
```

```bash conda
conda install pypdf -c conda-forge
```

```bash uv
uv add pypdf
```

For more details, see the [Installation guide](../../../Get%20started/Install%20LangChain.md).

### Configure LangSmith

Many of the applications you build with LangChain will contain multiple steps with multiple invocations of LLM calls.
As these applications get more and more complex, it becomes crucial to be able to inspect what exactly is going on inside your chain or agent.
The best way to do this is with [LangSmith](https://smith.langchain.com?utm_source=docs\&utm_medium=cta\&utm_campaign=langsmith-signup\&utm_content=oss-langchain-knowledge-base).

After you sign up at the link above, make sure to set your environment variables to start logging traces:

```shell
export LANGSMITH_TRACING="true"
export LANGSMITH_API_KEY="..."
```

In a notebook, you can set them with:

```python
import getpass
import os

os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_API_KEY"] = getpass.getpass()
```

## Create documents

LangChain implements a [`Document`](https://reference.langchain.com/python/langchain-core/documents/base/Document) abstraction for a unit of text and associated metadata. It has three attributes:

* `page_content`: a string representing the content.
* `metadata`: a dict containing arbitrary metadata.
* `id`: (optional) a string identifier for the document.

`metadata` can capture the source of the document, its relationship to other documents, and other information. An individual [`Document`](https://reference.langchain.com/python/langchain-core/documents/base/Document) often represents a chunk of a larger document.

The following code creates sample documents:

```python
from langchain_core.documents import Document

documents = [
    Document(
        page_content="Dogs are great companions, known for their loyalty and friendliness.",
        metadata={"source": "mammal-pets-doc"},
    ),
    Document(
        page_content="Cats are independent pets that often enjoy their own space.",
        metadata={"source": "mammal-pets-doc"},
    ),
]
```

## Generate embeddings

Vector search stores numeric vectors associated with text. Embed a query as a vector of the same dimension, then use similarity metrics (such as cosine similarity) to find related text.

LangChain supports embeddings from [many providers](https://docs.langchain.com/oss/python/integrations/embeddings.md). Select a model to specify how text should be converted into a numeric vector:

> [tab] OpenAI
>
> ```shell
> pip install -U "langchain-openai"
> ```
>
> ```python
> import getpass
> import os
>
> if not os.environ.get("OPENAI_API_KEY"):
>     os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter API key for OpenAI: ")
>
> from langchain_openai import OpenAIEmbeddings
>
> embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
> ```

> [tab] Azure
>
> ```shell
> pip install -U "langchain-openai"
> ```
>
> ```python
> import getpass
> import os
>
> if not os.environ.get("AZURE_OPENAI_API_KEY"):
>     os.environ["AZURE_OPENAI_API_KEY"] = getpass.getpass("Enter API key for Azure: ")
>
> from langchain_openai import AzureOpenAIEmbeddings
>
> embeddings = AzureOpenAIEmbeddings(
>     azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
>     azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
>     openai_api_version=os.environ["AZURE_OPENAI_API_VERSION"],
> )
> ```

> [tab] Google Gemini
>
> ```shell
> pip install -qU langchain-google-genai
> ```
>
> ```python
> import getpass
> import os
>
> if not os.environ.get("GOOGLE_API_KEY"):
>     os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter API key for Google Gemini: ")
>
> from langchain_google_genai import GoogleGenerativeAIEmbeddings
>
> embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
> ```

> [tab] Gemini Enterprise Agent Platform
>
> ```shell
> pip install -qU langchain-google-vertexai
> ```
>
> ```python
> from langchain_google_vertexai import VertexAIEmbeddings
>
> embeddings = VertexAIEmbeddings(model="text-embedding-005")
> ```

> [tab] AWS
>
> ```shell
> pip install -qU langchain-aws
> ```
>
> ```python
> from langchain_aws import BedrockEmbeddings
>
> embeddings = BedrockEmbeddings(model_id="amazon.titan-embed-text-v2:0")
> ```

> [tab] HuggingFace
>
> ```shell
> pip install -qU langchain-huggingface
> ```
>
> ```python
> from langchain_huggingface import HuggingFaceEmbeddings
>
> embeddings = HuggingFaceEmbeddings(
>     model_name="sentence-transformers/all-mpnet-base-v2",
>     encode_kwargs={"normalize_embeddings": True},
> )
> ```

> [tab] Ollama
>
> ```shell
> pip install -qU langchain-ollama
> ```
>
> ```python
> from langchain_ollama import OllamaEmbeddings
>
> embeddings = OllamaEmbeddings(model="llama3")
> ```

> [tab] Cohere
>
> ```shell
> pip install -qU langchain-cohere
> ```
>
> ```python
> import getpass
> import os
>
> if not os.environ.get("COHERE_API_KEY"):
>     os.environ["COHERE_API_KEY"] = getpass.getpass("Enter API key for Cohere: ")
>
> from langchain_cohere import CohereEmbeddings
>
> embeddings = CohereEmbeddings(model="embed-english-v3.0")
> ```

> [tab] MistralAI
>
> ```shell
> pip install -qU langchain-mistralai
> ```
>
> ```python
> import getpass
> import os
>
> if not os.environ.get("MISTRALAI_API_KEY"):
>     os.environ["MISTRALAI_API_KEY"] = getpass.getpass("Enter API key for MistralAI: ")
>
> from langchain_mistralai import MistralAIEmbeddings
>
> embeddings = MistralAIEmbeddings(model="mistral-embed")
> ```

> [tab] Nomic
>
> ```shell
> pip install -qU langchain-nomic
> ```
>
> ```python
> import getpass
> import os
>
> if not os.environ.get("NOMIC_API_KEY"):
>     os.environ["NOMIC_API_KEY"] = getpass.getpass("Enter API key for Nomic: ")
>
> from langchain_nomic import NomicEmbeddings
>
> embeddings = NomicEmbeddings(model="nomic-embed-text-v1.5")
> ```

> [tab] NVIDIA
>
> ```shell
> pip install -qU langchain-nvidia-ai-endpoints
> ```
>
> ```python
> import getpass
> import os
>
> if not os.environ.get("NVIDIA_API_KEY"):
>     os.environ["NVIDIA_API_KEY"] = getpass.getpass("Enter API key for NVIDIA: ")
>
> from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings
>
> embeddings = NVIDIAEmbeddings(model="NV-Embed-QA")
> ```

> [tab] Voyage AI
>
> ```shell
> pip install -qU langchain-voyageai
> ```
>
> ```python
> import getpass
> import os
>
> if not os.environ.get("VOYAGE_API_KEY"):
>     os.environ["VOYAGE_API_KEY"] = getpass.getpass("Enter API key for Voyage AI: ")
>
> from langchain_voyageai import VoyageAIEmbeddings
>
> embeddings = VoyageAIEmbeddings(model="voyage-3")
> ```

> [tab] IBM watsonx
>
> ```shell
> pip install -qU langchain-ibm
> ```
>
> ```python
> import getpass
> import os
>
> if not os.environ.get("WATSONX_APIKEY"):
>     os.environ["WATSONX_APIKEY"] = getpass.getpass("Enter API key for IBM watsonx: ")
>
> from langchain_ibm import WatsonxEmbeddings
>
> embeddings = WatsonxEmbeddings(
>     model_id="ibm/slate-125m-english-rtrvr",
>     url="https://us-south.ml.cloud.ibm.com",
>     project_id="<WATSONX PROJECT_ID>",
> )
> ```

> [tab] Fake
>
> ```shell
> pip install -qU langchain-core
> ```
>
> ```python
> from langchain_core.embeddings import DeterministicFakeEmbedding
>
> embeddings = DeterministicFakeEmbedding(size=4096)
> ```

> [tab] Isaacus
>
> ```shell
> pip install -qU langchain-isaacus
> ```
>
> ```python
> import getpass
> import os
>
> if not os.environ.get("ISAACUS_API_KEY"):
>     os.environ["ISAACUS_API_KEY"] = getpass.getpass("Enter API key for Isaacus: ")
>
> from langchain_isaacus import IsaacusEmbeddings
>
> embeddings = IsaacusEmbeddings(model="kanon-2-embedder")
> ```

```python
vector_1 = embeddings.embed_query(documents[0].page_content)
vector_2 = embeddings.embed_query(documents[1].page_content)

assert len(vector_1) == len(vector_2)
print(f"Generated vectors of length {len(vector_1)}\n")
print(vector_1[:10])
```

```text wrap
Generated vectors of length 1536

[-0.008586574345827103, -0.03341241180896759, -0.008936782367527485, -0.0036674530711025, 0.010564599186182022, 0.009598285891115665, -0.028587326407432556, -0.015824200585484505, 0.0030416189692914486, -0.012899317778646946]
```

Next, store embeddings in a vector store that supports efficient similarity search.

## Select a vector store

LangChain [`VectorStore`](https://reference.langchain.com/python/langchain-core/vectorstores/base/VectorStore) objects add text and [`Document`](https://reference.langchain.com/python/langchain-core/documents/base/Document) objects to a store and query them with similarity metrics. They are often initialized with [embedding](https://docs.langchain.com/oss/python/integrations/embeddings.md) models that translate text into numeric vectors.

LangChain includes [integrations](https://docs.langchain.com/oss/python/integrations/vectorstores.md) with many vector store technologies. Some are hosted and need credentials, some run in separate infrastructure (local or third-party), and others run in-memory for lightweight workloads. Select a vector store:

> [tab] In-memory
>
> ```shell
> pip install -U "langchain-core"
> ```
>
> ```python
> from langchain_core.vectorstores import InMemoryVectorStore
>
> vector_store = InMemoryVectorStore(embeddings)
> ```

> [tab] Amazon OpenSearch
>
> ```shell
> pip install -qU  boto3
> ```
>
> ```python
> from opensearchpy import RequestsHttpConnection
>
> service = "es"  # must set the service as 'es'
> region = "us-east-2"
> credentials = boto3.Session(
>     aws_access_key_id="xxxxxx", aws_secret_access_key="xxxxx"
> ).get_credentials()
> awsauth = AWS4Auth("xxxxx", "xxxxxx", region, service, session_token=credentials.token)
>
> vector_store = OpenSearchVectorSearch.from_documents(
>     docs,
>     embeddings,
>     opensearch_url="host url",
>     http_auth=awsauth,
>     timeout=300,
>     use_ssl=True,
>     verify_certs=True,
>     connection_class=RequestsHttpConnection,
>     index_name="test-index",
> )
> ```

> [tab] AstraDB
>
> ```shell
> pip install -U "langchain-astradb"
> ```
>
> ```python
> from langchain_astradb import AstraDBVectorStore
>
> vector_store = AstraDBVectorStore(
>     embedding=embeddings,
>     api_endpoint=ASTRA_DB_API_ENDPOINT,
>     collection_name="astra_vector_langchain",
>     token=ASTRA_DB_APPLICATION_TOKEN,
>     namespace=ASTRA_DB_NAMESPACE,
> )
> ```

> [tab] Chroma
>
> ```shell
> pip install -qU langchain-chroma
> ```
>
> ```python
> from langchain_chroma import Chroma
>
> vector_store = Chroma(
>     collection_name="example_collection",
>     embedding_function=embeddings,
>     persist_directory="./chroma_langchain_db",  # Where to save data locally, remove if not necessary
> )
> ```

> [tab] Milvus
>
> ```shell
> pip install -qU langchain-milvus
> ```
>
> ```python
> from langchain_milvus import Milvus
>
> URI = "./milvus_example.db"
>
> vector_store = Milvus(
>     embedding_function=embeddings,
>     connection_args={"uri": URI},
>     index_params={"index_type": "FLAT", "metric_type": "L2"},
> )
> ```

> [tab] MongoDB
>
> ```shell
> pip install -qU langchain-mongodb
> ```
>
> ```python
> from langchain_mongodb import MongoDBAtlasVectorSearch
>
> vector_store = MongoDBAtlasVectorSearch(
>     embedding=embeddings,
>     collection=MONGODB_COLLECTION,
>     index_name=ATLAS_VECTOR_SEARCH_INDEX_NAME,
>     relevance_score_fn="cosine",
> )
> ```

> [tab] PGVector
>
> ```shell
> pip install -qU langchain-postgres
> ```
>
> ```python
> from langchain_postgres import PGVector
>
> vector_store = PGVector(
>     embeddings=embeddings,
>     collection_name="my_docs",
>     connection="postgresql+psycopg://...",
> )
> ```

> [tab] PGVectorStore
>
> ```shell
> pip install -qU langchain-postgres
> ```
>
> ```python
> from langchain_postgres import PGEngine, PGVectorStore
>
> pg_engine = PGEngine.from_connection_string(
>     url="postgresql+psycopg://..."
> )
>
> vector_store = PGVectorStore.create_sync(
>     engine=pg_engine,
>     table_name='test_table',
>     embedding_service=embeddings
> )
> ```

> [tab] Pinecone
>
> ```shell
> pip install -qU langchain-pinecone
> ```
>
> ```python
> from langchain_pinecone import PineconeVectorStore
> from pinecone import Pinecone
>
> pc = Pinecone(api_key=...)
> index = pc.Index(index_name)
>
> vector_store = PineconeVectorStore(embedding=embeddings, index=index)
> ```

> [tab] Qdrant
>
> ```shell
> pip install -qU langchain-qdrant
> ```
>
> ```python
> from qdrant_client.models import Distance, VectorParams
> from langchain_qdrant import QdrantVectorStore
> from qdrant_client import QdrantClient
>
> client = QdrantClient(":memory:")
>
> vector_size = len(embeddings.embed_query("sample text"))
>
> if not client.collection_exists("test"):
>     client.create_collection(
>         collection_name="test",
>         vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
>     )
> vector_store = QdrantVectorStore(
>     client=client,
>     collection_name="test",
>     embedding=embeddings,
> )
> ```

## Load and split a PDF

Load content from a PDF, then split it into smaller chunks before indexing. This example uses [a sample Nike 10-K filing from 2023](https://github.com/langchain-ai/langchain/blob/v0.3/docs/docs/example_data/nke-10k-2023.pdf).

Download the sample PDF before running the example. Set `file_path` (Python) or `filePath` (JavaScript) to the downloaded file's absolute path, or use a path relative to your working directory.

For dedicated PDF document loaders (including `PyPDFLoader` and partner packages), see [PDF document loaders](https://docs.langchain.com/oss/python/integrations/document_loaders.md#pdfs).

```python
import pypdf
from langchain_core.documents import Document


# Below is a minimal helper for demonstration purposes.
def load_pdf_pages(file_path: str) -> list[Document]:
    reader = pypdf.PdfReader(file_path)
    return [
        Document(
            page_content=page.extract_text() or "",
            metadata={"source": file_path, "page": i},
        )
        for i, page in enumerate(reader.pages)
    ]


file_path = "../example_data/nke-10k-2023.pdf"
docs = load_pdf_pages(file_path)
print(len(docs))
```

```text
107
```

A page is often too coarse for retrieval. Split pages further so relevant passages are not diluted by surrounding text. [`RecursiveCharacterTextSplitter`](https://reference.langchain.com/python/langchain-text-splitters/character/RecursiveCharacterTextSplitter) recursively splits on common separators (such as newlines) until each chunk is the target size. This is the recommended text splitter for generic text use cases.

Set `add_start_index=True` so each split keeps a `start_index` metadata field for its character offset in the original document.

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=200, add_start_index=True
)
all_splits = text_splitter.split_documents(docs)

print(len(all_splits))
```

```text
516
```

## Index documents

Index the chunks into the vector store:

```python
ids = vector_store.add_documents(documents=all_splits)
```

Most vector store integrations also support connecting to an existing store (for example with a client or index name). See the docs for a specific [integration](https://docs.langchain.com/oss/python/integrations/vectorstores.md) for details.

## Query the vector store

After you have added the documents to the [`VectorStore`](https://reference.langchain.com/python/langchain-core/vectorstores/base/VectorStore), you can query it:

* Synchronously and asynchronously
* By string query and by vector
* With and without similarity scores
* By similarity and [maximum marginal relevance](https://reference.langchain.com/python/langchain-core/vectorstores/base/VectorStore/max_marginal_relevance_search) (to balance similarity with diversity)

These methods generally return a list of [`Document`](https://reference.langchain.com/python/langchain-core/documents/base/Document) objects.

### Search by string

Embeddings map text to dense vectors so similar meanings are geometrically close. This means you can Retrieve relevant passages by passing a natural-language question:

```python
results = vector_store.similarity_search(
    "How many distribution centers does Nike have in the US?"
)

print(results[0])
```

```python wrap
page_content='direct to consumer operations sell products through the following number of retail stores in the United States:
U.S. RETAIL STORES NUMBER
NIKE Brand factory stores 213
NIKE Brand in-line stores (including employee-only stores) 74
Converse stores (including factory stores) 82
TOTAL 369
In the United States, NIKE has eight significant distribution centers. Refer to Item 2. Properties for further information.
2023 FORM 10-K 2' metadata={'page': 4, 'source': '../example_data/nke-10k-2023.pdf', 'start_index': 3125}
```

Async query:

```python
results = await vector_store.asimilarity_search("When was Nike incorporated?")

print(results[0])
```

```python wrap
page_content='Table of Contents
PART I
ITEM 1. BUSINESS
GENERAL
NIKE, Inc. was incorporated in 1967 under the laws of the State of Oregon. As used in this Annual Report on Form 10-K (this "Annual Report"), the terms "we," "us," "our,"
"NIKE" and the "Company" refer to NIKE, Inc. and its predecessors, subsidiaries and affiliates, collectively, unless the context indicates otherwise.
Our principal business activity is the design, development and worldwide marketing and selling of athletic footwear, apparel, equipment, accessories and services. NIKE is
the largest seller of athletic footwear and apparel in the world. We sell our products through NIKE Direct operations, which are comprised of both NIKE-owned retail stores
and sales through our digital platforms (also referred to as "NIKE Brand Digital"), to retail accounts and to a mix of independent distributors, licensees and sales' metadata={'page': 3, 'source': '../example_data/nke-10k-2023.pdf', 'start_index': 0}
```

### Return scores

You can return similarity scores with the documents. Score meaning varies by provider. In this case, the score is a distance metric that varies inversely with similarity:

```python
# Note that providers implement different scores; the score here
# is a distance metric that varies inversely with similarity.

results = vector_store.similarity_search_with_score("What was Nike's revenue in 2023?")
doc, score = results[0]
print(f"Score: {score}\n")
print(doc)
```

```python wrap
Score: 0.23699893057346344

page_content='Table of Contents
FISCAL 2023 NIKE BRAND REVENUE HIGHLIGHTS
The following tables present NIKE Brand revenues disaggregated by reportable operating segment, distribution channel and major product line:
FISCAL 2023 COMPARED TO FISCAL 2022
•NIKE, Inc. Revenues were $51.2 billion in fiscal 2023, which increased 10% and 16% compared to fiscal 2022 on a reported and currency-neutral basis, respectively.
The increase was due to higher revenues in North America, Europe, Middle East & Africa ("EMEA"), APLA and Greater China, which contributed approximately 7, 6,
2 and 1 percentage points to NIKE, Inc. Revenues, respectively.
•NIKE Brand revenues, which represented over 90% of NIKE, Inc. Revenues, increased 10% and 16% on a reported and currency-neutral basis, respectively. This
increase was primarily due to higher revenues in Men's, the Jordan Brand, Women's and Kids' which grew 17%, 35%,11% and 10%, respectively, on a wholesale
equivalent basis.' metadata={'page': 35, 'source': '../example_data/nke-10k-2023.pdf', 'start_index': 0}
```

### Search by vector

Embed the query yourself, then search with the resulting vector:

```python
embedding = embeddings.embed_query("How were Nike's margins impacted in 2023?")

results = vector_store.similarity_search_by_vector(embedding)
print(results[0])
```

```python wrap
page_content='Table of Contents
GROSS MARGIN
FISCAL 2023 COMPARED TO FISCAL 2022
For fiscal 2023, our consolidated gross profit increased 4% to $22,292 million compared to $21,479 million for fiscal 2022. Gross margin decreased 250 basis points to
43.5% for fiscal 2023 compared to 46.0% for fiscal 2022 due to the following:
*Wholesale equivalent
The decrease in gross margin for fiscal 2023 was primarily due to:
•Higher NIKE Brand product costs, on a wholesale equivalent basis, primarily due to higher input costs and elevated inbound freight and logistics costs as well as
product mix;
•Lower margin in our NIKE Direct business, driven by higher promotional activity to liquidate inventory in the current period compared to lower promotional activity in
the prior period resulting from lower available inventory supply;
•Unfavorable changes in net foreign currency exchange rates, including hedges; and
•Lower off-price margin, on a wholesale equivalent basis.
This was partially offset by:' metadata={'page': 36, 'source': '../example_data/nke-10k-2023.pdf', 'start_index': 0}
```

Learn more:

* [API Reference](https://reference.langchain.com/python/langchain-core/vectorstores/base/VectorStore)
* [Integration-specific docs](https://docs.langchain.com/oss/python/integrations/vectorstores.md)

## Use retrievers

LangChain [`VectorStore`](https://reference.langchain.com/python/langchain-core/vectorstores/base/VectorStore) objects do not subclass [`Runnable`](https://reference.langchain.com/python/langchain-core/runnables/base/Runnable). [Retrievers](https://reference.langchain.com/python/langchain-core/retrievers/BaseRetriever) are Runnables, so they support standard methods such as sync and async `invoke` and `batch`.

You can also build retrievers from vector stores, and retrievers can also wrap non-vector sources (such as external APIs).

In this case, create a simple retriever without subclassing `Retriever` by wrapping `similarity_search`:

```python
from typing import List

from langchain_core.documents import Document
from langchain_core.runnables import chain


@chain
def retriever(query: str) -> List[Document]:
    return vector_store.similarity_search(query, k=1)


retriever.batch(
    [
        "How many distribution centers does Nike have in the US?",
        "When was Nike incorporated?",
    ],
)
```

```text wrap
[[Document(metadata={'page': 4, 'source': '../example_data/nke-10k-2023.pdf', 'start_index': 3125}, page_content='direct to consumer operations sell products through the following number of retail stores in the United States:\nU.S. RETAIL STORES NUMBER\nNIKE Brand factory stores 213 \nNIKE Brand in-line stores (including employee-only stores) 74 \nConverse stores (including factory stores) 82 \nTOTAL 369 \nIn the United States, NIKE has eight significant distribution centers. Refer to Item 2. Properties for further information.\n2023 FORM 10-K 2')],
 [Document(metadata={'page': 3, 'source': '../example_data/nke-10k-2023.pdf', 'start_index': 0}, page_content='Table of Contents\nPART I\nITEM 1. BUSINESS\nGENERAL\nNIKE, Inc. was incorporated in 1967 under the laws of the State of Oregon. As used in this Annual Report on Form 10-K (this "Annual Report"), the terms "we," "us," "our,"\n"NIKE" and the "Company" refer to NIKE, Inc. and its predecessors, subsidiaries and affiliates, collectively, unless the context indicates otherwise.\nOur principal business activity is the design, development and worldwide marketing and selling of athletic footwear, apparel, equipment, accessories and services. NIKE is\nthe largest seller of athletic footwear and apparel in the world. We sell our products through NIKE Direct operations, which are comprised of both NIKE-owned retail stores\nand sales through our digital platforms (also referred to as "NIKE Brand Digital"), to retail accounts and to a mix of independent distributors, licensees and sales')]]
```

Vector stores implement an `as_retriever` method that returns a [`VectorStoreRetriever`](https://reference.langchain.com/python/langchain-core/vectorstores/base/VectorStoreRetriever). These retrievers expose `search_type` and `search_kwargs` to select and parameterize the underlying store methods. Replicate the example above with:

```python
retriever = vector_store.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 1},
)

retriever.batch(
    [
        "How many distribution centers does Nike have in the US?",
        "When was Nike incorporated?",
    ],
)
```

```text wrap
[[Document(metadata={'page': 4, 'source': '../example_data/nke-10k-2023.pdf', 'start_index': 3125}, page_content='direct to consumer operations sell products through the following number of retail stores in the United States:\nU.S. RETAIL STORES NUMBER\nNIKE Brand factory stores 213 \nNIKE Brand in-line stores (including employee-only stores) 74 \nConverse stores (including factory stores) 82 \nTOTAL 369 \nIn the United States, NIKE has eight significant distribution centers. Refer to Item 2. Properties for further information.\n2023 FORM 10-K 2')],
 [Document(metadata={'page': 3, 'source': '../example_data/nke-10k-2023.pdf', 'start_index': 0}, page_content='Table of Contents\nPART I\nITEM 1. BUSINESS\nGENERAL\nNIKE, Inc. was incorporated in 1967 under the laws of the State of Oregon. As used in this Annual Report on Form 10-K (this "Annual Report"), the terms "we," "us," "our,"\n"NIKE" and the "Company" refer to NIKE, Inc. and its predecessors, subsidiaries and affiliates, collectively, unless the context indicates otherwise.\nOur principal business activity is the design, development and worldwide marketing and selling of athletic footwear, apparel, equipment, accessories and services. NIKE is\nthe largest seller of athletic footwear and apparel in the world. We sell our products through NIKE Direct operations, which are comprised of both NIKE-owned retail stores\nand sales through our digital platforms (also referred to as "NIKE Brand Digital"), to retail accounts and to a mix of independent distributors, licensees and sales')]]
```

`VectorStoreRetriever` supports search types of `"similarity"` (default), `"mmr"` (maximum marginal relevance), and `"similarity_score_threshold"`. Use the last option to filter documents by similarity score.

You can use retrievers in more complex apps such as [retrieval-augmented generation (RAG)](../../../Advanced%20usage/Retrieval.md), which combine a question with retrieved context in a prompt for an LLM. To learn more about building such an application, check out the [RAG tutorial](https://docs.langchain.com/oss/python/deepagents/rag.md) tutorial.

## Next steps

You've now seen how to build a semantic search engine over a PDF document.

For more information see:

* [Available embedding integrations](https://docs.langchain.com/oss/python/integrations/embeddings.md)
* [Available vector store integrations](https://docs.langchain.com/oss/python/integrations/vectorstores.md)

For more on RAG:

* [Retrieval overview](../../../Advanced%20usage/Retrieval.md)
* [RAG with Deep Agents](https://docs.langchain.com/oss/python/deepagents/rag.md)
* [Evaluate a RAG application](https://docs.langchain.com/langsmith/evaluate-rag-tutorial.md)

***

[Connect these docs](https://docs.langchain.com/use-these-docs.md) to your agent of choice via MCP for real-time answers.

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/langchain/knowledge-base.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).

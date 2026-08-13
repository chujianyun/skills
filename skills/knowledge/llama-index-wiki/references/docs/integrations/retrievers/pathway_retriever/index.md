# developers.llamaindex.ai/python/framework/integrations/retrievers/pathway_retriever/index.md
> https://developers.llamaindex.ai/python/framework/integrations/retrievers/pathway_retriever/index.md

[Column 1]
--- title: Pathway Retriever | Developer Documentation ---

In this notebook, we will use a public demo document processing pipeline [1] that:
1. Monitors several cloud data sources for data changes. 2. Builds a vector index for the data.
To have your own document processing pipeline check the hosted offering [2] or build your own [3] by following this notebook.
We will connect to the index using `llama_index.retrievers.pathway.PathwayRetriever` retriever, which implements the `retrieve` interface.
The basic pipeline described in this document allows to effortlessly build a simple index of files stored in a cloud location. However, Pathway provides everything needed to build realtime data pipelines and apps, including SQL-like able operations such as groupby-reductions and joins between disparate data sources, time-based grouping and windowing of data, and a wide array of connectors.
For more details about Pathway data ingestion pipeline and vector store, visit vector store pipeline [4].
## Prerequisites
To use `PathwayRetrievier` you must install `llama-index-retrievers-pathway` package.
``` !pip install llama-index-retrievers-pathway ```
## Create Retriever for llama-index
To instantiate and configure `PathwayRetriever` you need to provide either the `url` or the `host` and `port` of your document indexing pipeline. In the code below we use a publicly available [demo pipeline] [1], which REST API you can access at `https://demo-document-indexing.pathway.stream`. This demo ingests documents from [Google Drive] [6] and Sharepoint [5] and maintains an index for retrieving documents.

[Column 2]
> Pathway [7] is an open data processing framework. It allows you to easily develop data transformation pipelines and Machine Learning applications that work with live data sources and changing data.
This notebook demonstrates how to use a live data indexing pipeline with `LlamaIndex`. You can query the results of this pipeline from your LLM application using the provided `PathwayRetriever`. However, under the hood, Pathway updates the index on each data change giving you always up-to-date answers.


retriever = PathwayRetriever( url="https://demo-document-indexing.pathway.stream" ) retriever.retrieve(str_or_query_bundle="what is pathway") ```

**Your turn!** Get your pipeline [2] or upload new documents [8] to the demo pipeline and retry the query!
## Use in Query Engine
``` from llama_index.core.query_engine import RetrieverQueryEngine
query_engine = RetrieverQueryEngine.from_args( retriever, ) ```

``` response = query_engine.query("Tell me about Pathway") print(str(response)) ```

## Building your own data processing pipeline
### Prerequisites
Install `pathway` package. Then download sample data.
``` %pip install pathway %pip install llama-index-embeddings-openai ```

``` !mkdir -p 'data/' !wget 'https://gist.githubusercontent.com/janchorowski/dd22a293f3d99d1b726eedc7d46d2fc0/raw/pathway_readme.md' -O 'data/pathway_readme.md' ```

### Define data sources tracked by Pathway
Pathway can listen to many sources simultaneously, such as local files, S3 folders, cloud storage and any data stream for data changes.
See pathway-io [9] for more information.
``` import pathway as pw
data_sources = [] data_sources.append( pw.io.fs.read( "./data", format="binary", mode="streaming", with_metadata=True, ) # This creates a `pathway` connector that tracks # all the files in the ./data directory )

# This creates a connector that tracks files in Google drive. # please follow the instructions at https://pathway.com/developers/tutorials/connectors/gdrive-connector/ to get credentials # data_sources.append( # pw.io.gdrive.read(object_id="17H4YpBOAKQzEJ93xmC2z170l0bP2npMy", service_user_credentials_file="credentials.json", with_metadata=True)) ```

### Create the document indexing pipeline
Let us create the document indexing pipeline. The `transformations` should be a list of `TransformComponent`s ending with an `Embedding` transformation.
In this example, let’s first split the text first using `TokenTextSplitter`, then embed with `OpenAIEmbedding`.
``` from pathway.xpacks.llm.vector_store import VectorStoreServer from llama_index.embeddings.openai import OpenAIEmbedding from llama_index.core.node_parser import TokenTextSplitter

embed_model = OpenAIEmbedding(embed_batch_size=10)
transformations_example = [ TokenTextSplitter( chunk_size=150, chunk_overlap=10, separator=" ", ), embed_model, ]

processing_pipeline = VectorStoreServer.from_llamaindex_components( *data_sources, transformations=transformations_example, )

# Define the Host and port that Pathway will be on PATHWAY_HOST = "127.0.0.1" PATHWAY_PORT = 8754

# `threaded` runs pathway in detached mode, we have to set it to False when running from terminal or container # for more information on `with_cache` check out https://pathway.com/developers/api-docs/persistence-api processing_pipeline.run_server( host=PATHWAY_HOST, port=PATHWAY_PORT, with_cache=False, threaded=True ) ```

### Connect the retriever to the custom pipeline
``` from llama_index.retrievers.pathway import PathwayRetriever
retriever = PathwayRetriever(host=PATHWAY_HOST, port=PATHWAY_PORT) retriever.retrieve(str_or_query_bundle="what is pathway") ```

[1] https://pathway.com/solutions/ai-pipelines#try-it-out
[2] https://pathway.com/solutions/ai-pipelines
[3] https://pathway.com/developers/user-guide/llm-xpack/vectorstore_pipeline/
[4] https://pathway.com/developers/showcases/vectorstore_pipeline
[5] https://navalgo.sharepoint.com/sites/ConnectorSandbox/Shared%20Documents/Forms/AllItems.aspx? id=%2Fsites%2FConnectorSandbox%2FShared%20Documents%2FIndexerSandbox\&p=true\&ga=1
[6] https://drive.google.com/drive/u/0/folders/1cULDv2OaViJBmOfG5WB0oWcgayNrGtVs
[7] https://pathway.com/
[8] https://chat-realtime-sharepoint-gdrive.demo.pathway.com/
[9] https://pathway.com/developers/api-docs/pathway-io
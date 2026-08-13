# developers.llamaindex.ai/python/framework/integrations/vector_stores/vertexaivectorsearchdemo/index.md
> https://developers.llamaindex.ai/python/framework/integrations/vector_stores/vertexaivectorsearchdemo/index.md

--- title: Google Vertex AI Vector Search | Developer Documentation ---

This notebook shows how to use functionality related to the `Google Cloud Vertex AI Vector Search` vector database.
> Google Vertex AI Vector Search [1], formerly known as Vertex AI Matching Engine, provides the industry’s leading high-scale low latency vector database. These vector databases are commonly referred to as vector similarity-matching or an approximate nearest neighbor (ANN) service.
**Note**: LlamaIndex expects Vertex AI Vector Search endpoint and deployed index is already created. An empty index creation time take upto a minute and deploying an index to the endpoint can take upto 30 min.
> To see how to create an index refer to the section Create Index and deploy it to an Endpoint\ > If you already have an index deployed , skip to Create VectorStore from texts
## Installation
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.
``` ! pip install llama-index llama-index-vector-stores-vertexaivectorsearch llama-index-llms-vertex ```
## Create Index and deploy it to an Endpoint
- This section demonstrates creating a new index and deploying it to an endpoint.
``` # TODO : Set values as per your requirements
# Project and Storage Constants PROJECT_ID = "[your_project_id]" REGION = "[your_region]" GCS_BUCKET_NAME = "[your_gcs_bucket]" GCS_BUCKET_URI = f"gs://{GCS_BUCKET_NAME}"

# The number of dimensions for the textembedding-gecko@003 is 768 # If other embedder is used, the dimensions would probably need to change. VS_DIMENSIONS = 768

# Vertex AI Vector Search Index configuration # parameter description here # https://cloud.google.com/python/docs/reference/aiplatform/latest/google.cloud.aiplatform.MatchingEngineIndex#google_cloud_aiplatform_MatchingEngineIndex_create_tree_ah_index VS_INDEX_NAME = "llamaindex-doc-index" # @param {type:"string"} VS_INDEX_ENDPOINT_NAME = "llamaindex-doc-endpoint" # @param {type:"string"} ```

``` from google.cloud import aiplatform
aiplatform.init(project=PROJECT_ID, location=REGION) ```
### Create Cloud Storage bucket
``` # Create a bucket. ! gsutil mb -l $REGION -p $PROJECT_ID $GCS_BUCKET_URI ```

### Create an empty Index
**Note :** While creating an index you should specify an “index\_update\_method” - `BATCH_UPDATE` or `STREAM_UPDATE`
> A batch index is for when you want to update your index in a batch, with data which has been stored over a set amount of time, like systems which are processed weekly or monthly. > > A streaming index is when you want index data to be updated as new data is added to your datastore, for instance, if you have a bookstore and want to show new inventory online as soon as possible. > > Which type you choose is important, since setup and requirements are different.

Refer Official Documentation [2] and [API reference] [3] for more details on configuring indexes
``` # NOTE : This operation can take upto 30 seconds
# check if index exists index_names = [ index.resource_name for index in aiplatform.MatchingEngineIndex.list( filter=f"display_name={VS_INDEX_NAME}" ) ]

if len(index_names) == 0: print(f"Creating Vector Search index {VS_INDEX_NAME} ...") vs_index = aiplatform.MatchingEngineIndex.create_tree_ah_index( display_name=VS_INDEX_NAME, dimensions=VS_DIMENSIONS, distance_measure_type="DOT_PRODUCT_DISTANCE", shard_size="SHARD_SIZE_SMALL", index_update_method="STREAM_UPDATE", # allowed values BATCH_UPDATE , STREAM_UPDATE ) print( f"Vector Search index {vs_index.display_name} created with resource name {vs_index.resource_name}" ) else: vs_index = aiplatform.MatchingEngineIndex(index_name=index_names[0]) print( f"Vector Search index {vs_index.display_name} exists with resource name {vs_index.resource_name}" ) ```

### Create an Endpoint
To use the index, you need to create an index endpoint. It works as a server instance accepting query requests for your index. An endpoint can be a public endpoint [4] or a private endpoint [5].
Let’s create a public endpoint.
``` endpoint_names = [ endpoint.resource_name for endpoint in aiplatform.MatchingEngineIndexEndpoint.list( filter=f"display_name={VS_INDEX_ENDPOINT_NAME}" ) ]

if len(endpoint_names) == 0: print( f"Creating Vector Search index endpoint {VS_INDEX_ENDPOINT_NAME} ..." ) vs_endpoint = aiplatform.MatchingEngineIndexEndpoint.create( display_name=VS_INDEX_ENDPOINT_NAME, public_endpoint_enabled=True ) print( f"Vector Search index endpoint {vs_endpoint.display_name} created with resource name {vs_endpoint.resource_name}" ) else: vs_endpoint = aiplatform.MatchingEngineIndexEndpoint( index_endpoint_name=endpoint_names[0] ) print( f"Vector Search index endpoint {vs_endpoint.display_name} exists with resource name {vs_endpoint.resource_name}" ) ```

### Deploy Index to the Endpoint
With the index endpoint, deploy the index by specifying a unique deployed index ID.
**NOTE : This operation can take upto 30 minutes.**
``` # check if endpoint exists index_endpoints = [ (deployed_index.index_endpoint, deployed_index.deployed_index_id) for deployed_index in vs_index.deployed_indexes ]

if len(index_endpoints) == 0: print( f"Deploying Vector Search index {vs_index.display_name} at endpoint {vs_endpoint.display_name} ..." ) vs_deployed_index = vs_endpoint.deploy_index( index=vs_index, deployed_index_id=VS_INDEX_NAME, display_name=VS_INDEX_NAME, machine_type="e2-standard-16", min_replica_count=1, max_replica_count=1, ) print( f"Vector Search index {vs_index.display_name} is deployed at endpoint {vs_deployed_index.display_name}" ) else: vs_deployed_index = aiplatform.MatchingEngineIndexEndpoint( index_endpoint_name=index_endpoints[0][0] ) print( f"Vector Search index {vs_index.display_name} is already deployed at endpoint {vs_deployed_index.display_name}" ) ```

## Create Vector Store from texts
NOTE : If you have existing Vertex AI Vector Search Index and Endpoints, you can assign them using following code:
``` # TODO : replace 1234567890123456789 with your actual index ID vs_index = aiplatform.MatchingEngineIndex(index_name="1234567890123456789")

# TODO : replace 1234567890123456789 with your actual endpoint ID vs_endpoint = aiplatform.MatchingEngineIndexEndpoint( index_endpoint_name="1234567890123456789" ) ```

``` # import modules needed from llama_index.core import ( StorageContext, Settings, VectorStoreIndex, SimpleDirectoryReader, ) from llama_index.core.schema import TextNode from llama_index.core.vector_stores.types import ( MetadataFilters, MetadataFilter, FilterOperator, ) from llama_index.llms.vertex import Vertex from llama_index.embeddings.vertex import VertexTextEmbedding from llama_index.vector_stores.vertexaivectorsearch import VertexAIVectorStore ```

### Create a simple vector store from plain text without metadata filters

# set storage context storage_context = StorageContext.from_defaults(vector_store=vector_store) ```
### Use Vertex AI Embeddings [6] as the embeddings model
``` # configure embedding model embed_model = VertexTextEmbedding( model_name="textembedding-gecko@003", project=PROJECT_ID, location=REGION, )

# setup the index/query process, ie the embedding model (and completion if used) Settings.embed_model = embed_model ```
### Add vectors and mapped text chunks to your vectore store
``` # Input texts texts = [ "The cat sat on", "the mat.", "I like to", "eat pizza for", "dinner.", "The sun sets", "in the west.", ] nodes = [ TextNode(text=text, embedding=embed_model.get_text_embedding(text)) for text in texts ]

### Running a similarity search
``` # define index from vector store index = VectorStoreIndex.from_vector_store( vector_store=vector_store, embed_model=embed_model ) retriever = index.as_retriever() ```

``` response = retriever.retrieve("pizza") for row in response: print(f"Score: {row.get_score():.3f} Text: {row.get_text()}") ```

``` Score: 0.703 Text: eat pizza for Score: 0.626 Text: dinner. ```

## Add documents with metadata attributes and use filters
``` # Input text with metadata records = [ { "description": "A versatile pair of dark-wash denim jeans." "Made from durable cotton with a classic straight-leg cut, these jeans" " transition easily from casual days to dressier occasions.", "price": 65.00, "color": "blue", "season": ["fall", "winter", "spring"], }, { "description": "A lightweight linen button-down shirt in a crisp white." " Perfect for keeping cool with breathable fabric and a relaxed fit.", "price": 34.99, "color": "white", "season": ["summer", "spring"], }, { "description": "A soft, chunky knit sweater in a vibrant forest green. " "The oversized fit and cozy wool blend make this ideal for staying warm " "when the temperature drops.", "price": 89.99, "color": "green", "season": ["fall", "winter"], }, { "description": "A classic crewneck t-shirt in a soft, heathered blue. " "Made from comfortable cotton jersey, this t-shirt is a wardrobe essential "

"that works for every season.", "price": 19.99, "color": "blue", "season": ["fall", "winter", "summer", "spring"], }, { "description": "A flowing midi-skirt in a delicate floral print. " "Lightweight and airy, this skirt adds a touch of feminine style " "to warmer days.", "price": 45.00, "color": "white", "season": ["spring", "summer"], }, ]

nodes = [] for record in records: text = record.pop("description") embedding = embed_model.get_text_embedding(text) metadata = {**record} nodes.append(TextNode(text=text, embedding=embedding, metadata=metadata))

vector_store.add(nodes) ```
### Running a similarity search with filters
``` # define index from vector store index = VectorStoreIndex.from_vector_store( vector_store=vector_store, embed_model=embed_model ) ```

``` # simple similarity search without filter retriever = index.as_retriever() response = retriever.retrieve("pants")

``` Text: A pair of well-tailored dress pants in a neutral grey. Made from a wrinkle-resistant blend, these pants look sharp and professional for workwear or formal occasions. Score: 0.669 Metadata: {'price': 69.99, 'color': 'grey', 'season': ['fall', 'winter', 'summer', 'spring']} Text: A pair of tailored black trousers in a comfortable stretch fabric. Perfect for work or dressier events, these trousers provide a sleek, polished look. Score: 0.642 Metadata: {'price': 59.99, 'color': 'black', 'season': ['fall', 'winter', 'spring']} ```
``` # similarity search with text filter filters = MetadataFilters(filters=[MetadataFilter(key="color", value="blue")]) retriever = index.as_retriever(filters=filters, similarity_top_k=3) response = retriever.retrieve("denims")

``` Text: A versatile pair of dark-wash denim jeans.Made from durable cotton with a classic straight-leg cut, these jeans transition easily from casual days to dressier occasions. Score: 0.704 Metadata: {'price': 65.0, 'color': 'blue', 'season': ['fall', 'winter', 'spring']} Text: A denim jacket with a faded wash and distressed details. This wardrobe staple adds a touch of effortless cool to any outfit. Score: 0.667 Metadata: {'price': 79.99, 'color': 'blue', 'season': ['fall', 'spring', 'summer']} ```

``` # similarity search with text and numeric filter filters = MetadataFilters( filters=[ MetadataFilter(key="color", value="blue"), MetadataFilter(key="price", operator=FilterOperator.GT, value=70.0), ] ) retriever = index.as_retriever(filters=filters, similarity_top_k=3) response = retriever.retrieve("denims")

for row in response: print(f"Text: {row.get_text()}") print(f" Score: {row.get_score():.3f}") print(f" Metadata: {row.metadata}") ```
``` Text: A denim jacket with a faded wash and distressed details. This wardrobe staple adds a touch of effortless cool to any outfit. Score: 0.667 Metadata: {'price': 79.99, 'color': 'blue', 'season': ['fall', 'spring', 'summer']} ```
## Parse, Index and Query PDFs using Vertex AI Vector Search and Gemini Pro
``` ! mkdir -p ./data/arxiv/ ! wget 'https://arxiv.org/pdf/1706.03762.pdf' -O ./data/arxiv/test.pdf ```
``` E0501 00:56:50.842446801 266241 backup_poller.cc:127] Run client channel backup poller: UNKNOWN:pollset_work {created_time:"2024-05-01T00:56:50.841935606+00:00", children:[UNKNOWN:Bad file descriptor {created_time:"2024-05-01T00:56:50.841810434+00:00", errno:9, os_error:"Bad file descriptor", syscall:"epoll_wait"}]} --2024-05-01 00:56:52-- https://arxiv.org/pdf/1706.03762.pdf Resolving arxiv.org (arxiv.org)... 151.101.67.42, 151.101.195.42, 151.101.131.42, ... Connecting to arxiv.org (arxiv.org)|151.101.67.42|:443... connected. HTTP request sent, awaiting response... 301 Moved Permanently Location: http://arxiv.org/pdf/1706.03762 [following] --2024-05-01 00:56:52-- http://arxiv.org/pdf/1706.03762 Connecting to arxiv.org (arxiv.org)|151.101.67.42|:80... connected. HTTP request sent, awaiting response... 200 OK Length: 2215244 (2.1M) [application/pdf] Saving to: ‘./data/arxiv/test.pdf’

./data/arxiv/test.p 100%[===================>] 2.11M --.-KB/s in 0.07s
2024-05-01 00:56:52 (31.5 MB/s) - ‘./data/arxiv/test.pdf’ saved [2215244/2215244] ```
``` # load documents documents = SimpleDirectoryReader("./data/arxiv/").load_data() print(f"# of documents = {len(documents)}") ```
``` # of documents = 15 ```
``` # setup storage vector_store = VertexAIVectorStore( project_id=PROJECT_ID, region=REGION, index_id=vs_index.resource_name, endpoint_id=vs_endpoint.resource_name, gcs_bucket_name=GCS_BUCKET_NAME, )

# set storage context storage_context = StorageContext.from_defaults(vector_store=vector_store)
# configure embedding model embed_model = VertexTextEmbedding( model_name="textembedding-gecko@003", project=PROJECT_ID, location=REGION, )

vertex_gemini = Vertex( model="gemini-pro", context_window=100000, temperature=0, additional_kwargs={}, )

# setup the index/query process, ie the embedding model (and completion if used) Settings.llm = vertex_gemini Settings.embed_model = embed_model ```
``` # define index from vector store index = VectorStoreIndex.from_documents( documents, storage_context=storage_context ) ```

``` query_engine = index.as_query_engine() ```
``` response = query_engine.query( "who are the authors of paper Attention is All you need?" )
print(f"Response:") print("-" * 80) print(response.response) print("-" * 80) print(f"Source Documents:") print("-" * 80) for source in response.source_nodes: print(f"Sample Text: {source.text[:50]}") print(f"Relevance score: {source.get_score():.3f}") print(f"File Name: {source.metadata.get('file_name')}") print(f"Page #: {source.metadata.get('page_label')}") print(f"File Path: {source.metadata.get('file_path')}") print("-" * 80) ```

``` Response: -------------------------------------------------------------------------------- The authors of the paper "Attention Is All You Need" are:
* Ashish Vaswani * Noam Shazeer * Niki Parmar * Jakob Uszkoreit * Llion Jones * Aidan N. Gomez * Łukasz Kaiser * Illia Polosukhin -------------------------------------------------------------------------------- Source Documents: -------------------------------------------------------------------------------- Sample Text: Provided proper attribution is provided, Google he Relevance score: 0.720 File Name: test.pdf Page #: 1 File Path: /home/jupyter/llama_index/docs/examples/vector_stores/data/arxiv/test.pdf -------------------------------------------------------------------------------- Sample Text: length nis smaller than the representation dimensi Relevance score: 0.678 File Name: test.pdf Page #: 7 File Path: /home/jupyter/llama_index/docs/examples/vector_stores/data/arxiv/test.pdf -------------------------------------------------------------------------------- ```

---
## Clean Up
Please delete Vertex AI Vector Search Index and Index Endpoint after running your experiments to avoid incurring additional charges. Please note that you will be charged as long as the endpoint is running.
**⚠️ NOTE: Enabling \`CLEANUP\_RESOURCES\` flag deletes Vector Search Index, Index Endpoint and Cloud Storage bucket. Please run it with caution.**
``` CLEANUP_RESOURCES = False ```
- Undeploy indexes and Delete index endpoint
``` if CLEANUP_RESOURCES: print( f"Undeploying all indexes and deleting the index endpoint {vs_endpoint.display_name}" ) vs_endpoint.undeploy_all() vs_endpoint.delete() ```

- Delete index
``` if CLEANUP_RESOURCES: print(f"Deleting the index {vs_index.display_name}") vs_index.delete() ```
- Delete contents from the Cloud Storage bucket
``` if CLEANUP_RESOURCES and "GCS_BUCKET_NAME" in globals(): print(f"Deleting contents from the Cloud Storage bucket {GCS_BUCKET_NAME}")
shell_output = ! gsutil du -ash gs://$GCS_BUCKET_NAME print(shell_output) print( f"Size of the bucket {GCS_BUCKET_NAME} before deleting = {' '.join(shell_output[0].split()[:2])}" )

# uncomment below line to delete contents of the bucket # ! gsutil -m rm -r gs://$GCS_BUCKET_NAME ```

[1] https://cloud.google.com/vertex-ai/docs/vector-search/overview
[2] https://cloud.google.com/vertex-ai/docs/vector-search/create-manage-index
[3] https://cloud.google.com/python/docs/reference/aiplatform/latest/google.cloud.aiplatform.MatchingEngineIndex#google_cloud_aiplatform_MatchingEngineIndex_create_tree_ah_index
[4] https://cloud.google.com/vertex-ai/docs/vector- search/deploy-index-public
[5] https://cloud.google.com/vertex-ai/docs/vector-search/deploy-index-vpc
[6] https://github.com/run-llama/llama_index/tree/main/llama-index-integrations/embeddings/llama-index-embeddings-vertex